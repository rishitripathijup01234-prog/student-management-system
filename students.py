import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
import csv

from config import MYSQL_PASSWORD
# =========================================================
# DATABASE CONNECTION
# =========================================================

def create_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="student_management"
    )
    return connection


# =========================================================
# OPEN STUDENT MANAGEMENT WINDOW
# =========================================================

def open_students():

    window = tk.Toplevel()
    window.title("Student Management")
    window.geometry("1100x700")
    window.resizable(False, False)

    # =====================================================
    # TITLE
    # =====================================================

    title = tk.Label(
        window,
        text="Student Management System",
        font=("Arial", 24, "bold")
    )
    title.pack(pady=15)

    subtitle = tk.Label(
        window,
        text="Add, Update, Delete, Search and Manage Students",
        font=("Arial", 11)
    )
    subtitle.pack(pady=5)

    # =====================================================
    # FORM FRAME
    # =====================================================

    form_frame = tk.LabelFrame(
        window,
        text="Student Information",
        font=("Arial", 12, "bold"),
        padx=15,
        pady=15
    )
    form_frame.pack(
        fill="x",
        padx=20,
        pady=15
    )

    # =====================================================
    # VARIABLES
    # =====================================================

    student_id_var = tk.StringVar()
    name_var = tk.StringVar()
    email_var = tk.StringVar()
    phone_var = tk.StringVar()
    gender_var = tk.StringVar()
    course_var = tk.StringVar()
    semester_var = tk.StringVar()

    # =====================================================
    # LABELS AND ENTRY FIELDS
    # =====================================================

    tk.Label(
        form_frame,
        text="Student ID"
    ).grid(row=0, column=0, padx=10, pady=8, sticky="w")

    student_id_entry = tk.Entry(
        form_frame,
        textvariable=student_id_var,
        width=30
    )
    student_id_entry.grid(
        row=0,
        column=1,
        padx=10,
        pady=8
    )

    tk.Label(
        form_frame,
        text="Name"
    ).grid(row=0, column=2, padx=10, pady=8, sticky="w")

    name_entry = tk.Entry(
        form_frame,
        textvariable=name_var,
        width=30
    )
    name_entry.grid(
        row=0,
        column=3,
        padx=10,
        pady=8
    )

    tk.Label(
        form_frame,
        text="Email"
    ).grid(row=1, column=0, padx=10, pady=8, sticky="w")

    email_entry = tk.Entry(
        form_frame,
        textvariable=email_var,
        width=30
    )
    email_entry.grid(
        row=1,
        column=1,
        padx=10,
        pady=8
    )

    tk.Label(
        form_frame,
        text="Phone"
    ).grid(row=1, column=2, padx=10, pady=8, sticky="w")

    phone_entry = tk.Entry(
        form_frame,
        textvariable=phone_var,
        width=30
    )
    phone_entry.grid(
        row=1,
        column=3,
        padx=10,
        pady=8
    )

    tk.Label(
        form_frame,
        text="Gender"
    ).grid(row=2, column=0, padx=10, pady=8, sticky="w")

    gender_combo = ttk.Combobox(
        form_frame,
        textvariable=gender_var,
        values=["Male", "Female", "Other"],
        state="readonly",
        width=27
    )
    gender_combo.grid(
        row=2,
        column=1,
        padx=10,
        pady=8
    )

    tk.Label(
        form_frame,
        text="Course"
    ).grid(row=2, column=2, padx=10, pady=8, sticky="w")

    course_entry = tk.Entry(
        form_frame,
        textvariable=course_var,
        width=30
    )
    course_entry.grid(
        row=2,
        column=3,
        padx=10,
        pady=8
    )

    tk.Label(
        form_frame,
        text="Semester"
    ).grid(row=3, column=0, padx=10, pady=8, sticky="w")

    semester_combo = ttk.Combobox(
        form_frame,
        textvariable=semester_var,
        values=["1", "2", "3", "4", "5", "6"],
        state="readonly",
        width=27
    )
    semester_combo.grid(
        row=3,
        column=1,
        padx=10,
        pady=8
    )

    # =====================================================
    # CLEAR FUNCTION
    # =====================================================

    def clear_fields():

        student_id_var.set("")
        name_var.set("")
        email_var.set("")
        phone_var.set("")
        gender_var.set("")
        course_var.set("")
        semester_var.set("")

        student_id_entry.focus()

    # =====================================================
    # LOAD STUDENTS
    # =====================================================

    def load_students():

        for item in tree.get_children():
            tree.delete(item)

        try:
            conn = create_connection()
            cursor = conn.cursor()

            query = """
                SELECT id, name, email, phone, gender, course, semester
                FROM students
                ORDER BY id
            """

            cursor.execute(query)

            records = cursor.fetchall()

            for record in records:
                tree.insert(
                    "",
                    tk.END,
                    values=record
                )

            cursor.close()
            conn.close()

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    # =====================================================
    # ADD STUDENT
    # =====================================================

    def add_student():

        name = name_var.get().strip()
        email = email_var.get().strip()
        phone = phone_var.get().strip()
        gender = gender_var.get().strip()
        course = course_var.get().strip()
        semester = semester_var.get().strip()

        if name == "":
            messagebox.showwarning(
                "Warning",
                "Please enter student name."
            )
            return

        if course == "":
            messagebox.showwarning(
                "Warning",
                "Please enter course."
            )
            return

        if semester == "":
            messagebox.showwarning(
                "Warning",
                "Please select semester."
            )
            return

        try:
            semester_number = int(semester)

        except ValueError:
            messagebox.showwarning(
                "Warning",
                "Semester must be a number."
            )
            return

        try:
            conn = create_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO students
                (name, email, phone, gender, course, semester)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            values = (
                name,
                email,
                phone,
                gender,
                course,
                semester_number
            )

            cursor.execute(query, values)

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Student added successfully!"
            )

            clear_fields()
            load_students()

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    # =====================================================
    # UPDATE STUDENT
    # =====================================================

    def update_student():

        student_id = student_id_var.get().strip()

        if student_id == "":
            messagebox.showwarning(
                "Warning",
                "Please select a student first."
            )
            return

        name = name_var.get().strip()
        email = email_var.get().strip()
        phone = phone_var.get().strip()
        gender = gender_var.get().strip()
        course = course_var.get().strip()
        semester = semester_var.get().strip()

        if name == "":
            messagebox.showwarning(
                "Warning",
                "Please enter student name."
            )
            return

        if course == "":
            messagebox.showwarning(
                "Warning",
                "Please enter course."
            )
            return

        if semester == "":
            messagebox.showwarning(
                "Warning",
                "Please select semester."
            )
            return

        try:
            student_id_number = int(student_id)
            semester_number = int(semester)

        except ValueError:
            messagebox.showwarning(
                "Warning",
                "Student ID and Semester must be numbers."
            )
            return

        try:
            conn = create_connection()
            cursor = conn.cursor()

            query = """
                UPDATE students
                SET name=%s,
                    email=%s,
                    phone=%s,
                    gender=%s,
                    course=%s,
                    semester=%s
                WHERE id=%s
            """

            values = (
                name,
                email,
                phone,
                gender,
                course,
                semester_number,
                student_id_number
            )

            cursor.execute(query, values)

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Student updated successfully!"
            )

            clear_fields()
            load_students()

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    # =====================================================
    # DELETE STUDENT
    # =====================================================

    def delete_student():

        student_id = student_id_var.get().strip()

        if student_id == "":
            messagebox.showwarning(
                "Warning",
                "Please select a student first."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this student?"
        )

        if not confirm:
            return

        try:
            student_id_number = int(student_id)

        except ValueError:
            messagebox.showwarning(
                "Warning",
                "Invalid Student ID."
            )
            return

        try:
            conn = create_connection()
            cursor = conn.cursor()

            query = "DELETE FROM students WHERE id=%s"

            cursor.execute(
                query,
                (student_id_number,)
            )

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Student deleted successfully!"
            )

            clear_fields()
            load_students()

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    # =====================================================
    # SEARCH STUDENT
    # =====================================================

    def search_student():

        search_text = search_var.get().strip()

        if search_text == "":
            load_students()
            return

        for item in tree.get_children():
            tree.delete(item)

        try:
            conn = create_connection()
            cursor = conn.cursor()

            query = """
                SELECT id, name, email, phone, gender, course, semester
                FROM students
                WHERE name LIKE %s
                   OR email LIKE %s
                   OR phone LIKE %s
                   OR course LIKE %s
                   OR id LIKE %s
                ORDER BY id
            """

            search_value = "%" + search_text + "%"

            values = (
                search_value,
                search_value,
                search_value,
                search_value,
                search_value
            )

            cursor.execute(
                query,
                values
            )

            records = cursor.fetchall()

            for record in records:

                tree.insert(
                    "",
                    tk.END,
                    values=record
                )

            cursor.close()
            conn.close()

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    # =====================================================
    # IMPORT STUDENTS FROM CSV
    # =====================================================

    def import_students():

        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[
                ("CSV Files", "*.csv"),
                ("All Files", "*.*")
            ]
        )

        if file_path == "":
            return

        try:

            with open(
                file_path,
                "r",
                newline="",
                encoding="utf-8-sig"
            ) as file:

                reader = csv.DictReader(file)

                required_columns = [
                    "Name",
                    "Email",
                    "Phone",
                    "Gender",
                    "Course",
                    "Semester"
                ]

                if reader.fieldnames is None:

                    messagebox.showerror(
                        "Error",
                        "CSV file is empty or invalid."
                    )
                    return

                missing_columns = [
                    column
                    for column in required_columns
                    if column not in reader.fieldnames
                ]

                if missing_columns:

                    messagebox.showerror(
                        "Error",
                        "Missing columns: "
                        + ", ".join(missing_columns)
                    )
                    return

                students_data = []

                for row in reader:

                    name = row["Name"].strip()
                    email = row["Email"].strip()
                    phone = row["Phone"].strip()
                    gender = row["Gender"].strip()
                    course = row["Course"].strip()
                    semester = row["Semester"].strip()

                    if (
                        name == ""
                        or course == ""
                        or semester == ""
                    ):
                        continue

                    try:
                        semester_number = int(semester)

                    except ValueError:
                        continue

                    students_data.append(
                        (
                            name,
                            email,
                            phone,
                            gender,
                            course,
                            semester_number
                        )
                    )

            if len(students_data) == 0:

                messagebox.showwarning(
                    "Warning",
                    "No valid student records found."
                )
                return

            conn = create_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO students
                (name, email, phone, gender, course, semester)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            cursor.executemany(
                query,
                students_data
            )

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                str(len(students_data))
                + " students imported successfully!"
            )

            load_students()

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # =====================================================
    # SELECT STUDENT FROM TABLE
    # =====================================================

    def select_student(event):

        selected = tree.focus()

        if selected == "":
            return

        values = tree.item(
            selected,
            "values"
        )

        if not values:
            return

        student_id_var.set(values[0])
        name_var.set(values[1])
        email_var.set(values[2])
        phone_var.set(values[3])
        gender_var.set(values[4])
        course_var.set(values[5])
        semester_var.set(values[6])

    # =====================================================
    # BUTTON FRAME
    # =====================================================

    button_frame = tk.Frame(window)
    button_frame.pack(pady=5)

    tk.Button(
        button_frame,
        text="Add Student",
        width=15,
        command=add_student
    ).grid(
        row=0,
        column=0,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Update",
        width=15,
        command=update_student
    ).grid(
        row=0,
        column=1,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Delete",
        width=15,
        command=delete_student
    ).grid(
        row=0,
        column=2,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Clear",
        width=15,
        command=clear_fields
    ).grid(
        row=0,
        column=3,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Import CSV",
        width=15,
        command=import_students
    ).grid(
        row=0,
        column=4,
        padx=5
    )

    # =====================================================
    # SEARCH FRAME
    # =====================================================

    search_frame = tk.Frame(window)
    search_frame.pack(
        fill="x",
        padx=20,
        pady=10
    )

    search_var = tk.StringVar()

    tk.Label(
        search_frame,
        text="Search Student:",
        font=("Arial", 11, "bold")
    ).pack(
        side="left",
        padx=5
    )

    search_entry = tk.Entry(
        search_frame,
        textvariable=search_var,
        width=40
    )
    search_entry.pack(
        side="left",
        padx=5
    )

    tk.Button(
        search_frame,
        text="Search",
        width=12,
        command=search_student
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        search_frame,
        text="Show All",
        width=12,
        command=load_students
    ).pack(
        side="left",
        padx=5
    )

    # =====================================================
    # TABLE FRAME
    # =====================================================

    table_frame = tk.Frame(window)
    table_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    # =====================================================
    # SCROLLBARS
    # =====================================================

    vertical_scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical"
    )

    horizontal_scrollbar = ttk.Scrollbar(
        table_frame,
        orient="horizontal"
    )

    # =====================================================
    # TREEVIEW
    # =====================================================

    columns = (
        "ID",
        "Name",
        "Email",
        "Phone",
        "Gender",
        "Course",
        "Semester"
    )

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        yscrollcommand=vertical_scrollbar.set,
        xscrollcommand=horizontal_scrollbar.set
    )

    vertical_scrollbar.config(
        command=tree.yview
    )

    horizontal_scrollbar.config(
        command=tree.xview
    )

    # =====================================================
    # COLUMN HEADINGS
    # =====================================================

    for column in columns:

        tree.heading(
            column,
            text=column
        )

    # =====================================================
    # COLUMN WIDTHS
    # =====================================================

    tree.column(
        "ID",
        width=60,
        anchor="center"
    )

    tree.column(
        "Name",
        width=180
    )

    tree.column(
        "Email",
        width=220
    )

    tree.column(
        "Phone",
        width=130
    )

    tree.column(
        "Gender",
        width=100,
        anchor="center"
    )

    tree.column(
        "Course",
        width=120,
        anchor="center"
    )

    tree.column(
        "Semester",
        width=100,
        anchor="center"
    )

    # =====================================================
    # PACK TABLE
    # =====================================================

    tree.pack(
        side="left",
        fill="both",
        expand=True
    )

    vertical_scrollbar.pack(
        side="right",
        fill="y"
    )

    horizontal_scrollbar.pack(
        side="bottom",
        fill="x"
    )

    # =====================================================
    # SELECT EVENT
    # =====================================================

    tree.bind(
        "<ButtonRelease-1>",
        select_student
    )

    # =====================================================
    # LOAD DATA WHEN WINDOW OPENS
    # =====================================================

    load_students()


# =========================================================
# TEST STUDENT MANAGEMENT
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()
    root.withdraw()

    open_students()

    root.mainloop()