import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import date

from config import MYSQL_PASSWORD
# ================= DATABASE CONNECTION =================

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=MYSQL_PASSWORD,
        database="student_management"
    )


# ================= ATTENDANCE MANAGEMENT =================

def open_attendance():

    window = tk.Toplevel()
    window.title("Attendance Management")
    window.geometry("1000x650")
    window.resizable(False, False)

    student_id_var = tk.StringVar()
    date_var = tk.StringVar(value=str(date.today()))
    status_var = tk.StringVar(value="Present")
    search_var = tk.StringVar()

    # ================= TITLE =================

    tk.Label(
        window,
        text="Attendance Management",
        font=("Arial", 24, "bold")
    ).pack(pady=15)

    # ================= FORM =================

    form_frame = tk.Frame(window)
    form_frame.pack(pady=10)

    tk.Label(
        form_frame,
        text="Student ID",
        font=("Arial", 11)
    ).grid(row=0, column=0, padx=10, pady=8)

    tk.Entry(
        form_frame,
        textvariable=student_id_var,
        width=25
    ).grid(row=0, column=1, padx=10)

    tk.Label(
        form_frame,
        text="Date (YYYY-MM-DD)",
        font=("Arial", 11)
    ).grid(row=1, column=0, padx=10, pady=8)

    tk.Entry(
        form_frame,
        textvariable=date_var,
        width=25
    ).grid(row=1, column=1, padx=10)

    tk.Label(
        form_frame,
        text="Status",
        font=("Arial", 11)
    ).grid(row=2, column=0, padx=10, pady=8)

    status_box = ttk.Combobox(
        form_frame,
        textvariable=status_var,
        values=("Present", "Absent"),
        state="readonly",
        width=22
    )
    status_box.grid(row=2, column=1, padx=10)

    # ================= TABLE =================

    table_frame = tk.Frame(window)
    table_frame.pack(pady=15)

    columns = (
        "ID",
        "Student ID",
        "Date",
        "Status"
    )

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=12
    )

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=170)

    tree.pack(side="left")

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )

    scrollbar.pack(side="right", fill="y")

    tree.configure(
        yscrollcommand=scrollbar.set
    )

    # ================= FUNCTIONS =================

    def load_attendance():

        for item in tree.get_children():
            tree.delete(item)

        try:
            conn = create_connection()
            cursor = conn.cursor()

            query = """
                SELECT id, student_id, attendance_date, status
                FROM attendance
                ORDER BY attendance_date DESC, id DESC
            """

            cursor.execute(query)

            records = cursor.fetchall()

            for record in records:
                tree.insert("", "end", values=record)

            cursor.close()
            conn.close()

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    def add_attendance():

        student_id = student_id_var.get().strip()
        attendance_date = date_var.get().strip()
        status = status_var.get().strip()

        if student_id == "" or attendance_date == "":
            messagebox.showwarning(
                "Warning",
                "Please fill all fields"
            )
            return

        try:
            student_id = int(student_id)

        except ValueError:
            messagebox.showwarning(
                "Warning",
                "Student ID must be a number"
            )
            return

        try:
            conn = create_connection()
            cursor = conn.cursor()

            # Check whether student exists
            cursor.execute(
                "SELECT id FROM students WHERE id=%s",
                (student_id,)
            )

            student = cursor.fetchone()

            if not student:
                messagebox.showerror(
                    "Error",
                    "Student ID does not exist"
                )
                cursor.close()
                conn.close()
                return

            query = """
                INSERT INTO attendance
                (student_id, attendance_date, status)
                VALUES (%s, %s, %s)
            """

            cursor.execute(
                query,
                (student_id, attendance_date, status)
            )

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Attendance added successfully!"
            )

            clear_fields()
            load_attendance()

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    def update_attendance():

        selected = tree.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select an attendance record"
            )
            return

        item = tree.item(selected[0])
        record_id = item["values"][0]

        student_id = student_id_var.get().strip()
        attendance_date = date_var.get().strip()
        status = status_var.get().strip()

        if student_id == "" or attendance_date == "":
            messagebox.showwarning(
                "Warning",
                "Please fill all fields"
            )
            return

        try:
            student_id = int(student_id)

        except ValueError:
            messagebox.showwarning(
                "Warning",
                "Student ID must be a number"
            )
            return

        try:
            conn = create_connection()
            cursor = conn.cursor()

            query = """
                UPDATE attendance
                SET student_id=%s,
                    attendance_date=%s,
                    status=%s
                WHERE id=%s
            """

            cursor.execute(
                query,
                (
                    student_id,
                    attendance_date,
                    status,
                    record_id
                )
            )

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Attendance updated successfully!"
            )

            clear_fields()
            load_attendance()

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    def delete_attendance():

        selected = tree.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select a record first"
            )
            return

        item = tree.item(selected[0])
        record_id = item["values"][0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this attendance record?"
        )

        if not confirm:
            return

        try:
            conn = create_connection()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM attendance WHERE id=%s",
                (record_id,)
            )

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Attendance deleted successfully!"
            )

            clear_fields()
            load_attendance()

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    def search_attendance():

        search = search_var.get().strip()

        for item in tree.get_children():
            tree.delete(item)

        try:
            conn = create_connection()
            cursor = conn.cursor()

            query = """
                SELECT id, student_id, attendance_date, status
                FROM attendance
                WHERE CAST(student_id AS CHAR) LIKE %s
                OR status LIKE %s
                OR attendance_date LIKE %s
                ORDER BY attendance_date DESC
            """

            value = "%" + search + "%"

            cursor.execute(
                query,
                (value, value, value)
            )

            records = cursor.fetchall()

            for record in records:
                tree.insert("", "end", values=record)

            cursor.close()
            conn.close()

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    def clear_fields():

        student_id_var.set("")
        date_var.set(str(date.today()))
        status_var.set("Present")

        for item in tree.selection():
            tree.selection_remove(item)

    def select_record(event):

        selected = tree.selection()

        if not selected:
            return

        item = tree.item(selected[0])
        values = item["values"]

        student_id_var.set(values[1])
        date_var.set(values[2])
        status_var.set(values[3])

    # ================= BUTTONS =================

    button_frame = tk.Frame(window)
    button_frame.pack(pady=5)

    tk.Button(
        button_frame,
        text="Add Attendance",
        width=15,
        command=add_attendance
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        button_frame,
        text="Update",
        width=15,
        command=update_attendance
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        button_frame,
        text="Delete",
        width=15,
        command=delete_attendance
    ).grid(row=0, column=2, padx=5)

    tk.Button(
        button_frame,
        text="Clear",
        width=15,
        command=clear_fields
    ).grid(row=0, column=3, padx=5)

    # ================= SEARCH =================

    search_frame = tk.Frame(window)
    search_frame.pack(pady=15)

    tk.Label(
        search_frame,
        text="Search:",
        font=("Arial", 11)
    ).pack(side="left", padx=5)

    tk.Entry(
        search_frame,
        textvariable=search_var,
        width=30
    ).pack(side="left", padx=5)

    tk.Button(
        search_frame,
        text="Search",
        width=12,
        command=search_attendance
    ).pack(side="left", padx=5)

    tk.Button(
        search_frame,
        text="Show All",
        width=12,
        command=load_attendance
    ).pack(side="left", padx=5)

    tree.bind(
        "<ButtonRelease-1>",
        select_record
    )

    load_attendance()


# ================= TEST =================

if __name__ == "__main__":

    root = tk.Tk()
    root.withdraw()

    open_attendance()

    root.mainloop()