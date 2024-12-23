# CREATE DATABASE my_database;

# USE my_database;

# CREATE TABLE students (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(100) NOT NULL,
#     course VARCHAR(100) NOT NULL,
#     fees DECIMAL(10, 2) NOT NULL
# );


import mysql.connector

def insert_student(name, course, fees):
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host='localhost',      # Change this to your MySQL server host
            user='root',           # Change this to your MySQL username
            password='1234',   # Change this to your MySQL password
            database='csc' # Change this to your database name
        )

        cursor = connection.cursor()

        # SQL Query to insert data
        query = "INSERT INTO students (name, course, fees) VALUES (%s, %s, %s)"
        values = (name, course, fees)

        # Execute the query
        cursor.execute(query, values)
        
        connection.commit()  # Commit changes to the database

        print(f"Student {name} inserted successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the connection
        if connection.is_connected():
            cursor.close()
            connection.close()

# Example usage
insert_student("ram", "Python Programming", 500.00)




# import mysql.connector

# def update_student(name, course=None, fees=None):
#     try:
#         # Connect to the database
#         connection = mysql.connector.connect(
#             host='localhost',      # Change this to your MySQL server host
#             user='root',           # Change this to your MySQL username
#             password='password',   # Change this to your MySQL password
#             database='my_database' # Change this to your database name
#         )

#         cursor = connection.cursor()

#         # Build the SQL query dynamically
#         updates = []
#         values = []

#         if course:
#             updates.append("course = %s")
#             values.append(course)

#         if fees:
#             updates.append("fees = %s")
#             values.append(fees)

#         if not updates:
#             print("No updates specified.")
#             return

#         query = f"UPDATE students SET {', '.join(updates)} WHERE name = %s"
#         values.append(name)

#         # Execute the query
#         cursor.execute(query, tuple(values))
#         connection.commit()

#         if cursor.rowcount > 0:
#             print(f"Student {name}'s record updated successfully!")
#         else:
#             print(f"No record found for student {name}.")

#     except mysql.connector.Error as err:
#         print(f"Error: {err}")

#     finally:
#         # Close the connection
#         if connection.is_connected():
#             cursor.close()
#             connection.close()

# # Example usage
# update_student("Alice", course="Advanced Python", fees=600.00)
# update_student("Bob", fees=800.00)


# import mysql.connector

# def delete_student(name):
#     try:
#         # Connect to the database
#         connection = mysql.connector.connect(
#             host='localhost',      # Change this to your MySQL server host
#             user='root',           # Change this to your MySQL username
#             password='password',   # Change this to your MySQL password
#             database='my_database' # Change this to your database name
#         )

#         cursor = connection.cursor()

#         # SQL query to delete a record
#         query = "DELETE FROM students WHERE name = %s"
#         value = (name,)

#         # Execute the query
#         cursor.execute(query, value)
#         connection.commit()

#         if cursor.rowcount > 0:
#             print(f"Student {name} deleted successfully!")
#         else:
#             print(f"No record found for student {name}.")

#     except mysql.connector.Error as err:
#         print(f"Error: {err}")

#     finally:
#         # Close the connection
#         if connection.is_connected():
#             cursor.close()
#             connection.close()

# # Example usage
# delete_student("Alice")
# delete_student("Bob")
