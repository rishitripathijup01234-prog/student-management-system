import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

from config import MYSQL_PASSWORD
# ================= DATABASE CONNECTION =================

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=MYSQL_PASSWORD,
        database="student_management"
    )


# ================= MARKS MANAGEMENT =================

def open_marks():

    window = tk.Toplevel()
    window.title("Marks Management")
    window.geometry("1000x650")
    window.resizable(False, False)

    # ---------- Variables ----------
    student_id_var = tk.StringVar()
    subject_var = tk.StringVar()
    marks_var = tk.StringVar()
    search_var = tk.StringVar()

    # ---------- Title ----------
    tk.Label(
        window,
        text="Marks Management",
        font=("Arial", 24, "bold")
    ).pack(pady=15)

    # ---------- Form ----------
    form_frame = tk.Frame(window)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Student ID", font=("Arial", 11)).grid(
        row=0, column=0, padx=10, pady=8
    )

    student_entry = tk.Entry(
        form_frame,
        textvariable=student_id_var,
        width=25
    )
    student_entry.grid(row=0, column=1, padx=10)

    tk.Label(form_frame, text="Subject", font=("Arial", 11)).grid(
        row=1, column=0, padx=10, pady=8
    )

    subject_entry = tk.Entry(
        form_frame,
        textvariable=subject_var,
        width=25
    )
    subject_entry.grid(row=1, column=1, padx=10)

    tk.Label(form_frame, text="Marks", font=("Arial", 11)).grid(
        row=2, column=0, padx=10, pady=8
    )

    marks_entry = tk.Entry(
        form_frame,
        textvariable=marks_var,
        width=25
    )
    marks_entry.grid(row=2, column=1, padx=10)

    # ---------- Table ----------
    table_frame = tk.Frame(window)
    table_frame.pack(pady=15)

    columns = (
        "ID",
        "Student ID",
        "Subject",
        "Marks"
    )

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=12
    )

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    tree.pack(side="left")

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )

    scrollbar.pack(side="right", fill="y")

    tree.configure(yscrollcommand=scrollbar.set)

    # ================= FUNCTIONS =================

    def load_marks():

        for item in tree.get_children():
            tree.delete(item)

        try:
            conn = create_connection()
            cursor = conn.cursor()

            query = """
                SELECT id, student_id, subject, marks
                FROM marks
                ORDER BY id DESC
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

    def add_marks():

        student_id = student_id_var.get().strip()
        subject = subject_var.get().strip()
        marks = marks_var.get().strip()

        if student_id == "" or subject == "" or marks == "":
            messagebox.showwarning(
                "Warning",
                "Please fill all fields"
            )
            return

        try:
            student_id = int(student_id)
            marks = int(marks)

            if marks < 0 or marks > 100:
                messagebox.showwarning(
                    "Warning",
                    "Marks must be between 0 and 100"
                )
                return

        except ValueError:
            messagebox.showwarning(
                "Warning",
                "Student ID and Marks must be numbers"
            )
            return

        try:
            conn = create_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO marks
                (student_id, subject, marks)
                VALUES (%s, %s, %s)
            """

            cursor.execute(
                query,
                (student_id, subject, marks)
            )

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Marks added successfully!"
            )

            clear_fields()
            load_marks()

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    def update_marks():

        selected = tree.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select a record first"
            )
            return

        item = tree.item(selected[0])
        record_id = item["values"][0]

        student_id = student_id_var.get().strip()
        subject = subject_var.get().strip()
        marks = marks_var.get().strip()

        if student_id == "" or subject == "" or marks == "":
            messagebox.showwarning(
                "Warning",
                "Please fill all fields"
            )
            return

        try:
            student_id = int(student_id)
            marks = int(marks)

            if marks < 0 or marks > 100:
                messagebox.showwarning(
                    "Warning",
                    "Marks must be between 0 and 100"
                )
                return

        except ValueError:
            messagebox.showwarning(
                "Warning",
                "Student ID and Marks must be numbers"
            )
            return

        try:
            conn = create_connection()
            cursor = conn.cursor()

            query = """
                UPDATE marks
                SET student_id=%s,
                    subject=%s,
                    marks=%s
                WHERE id=%s
            """

            cursor.execute(
                query,
                (student_id, subject, marks, record_id)
            )

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Marks updated successfully!"
            )

            clear_fields()
            load_marks()

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    def delete_marks():

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
            "Are you sure you want to delete this marks record?"
        )

        if not confirm:
            return

        try:
            conn = create_connection()
            cursor = conn.cursor()

            query = "DELETE FROM marks WHERE id=%s"

            cursor.execute(
                query,
                (record_id,)
            )

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Marks deleted successfully!"
            )

            clear_fields()
            load_marks()

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    def search_marks():

        search = search_var.get().strip()

        for item in tree.get_children():
            tree.delete(item)

        try:
            conn = create_connection()
            cursor = conn.cursor()

            query = """
                SELECT id, student_id, subject, marks
                FROM marks
                WHERE student_id LIKE %s
                OR subject LIKE %s
                ORDER BY id DESC
            """

            value = "%" + search + "%"

            cursor.execute(
                query,
                (value, value)
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
        subject_var.set("")
        marks_var.set("")

        for item in tree.selection():
            tree.selection_remove(item)

    def select_record(event):

        selected = tree.selection()

        if not selected:
            return

        item = tree.item(selected[0])
        values = item["values"]

        student_id_var.set(values[1])
        subject_var.set(values[2])
        marks_var.set(values[3])

    # ================= BUTTONS =================

    button_frame = tk.Frame(window)
    button_frame.pack(pady=5)

    tk.Button(
        button_frame,
        text="Add Marks",
        width=15,
        command=add_marks
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        button_frame,
        text="Update",
        width=15,
        command=update_marks
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        button_frame,
        text="Delete",
        width=15,
        command=delete_marks
    ).grid(row=0, column=2, padx=5)

    tk.Button(
        button_frame,
        text="Clear",
        width=15,
        command=clear_fields
    ).grid(row=0, column=3, padx=5)

    # ---------- Search ----------

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
        command=search_marks
    ).pack(side="left", padx=5)

    tk.Button(
        search_frame,
        text="Show All",
        width=12,
        command=load_marks
    ).pack(side="left", padx=5)

    # ---------- Select Event ----------

    tree.bind(
        "<ButtonRelease-1>",
        select_record
    )

    # ---------- Initial Load ----------

    load_marks()


# ================= TEST =================

if __name__ == "__main__":

    root = tk.Tk()
    root.withdraw()

    open_marks()

    root.mainloop()