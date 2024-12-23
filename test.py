from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
import mysql.connector
from mysql.connector import Error
import datetime
import csv
import io

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.add_url_rule('/photos/<path:filename>', endpoint='photos', view_func=app.send_static_file)

# MySQL Connection Function
def connect_db(user, password, db):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user=user,
            password=password,
            database=db
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

@app.route('/photo')
def photo():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title': 'Latest Photo',
        'time': timeString
    }
    return render_template('photo1.html', **templateData)

# Login Page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in ['user1', 'user2', 'user3', 'user4'] and password == f'password{username[-1]}':
            session['user'] = username
            return redirect(url_for('user', db=f'database{username[-1]}'))
        else:
            flash('Invalid login credentials')

    return render_template('authentication/login.html')

# User Dashboard
@app.route('/dashboard/<db>', methods=['GET', 'POST'])
def user_dashboard(db):
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))

    connection = connect_db(user, f'password{user[-1]}', db)
    if connection:
        cursor = connection.cursor()
        if request.method == 'POST':
            data = (
                request.form['enroll_no'],
                request.form['course'],
                request.form['sex'],
                request.form['name'],
                request.form['father_name'],
                request.form['address1'],
                request.form['address2'],
                request.form['city'],
                request.form['pincode'],
                request.form['qualification'],
                request.form['date_of_join'],
                request.form['age'],
                request.form['scheme'],
                request.form['date_of_birth'],
                request.form['concession'],
                request.form['net_fees']
            )
            cursor.execute('''
                INSERT INTO student_details (enroll_no, course, sex, name, father_name, address1, address2, city, pincode, 
                qualification, date_of_join, age, scheme, date_of_birth, concession, net_fees) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', data)
            connection.commit()
            flash('Student details added successfully')

        return render_template('application/add.html', db=db)
    else:
        flash('Failed to connect to the database')
        return redirect(url_for('login'))

# Update Student Details
@app.route('/edit/<db>', methods=['GET', 'POST'])
def update_student(db):
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))

    connection = connect_db(user, f'password{user[-1]}', db)
    if connection:
        cursor = connection.cursor()
        if request.method == 'POST':
            enroll_no = request.form['enroll_no']
            updated_data = (
                request.form['course'],
                request.form['sex'],
                request.form['name'],
                request.form['father_name'],
                request.form['address1'],
                request.form['address2'],
                request.form['city'],
                request.form['pincode'],
                request.form['qualification'],
                request.form['date_of_join'],
                request.form['age'],
                request.form['scheme'],
                request.form['date_of_birth'],
                request.form['concession'],
                request.form['net_fees'],
                enroll_no
            )
            cursor.execute('''
                UPDATE student_details
                SET course=%s, sex=%s, name=%s, father_name=%s, address1=%s, address2=%s, city=%s, pincode=%s, 
                qualification=%s, date_of_join=%s, age=%s, scheme=%s, date_of_birth=%s, concession=%s, net_fees=%s
                WHERE enroll_no=%s
            ''', updated_data)
            connection.commit()
            flash('Student details updated successfully')

        return render_template('application/edit.html', db=db)
    else:
        flash('Failed to connect to the database')
        return redirect(url_for('login'))

# Delete Student Details
@app.route('/delete/<db>', methods=['GET', 'POST'])
def delete_student(db):
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))

    connection = connect_db(user, f'password{user[-1]}', db)
    if connection:
        cursor = connection.cursor()
        if request.method == 'POST':
            enroll_no = request.form['enroll_no']
            cursor.execute('DELETE FROM student_details WHERE enroll_no=%s', (enroll_no,))
            connection.commit()
            flash('Student record deleted successfully')

        return render_template('application/delete.html', db=db)
    else:
        flash('Failed to connect to the database')
        return redirect(url_for('login'))

# Information Page
@app.route('/information/<db>', methods=['GET'])
def information_dashboard(db):
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))

    connection = connect_db(user, f'password{user[-1]}', db)
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM student_information_sheet")
        students = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('information/user_dashboard.html', students=students)
    else:
        flash('Failed to connect to the database')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
