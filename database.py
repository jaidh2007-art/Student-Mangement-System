import sqlite3

DB_NAME = 'students.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            course TEXT,
            grade TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_all_students():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return students

def get_student_by_id(student_id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    conn.close()
    return student

def insert_student(name, email, course, grade):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO students (name, email, course, grade) VALUES (?, ?, ?, ?)',
        (name, email, course, grade)
    )
    conn.commit()
    conn.close()

def update_student(student_id, name, email, course, grade):
    conn = get_db_connection()
    conn.execute(
        'UPDATE students SET name = ?, email = ?, course = ?, grade = ? WHERE id = ?',
        (name, email, course, grade, student_id)
    )
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id = ?', (student_id,))
    conn.commit()
    conn.close()
