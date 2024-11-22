import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

def create_connection(db_name):
    """Create a database connection."""
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error connecting to database: {e}")
    return conn

def create_table(conn):
    """Create a table in the database."""
    try:
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            email TEXT UNIQUE
        );
        """
        conn.execute(sql)
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error creating table: {e}")

def insert_record(conn, name, age, email):
    """Insert a new record."""
    try:
        sql = "INSERT INTO users (name, age, email) VALUES (?, ?, ?)"
        conn.execute(sql, (name, age, email))
        conn.commit()
        messagebox.showinfo("Success", f"User {name} added successfully!")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error inserting record: {e}")

def fetch_records(conn):
    """Fetch all records."""
    try:
        sql = "SELECT * FROM users"
        cursor = conn.execute(sql)
        return cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error reading records: {e}")
        return []

def update_record(conn, user_id, name, age, email):
    """Update a record."""
    try:
        sql = "UPDATE users SET name = ?, age = ?, email = ? WHERE id = ?"
        conn.execute(sql, (name, age, email, user_id))
        conn.commit()
        messagebox.showinfo("Success", f"User with ID {user_id} updated successfully!")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error updating record: {e}")

def delete_record(conn, user_id):
    """Delete a record."""
    try:
        sql = "DELETE FROM users WHERE id = ?"
        conn.execute(sql, (user_id,))
        conn.commit()
        messagebox.showinfo("Success", f"User with ID {user_id} deleted successfully!")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error deleting record: {e}")

# GUI Functions
def add_user():
    """Add user to database."""
    name = entry_name.get()
    age = entry_age.get()
    email = entry_email.get()
    if name and age.isdigit() and email:
        insert_record(conn, name, int(age), email)
        refresh_table()
    else:
        messagebox.showwarning("Invalid Input", "Please provide valid name, age, and email.")

def refresh_table():
    """Refresh the user table in the GUI."""
    for row in tree.get_children():
        tree.delete(row)
    for record in fetch_records(conn):
        tree.insert("", tk.END, values=record)

def edit_user():
    """Edit selected user."""
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a user to edit.")
        return
    values = tree.item(selected, "values")
    user_id = values[0]
    name = entry_name.get()
    age = entry_age.get()
    email = entry_email.get()
    if name and age.isdigit() and email:
        update_record(conn, user_id, name, int(age), email)
        refresh_table()
    else:
        messagebox.showwarning("Invalid Input", "Please provide valid name, age, and email.")

def delete_user():
    """Delete selected user."""
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a user to delete.")
        return
    values = tree.item(selected, "values")
    user_id = values[0]
    delete_record(conn, user_id)
    refresh_table()

# Main Program
conn = create_connection("example.db")
if conn:
    create_table(conn)

# GUI Setup
root = tk.Tk()
root.title("Database Manager")

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

tk.Label(frame_top, text="Name:").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(frame_top)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_top, text="Age:").grid(row=1, column=0, padx=5, pady=5)
entry_age = tk.Entry(frame_top)
entry_age.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_top, text="Email:").grid(row=2, column=0, padx=5, pady=5)
entry_email = tk.Entry(frame_top)
entry_email.grid(row=2, column=1, padx=5, pady=5)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Add User", command=add_user).grid(row=0, column=0, padx=10)
tk.Button(frame_buttons, text="Edit User", command=edit_user).grid(row=0, column=1, padx=10)
tk.Button(frame_buttons, text="Delete User", command=delete_user).grid(row=0, column=2, padx=10)

frame_table = tk.Frame(root)
frame_table.pack(pady=10)

tree = ttk.Treeview(frame_table, columns=("ID", "Name", "Age", "Email"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Email", text="Email")
tree.column("ID", width=50)
tree.column("Name", width=150)
tree.column("Age", width=50)
tree.column("Email", width=200)
tree.pack()

refresh_table()

root.mainloop()
