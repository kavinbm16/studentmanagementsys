import mysql.connector
from tkinter import messagebox

def setup_database():
    """Connect to the database and create the students table if it doesn't exist."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="students_db"
        )
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                            name VARCHAR(100),
                            roll_no INT PRIMARY KEY,
                            email VARCHAR(100),
                            gender VARCHAR(10),
                            contact VARCHAR(20),
                            dob DATE,
                            address TEXT
                        )''')
        conn.commit()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error connecting to MySQL: {err}")


def execute_stored_procedure(proc_name, args):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="students_db"
        )
        # Explicitly get the cursor from the connection
        cursor = conn.cursor()
        cursor.callproc(proc_name, args)
        conn.commit()
        return list(cursor.stored_results())
    except mysql.connector.Error:
        # Re-raise the error for the test to catch
        raise


