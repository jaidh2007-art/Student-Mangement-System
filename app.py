from flask import Flask, render_template, request, redirect, url_for, flash
import database as db

app = Flask(__name__)
app.secret_key = 'super-secret-key-change-this-in-production'

# Ensure the database and table exist before the first request
with app.app_context():
    db.init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students')
def students():
    all_students = db.get_all_students()
    return render_template('students.html', students=all_students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        grade = request.form['grade']

        if not name or not email:
            flash('Name and Email are required!', 'error')
            return redirect(url_for('add_student'))

        db.insert_student(name, email, course, grade)
        flash('Student added successfully!', 'success')
        return redirect(url_for('students'))

    return render_template('add_student.html')

@app.route('/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = db.get_student_by_id(student_id)
    if not student:
        flash('Student not found!', 'error')
        return redirect(url_for('students'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        grade = request.form['grade']

        db.update_student(student_id, name, email, course, grade)
        flash('Student updated successfully!', 'success')
        return redirect(url_for('students'))

    return render_template('edit_student.html', student=student)

@app.route('/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    db.delete_student(student_id)
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('students'))

if __name__ == '__main__':
    app.run(debug=True)
