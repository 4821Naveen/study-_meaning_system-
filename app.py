from flask import Flask, render_template, request, redirect, url_for, flash, session ,send_file
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




@app.route('/das/<db>', methods=['GET', 'POST'])
def user(db):
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))

    connection = connect_db(user, f'password{user[-1]}', db)
    if connection:
        cursor = connection.cursor(dictionary=True)
        # Fetch all students
        cursor.execute("SELECT enroll_no, name, course FROM student_details")
        students = cursor.fetchall()
        
        return render_template('application/user_dashboard.html', db=db, user=user, students=students)
    
    else:
        flash('Failed to connect to the database')
        return redirect(url_for('login'))
    

@app.route('/export_application/<db>/<table_name>', methods=['GET'])
def export_application(db, table_name):
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))

    connection = connect_db(user, f'password{user[-1]}', db)
    if connection:
        cursor = connection.cursor()

        try:
            # Fetch data from the specified table
            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)
            rows = cursor.fetchall()

            # Get column headers
            column_headers = [i[0] for i in cursor.description]

            # Create an in-memory file for the CSV
            output = io.StringIO()
            writer = csv.writer(output)

            # Write column headers to the CSV
            writer.writerow(column_headers)

            # Write data rows to the CSV
            writer.writerows(rows)

            output.seek(0)

            # Send the CSV as a downloadable file
            return send_file(
                io.BytesIO(output.getvalue().encode('utf-8')),
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'{table_name}.csv'
            )
        except Error as e:
            flash(f"Failed to export data: {e}")
            return redirect(url_for('user_dashboard', db=db))
        finally:
            cursor.close()
            connection.close()
    else:
        flash('Failed to connect to the database')
        return redirect(url_for('login'))

@app.route('/report/<db>', methods=['GET'])
def report(db):
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))

    connection = connect_db(user, f'password{user[-1]}', db)
    if connection:
        cursor = connection.cursor(dictionary=True)
        
        try:
            # Query to get monthly fees (using numeric month)
            cursor.execute("""
                SELECT MONTH(date_of_join) AS month, SUM(net_fees) AS total_fees
                FROM student_details
                GROUP BY MONTH(date_of_join)
                ORDER BY MONTH(date_of_join)
            """)
            fee_data = cursor.fetchall()

            # Query to get student data grouped by month (numeric month)
            cursor.execute("""
                SELECT MONTH(date_of_join) AS month, COUNT(*) AS student_count
                FROM student_details
                GROUP BY MONTH(date_of_join)
            """)
            student_data = cursor.fetchall()

            # Query to get course data grouped by month (numeric month)
            cursor.execute("""
                SELECT MONTH(date_of_join) AS month, COUNT(DISTINCT course) AS course_count
                FROM student_details
                GROUP BY MONTH(date_of_join)
            """)
            course_data = cursor.fetchall()

            # Prepare data for Chart.js
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            student_counts = [0] * 12
            course_counts = [0] * 12
            fees = [0] * 12

            # Map fee data to the correct index based on numeric month
            for data in fee_data:
                month_index = data['month'] - 1  # Convert to 0-indexed
                fees[month_index] = data['total_fees']

            # Map student data to the correct index based on numeric month
            for data in student_data:
                month_index = data['month'] - 1  # Convert to 0-indexed
                student_counts[month_index] = data['student_count']

            # Map course data to the correct index based on numeric month
            for data in course_data:
                month_index = data['month'] - 1  # Convert to 0-indexed
                course_counts[month_index] = data['course_count']

            return render_template('report/report_course.html', db=db, months=months, 
                                   student_counts=student_counts, course_counts=course_counts, fees=fees)
        
        except Error as e:
            flash(f"Failed to fetch report data: {e}")
            return redirect(url_for('user_dashboard', db=db))
        
        finally:
            cursor.close()
            connection.close()
    else:
        flash('Failed to connect to the database')
        return redirect(url_for('login'))


    
########################################################################################################

""" these functions use to information """

@app.route('/information/<db>', methods=['GET'])
def information_dashboard(db):
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))

    connection = connect_db(user, f'password{user[-1]}', db)
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM student_information_sheet")
            students = cursor.fetchall()
            return render_template('information/user_dashboard.html', students=students, db=db)
        except Error as e:
            flash(f"Failed to fetch data: {e}", "danger")
        finally:
            cursor.close()
            connection.close()
    flash("Failed to connect to the database", "danger")
    return redirect(url_for('login'))


# Form Route for Adding Student Information
@app.route('/information_form/<db>', methods=['GET', 'POST'])
def information_form(db):
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        father_name = request.form.get('father_name')
        employment_status = request.form.get('employment_status')
        address = request.form.get('address')
        pin_code = request.form.get('pin_code')
        sex = request.form.get('sex')
        qualification = request.form.get('qualification')
        reason = request.form.get('reason')
        course_interested = request.form.get('course_interested')
        joining_plan = request.form.get('joining_plan')
        source_info = ', '.join(request.form.getlist('source_info'))

        connection = connect_db(user, f'password{user[-1]}', db)
        if connection:
            try:
                cursor = connection.cursor()
                insert_query = """
                INSERT INTO student_information_sheet 
                (name, father_name, employment_status, address, pin_code, sex, qualification, reason, 
                 course_interested, joining_plan, source_info)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    name, father_name, employment_status, address, pin_code, sex,
                    qualification, reason, course_interested, joining_plan, source_info
                ))
                connection.commit()
                flash("Form submitted successfully!", "success")
                return redirect(url_for('information_dashboard', db=db))
            except Error as e:
                flash(f"Failed to submit the form: {e}", "danger")
            finally:
                cursor.close()
                connection.close()
        else:
            flash("Failed to connect to the database", "danger")

    return render_template('information/add.html', db=db)


# Export Data to CSV Route
@app.route('/export_information/<db>/<table_name>', methods=['GET'])

def export_information(db, table_name):
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))

    connection = connect_db(user, f'password{user[-1]}', db)
    if connection:
        cursor = connection.cursor()
        try:
            # Fetch data from the specified table
            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)
            rows = cursor.fetchall()

            if not rows:
                flash("No data available to export.", "warning")
                return redirect(url_for('information_dashboard', db=db))

            # Get column headers
            column_headers = [i[0] for i in cursor.description]

            # Create an in-memory file for the CSV
            output = io.StringIO()
            writer = csv.writer(output)

            # Write column headers to the CSV
            writer.writerow(column_headers)

            # Write data rows to the CSV
            writer.writerows(rows)

            output.seek(0)

            # Send the CSV as a downloadable file
            return send_file(
                io.BytesIO(output.getvalue().encode('utf-8')),
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'{table_name}.csv'
            )
        except Error as e:
            flash(f"Failed to export data: {e}", "danger")
            return redirect(url_for('information_dashboard', db=db))
        finally:
            cursor.close()
            connection.close()
    else:
        flash("Failed to connect to the database", "danger")
        return redirect(url_for('login'))



########################################################################################################

@app.route('/logout')
def logout():
    # Clear the session to log out the user
    session.clear()
    flash('You have been logged out successfully.')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

