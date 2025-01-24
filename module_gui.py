import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
from module_database import setup_database, execute_stored_procedure
from module_validate import validate_email,validate_contact

def update_clock():
    current_time = datetime.now().strftime("%H:%M:%S")
    clock_label.config(text=current_time)
    root.after(1000, update_clock)

def clear_fields():
    name_var.set("")
    roll_var.set("")
    email_var.set("")
    gender_var.set("")
    contact_var.set("")
    dob_entry.set("")
    address_text.delete("1.0", "end")

def clear_fields():
    try:
        name_var.set("")
        roll_var.set("")
        email_var.set("")
        gender_var.set("")
        contact_var.set("")
        dob_entry.set_date(datetime.now().date())
        address_text.delete("1.0", tk.END)
        roll_entry.config(state="normal")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to clear fields: {e}")

def on_tree_select(root):
    try:
        selected_item = tree.selection()[0]
        values = tree.item(selected_item, "values")
        roll_var.set(values[1])
        name_var.set(values[0])
        email_var.set(values[2])
        gender_var.set(values[3])
        contact_var.set(values[4])
        dob_entry.set_date(values[5])
        address_text.delete("1.0", "end")
        address_text.insert("1.0", values[6])
        roll_entry.config(state="disabled")
    except IndexError:
        pass

def search_students():
    search_by = search_var.get()
    search_query = search_entry.get()
    if not search_query:
        messagebox.showerror("Error", "Please enter a value to search.")
        return
    query_map = {
        "Roll No": "roll_no",
        "Name": "name",
        "DOB": "dob",
        "Email": "email",
        "Gender": "gender" }
    column = query_map.get(search_by)
    if not column:
        messagebox.showerror("Error", "Invalid search criterion.")
        return
    for row in tree.get_children():
        tree.delete(row)
    try:
        args = ('Search', None, None, None, None, None, None, None, column, search_query)
        results = execute_stored_procedure("ManageStudents", args)
        if results:
            for result in results:
                for row in result.fetchall():
                    tree.insert("", "end", values=row)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Event handlers for adding, updating, deleting, and searching students
def add_student():
    if not all([name_var.get(), roll_var.get(), email_var.get(), gender_var.get(), contact_var.get(), dob_entry.get(), address_text.get("1.0", "end-1c").strip()]):
        messagebox.showerror("Error", "All fields are required")
        return
    try:
        roll_no = int(roll_var.get())
    except ValueError:
        messagebox.showerror("Error", "Roll No must be an integer")
        return
    if not (validate_contact(contact_var.get())):
        messagebox.showerror("Error", "Contact No must be at least 10 digits")
        return
    if not validate_email(email_var.get()):
        messagebox.showerror("Error", "Invalid email format")
        return
    args = ('Add', name_var.get(), roll_no, email_var.get(), gender_var.get(), contact_var.get(), dob_entry.get(), address_text.get("1.0", "end-1c"), None, None)
    print(f"Calling stored procedure with args: {args}")  # Debugging output
    results = execute_stored_procedure("ManageStudents", args)
    print(f"Results from stored procedure: {results}")  # Debugging output
    messagebox.showinfo("Success", "Student added successfully")
    if results:
        messagebox.showinfo("Success", "Student added successfully")
        fetch_students()
        clear_fields()
        # messagebox.showinfo("Success", "Student added successfully")
    else:
        messagebox.showerror("Error", "Failed to add student")
def fetch_students():
    for row in tree.get_children():
        tree.delete(row)
    results = execute_stored_procedure("ManageStudents", ('GetAll', None, None, None, None, None, None, None, None, None))
    if results:
        for result in results:
            for row in result.fetchall():
                tree.insert("", "end", values=row)

def update_student():
    if not all([name_var.get(), roll_var.get(), email_var.get(), gender_var.get(), contact_var.get(), dob_entry.get(), address_text.get("1.0", "end-1c").strip()]):
        messagebox.showerror("Error", "No fields are selected")
        return
    if not validate_email(email_var.get()):
        messagebox.showerror("Error", "Invalid email format")
        return
    if not (contact_var.get().isdigit() and len(contact_var.get()) >= 10):
        messagebox.showerror("Error", "Contact No must be at least 10 digits")
        return
    args = ('Update', name_var.get(), int(roll_var.get()), email_var.get(), gender_var.get(), contact_var.get(), dob_entry.get(), address_text.get("1.0", "end-1c"), None, None)
    results = execute_stored_procedure("ManageStudents", args)
    if results:
        fetch_students()
        clear_fields()
        messagebox.showinfo("Success", "Student updated successfully")

def delete_student():
    try:
        args = ('Delete', None, int(roll_var.get()), None, None, None, None, None, None, None)
        results = execute_stored_procedure("ManageStudents", args)
        if results:
            fetch_students()
            clear_fields()
            messagebox.showinfo("Success", "Student deleted successfully")
    except ValueError:
        messagebox.showerror("Error", "No student selected")

# Main application setup
setup_database()
root = tk.Tk()
root.title("Student Management System")
root.state("zoomed")

# Clock Label
clock_label = tk.Label(root, font=("Arial", 14), bg="lightgray", fg="black")
clock_label.place(x=10, y=10)

# Title Label
title_label = tk.Label(root, text="STUDENT MANAGEMENT SYSTEM", font=("Times new roman", 24, "bold", "underline"), bg="lightgray", fg="black")
title_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

# Left Frame
left_frame = tk.Frame(root, padx=10, pady=10, bg="lightgray", relief=tk.RIDGE, bd=5)
left_frame.place(x=10, y=80, width=500, height=640)

left_title = tk.Label(left_frame, text="Manage Students", font=("Arial", 16, "bold", "underline"), bg="lightgray")
left_title.grid(row=0, column=0, columnspan=2, pady=10)

# Input Fields
fields = [
    ("Roll No:", roll_var := tk.StringVar()),
    ("Name:", name_var := tk.StringVar()),
    ("Email:", email_var := tk.StringVar()),
    ("Contact:", contact_var := tk.StringVar()),
]

for i, (label, var) in enumerate(fields):
    tk.Label(left_frame, text=label, font=("Arial", 12), bg="lightgray").grid(row=i + 1, column=0, sticky=tk.W, pady=5)

roll_entry = tk.Entry(left_frame, textvariable=roll_var, font=("Arial", 12))
roll_entry.grid(row=1, column=1, pady=5)

for i, (label, var) in enumerate(fields[1:], start=1):
    tk.Entry(left_frame, textvariable=var, font=("Arial", 12)).grid(row=i + 1, column=1, pady=5)

# Gender Dropdown
tk.Label(left_frame, text="Gender:", font=("Arial", 12), bg="lightgray").grid(row=5, column=0, sticky=tk.W, pady=5)
gender_var = tk.StringVar(value="Male")
gender_menu = ttk.Combobox(left_frame, textvariable=gender_var, values=["Male", "Female"], state="readonly", font=("Arial", 12))
gender_menu.grid(row=5, column=1, pady=5)

tk.Label(left_frame, text="D.O.B:", font=("Arial", 12), bg="lightgray").grid(row=6, column=0, sticky=tk.W, pady=5)
dob_entry = DateEntry(left_frame, font=("Arial", 12), date_pattern="yyyy-mm-dd")
dob_entry.set_date(datetime.now().date())
dob_entry.grid(row=6, column=1, pady=5)

# Address Field
tk.Label(left_frame, text="Address:", font=("Arial", 12), bg="lightgray").grid(row=7, column=0, sticky=tk.W, pady=5)
address_text = tk.Text(left_frame, width=25, height=4, font=("Arial", 12))
address_text.grid(row=7, column=1, pady=5)

# Buttons
buttons = [
    ("Add", add_student, "blue", "white"),
    ("Update", update_student, "blue", "white"),
    ("Delete", delete_student, "red", "Black"),
    ("Clear", clear_fields, "orange", "black"),]

for i, (text, cmd, bg, fg) in enumerate(buttons):
    tk.Button(left_frame, text=text, font=("Arial", 12), command=cmd, bg=bg, fg=fg).grid(row=8 + i // 2, column=i % 2, pady=10, padx=5)

# Right Frame
right_frame = tk.Frame(root, padx=10, pady=10, bg="lightblue", relief=tk.RIDGE, bd=5)
right_frame.place(x=520, y=80, width=1000, height=640)

right_title = tk.Label(right_frame, text="Search and Display Students", font=("Arial", 16, "bold", "underline"), bg="lightblue")
right_title.pack(pady=10)

# Search Section
search_frame = tk.Frame(right_frame, bg="lightblue")
search_frame.pack(pady=5)

search_var = tk.StringVar(value="Click here")
search_menu = ttk.Combobox(search_frame, textvariable=search_var, values=["Roll No", "Name", "DOB", "Email", "Gender"], state="readonly", font=("Arial", 12))
search_menu.grid(row=0, column=0, padx=5)

search_entry = tk.Entry(search_frame, font=("Arial", 12))
search_entry.grid(row=0, column=1, padx=5)

btn_search_all = tk.Button(search_frame, text="Search All", font=("Arial", 12), command=search_students, bg="purple", fg="white")
btn_search_all.grid(row=0, column=2, padx=5)

btn_show_all = tk.Button(right_frame, text="Show All", font=("Arial", 12), command=fetch_students, bg="green", fg="white")
btn_show_all.pack(pady=5)

columns = ("Name", "Roll No", "Email", "Gender", "Contact", "DOB", "Address")
tree = ttk.Treeview(right_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120, anchor=tk.CENTER)
tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Scrollbars
scroll_x = tk.Scrollbar(right_frame, orient="horizontal", command=tree.xview)
scroll_y = tk.Scrollbar(right_frame, orient="vertical", command=tree.yview)
tree.configure(xscrollcommand=scroll_x.set)
scroll_x.pack(side="bottom", fill="x")

# Bind treeview selection event
tree.bind("<<TreeviewSelect>>", on_tree_select)
fetch_students()