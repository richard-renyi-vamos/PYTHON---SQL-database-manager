import tkinter as tk
import sqlite3

def create_database():
    # Get the database name from the entry field
    db_name = entry.get()

    # Create a connection to the database
    conn = sqlite3.connect(db_name + ".db")

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Create a table (For example)
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        age INTEGER)''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    label_status.config(text="Database created successfully!")

# Create the main window
root = tk.Tk()
root.title("Create SQL Database")

# Label and Entry for database name
label = tk.Label(root, text="Enter database name:")
label.pack()
entry = tk.Entry(root)
entry.pack()

# Button to create the database
button_create = tk.Button(root, text="Create Database", command=create_database)
button_create.pack()

# Label for status message
label_status = tk.Label(root, text="")
label_status.pack()

# Run the main loop
root.mainloop()
