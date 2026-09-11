import tkinter as tk
from tkinter import messagebox
import mysql.connector

from config import MYSQL_PASSWORD
def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "" or password == "":
        messagebox.showwarning(
            "Warning",
            "Please enter username and password"
        )
        return

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=MYSQL_PASSWORD,
            database="student_management"
        )

        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        cursor.execute(query, (username, password))

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            messagebox.showinfo("Success", "Login Successful!")

            # Close login window
            root.destroy()

            # Open dashboard
            import dashboard
            dashboard.root = tk.Tk()
            dashboard.root.withdraw()
            dashboard.open_dashboard()
            dashboard.root.mainloop()

        else:
            messagebox.showerror(
                "Error",
                "Invalid username or password"
            )

    except mysql.connector.Error as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )


# Main Login Window
root = tk.Tk()
root.title("Student Management System - Login")
root.geometry("400x300")
root.resizable(False, False)

title = tk.Label(
    root,
    text="Student Management System",
    font=("Arial", 18, "bold")
)
title.pack(pady=30)

username_label = tk.Label(
    root,
    text="Username"
)
username_label.pack()

username_entry = tk.Entry(
    root,
    width=30
)
username_entry.pack(pady=5)

password_label = tk.Label(
    root,
    text="Password"
)
password_label.pack()

password_entry = tk.Entry(
    root,
    width=30,
    show="*"
)
password_entry.pack(pady=5)

login_button = tk.Button(
    root,
    text="Login",
    width=15,
    command=login
)
login_button.pack(pady=20)

root.mainloop()