import unittest
from unittest.mock import patch, MagicMock
from module_database import setup_database, execute_stored_procedure
from module_validate import validate_email, validate_contact
from tkinter import Tk, StringVar, Text
from module_gui import (add_student, update_student, delete_student, clear_fields )
import mysql.connector


class TestDatabaseModule(unittest.TestCase):
    @patch('mysql.connector.connect')
    def test_setup_database_success(self, mock_connect):
        """Test setup_database connects to the database and creates the table."""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        setup_database()
        mock_connect.assert_called_once()
        mock_conn.cursor().execute.assert_called_with('''CREATE TABLE IF NOT EXISTS students (
                            name VARCHAR(100),
                            roll_no INT PRIMARY KEY,
                            email VARCHAR(100),
                            gender VARCHAR(10),
                            contact VARCHAR(20),
                            dob DATE,
                            address TEXT
                        )''')
        mock_conn.commit.assert_called_once()

    @patch('mysql.connector.connect')
    def test_setup_database_connection_error(self, mock_connect):
        mock_connect.side_effect = Exception("Connection Error")
        with self.assertRaises(Exception):
            setup_database()

    @patch('mysql.connector.connect')
    def test_execute_stored_procedure_success(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        # Simulate stored procedure results
        mock_result_set = MagicMock()
        mock_cursor.stored_results.return_value = [mock_result_set]
        results = execute_stored_procedure(
            "ManageStudents",
            ('GetAll', None, None, None, None, None, None, None, None, None))
        mock_conn.cursor.assert_called_once()
        mock_cursor.callproc.assert_called_once_with(
            "ManageStudents",
            ('GetAll', None, None, None, None, None, None, None, None, None) )
        self.assertEqual(results, [mock_result_set])

    @patch('mysql.connector.connect')
    def test_execute_stored_procedure_error(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.callproc.side_effect = mysql.connector.Error("Procedure Error")
        with self.assertRaises(mysql.connector.Error) as context:
            execute_stored_procedure("ManageStudents",
                ('GetAll', None, None, None, None, None, None, None, None, None) )
        self.assertEqual(str(context.exception), "Procedure Error")
        mock_cursor.callproc.assert_called_once_with(
            "ManageStudents",
            ('GetAll', None, None, None, None, None, None, None, None, None) )


class TestValidationModule(unittest.TestCase):
    def test_validate_email_valid(self):
        self.assertTrue(validate_email("test@gmail.com"))
        self.assertTrue(validate_email("user@yahoo.com"))

    def test_validate_email_invalid(self):
        self.assertFalse(validate_email("invalid-email"))
        self.assertFalse(validate_email("missinguser.com"))

    def test_validate_contact_valid(self):
        self.assertTrue(validate_contact("1234567890"))
        self.assertTrue(validate_contact("0987654321"))

    def test_validate_contact_invalid(self):
        self.assertFalse(validate_contact("123"))
        self.assertFalse(validate_contact("abcd12345"))


class TestAddStudent(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.name_var = StringVar()
        self.roll_var = StringVar()
        self.email_var = StringVar()
        self.gender_var = StringVar()
        self.contact_var = StringVar()
        self.dob_entry = StringVar()
        self.address_text = Text(self.root)
        global name_var, roll_var, email_var, gender_var, contact_var, dob_entry, address_text
        name_var = self.name_var
        roll_var = self.roll_var
        email_var = self.email_var
        gender_var = self.gender_var
        contact_var = self.contact_var
        dob_entry = self.dob_entry
        address_text = self.address_text

    def tearDown(self):
        self.root.destroy()

    @patch('module_gui.messagebox')
    def test_add_student_missing_fields(self, mock_messagebox):
        add_student()
        mock_messagebox.showerror.assert_called_once_with("Error", "All fields are required")

    @patch('module_gui.messagebox')
    def test_add_student_invalid_email(self, mock_messagebox):
        self.name_var.set("John Doe")
        self.roll_var.set("123")
        self.email_var.set("invalid-email")
        self.gender_var.set("Male")
        self.contact_var.set("1234567890")
        self.dob_entry.set("2000-01-01")
        self.address_text.insert("1.0", "123 Main St")
        add_student()
        mock_messagebox.showerror.assert_called_once_with


class TestDeleteStudent(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.roll_var = StringVar()
        self.address_text = Text(self.root)
        global roll_var, address_text
        roll_var = self.roll_var
        address_text = self.address_text

    def tearDown(self):
        self.root.destroy()


    @patch('module_gui.messagebox')
    @patch('module_database.execute_stored_procedure')
    def test_delete_student_non_existent(self, mock_execute, mock_messagebox):
        self.roll_var.set("999")
        mock_execute.return_value = []
        delete_student()
        mock_messagebox.showerror.assert_called_once_with("Error", "No student selected")

    @patch('module_gui.messagebox')
    def test_delete_student_without_selection(self, mock_messagebox):
        self.roll_var.set("")
        delete_student()
        mock_messagebox.showerror.assert_called_once_with("Error", "No student selected")


class TestUpdateStudent(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.name_var = StringVar()
        self.roll_var = StringVar()
        self.email_var = StringVar()
        self.gender_var = StringVar()
        self.contact_var = StringVar()
        self.dob_entry = StringVar()
        self.address_text = Text(self.root)

        global name_var, roll_var, email_var, gender_var, contact_var, dob_entry, address_text
        name_var = self.name_var
        roll_var = self.roll_var
        email_var = self.email_var
        gender_var = self.gender_var
        contact_var = self.contact_var
        dob_entry = self.dob_entry
        address_text = self.address_text

    def tearDown(self):
        self.root.destroy()

    @patch('module_gui.messagebox')
    def test_update_student_missing_fields(self, mock_messagebox):
        update_student()
        mock_messagebox.showerror.assert_called_once_with("Error", "No fields are selected")


class TestClearFields(unittest.TestCase):
    def setUp(self):
        # Set up a basic Tkinter window and variables
        self.root = Tk()
        self.name_var = StringVar()
        self.roll_var = StringVar()
        self.email_var = StringVar()
        self.gender_var = StringVar()
        self.contact_var = StringVar()
        self.dob_entry = StringVar()
        self.address_text = Text(self.root)

        # Assign the variables to the global scope for the module
        global name_var, roll_var, email_var, gender_var, contact_var, dob_entry, address_text
        name_var = self.name_var
        roll_var = self.roll_var
        email_var = self.email_var
        gender_var = self.gender_var
        contact_var = self.contact_var
        dob_entry = self.dob_entry
        address_text = self.address_text

    def tearDown(self):
        self.root.destroy()

    def test_clear_fields(self):
        clear_fields()
        # Verify all fields are cleared
        self.assertEqual(self.name_var.get(), "")
        self.assertEqual(self.roll_var.get(), "")
        self.assertEqual(self.email_var.get(), "")
        self.assertEqual(self.gender_var.get(), "")
        self.assertEqual(self.contact_var.get(), "")
        self.assertEqual(self.dob_entry.get(), "")
        self.assertEqual(self.address_text.get("1.0", "end").strip(), "")

if __name__ == '__main__':
    unittest.main()
