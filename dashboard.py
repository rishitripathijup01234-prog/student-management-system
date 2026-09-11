import tkinter as tk
from tkinter import messagebox


def open_dashboard():

    dashboard = tk.Toplevel()
    dashboard.title("Student Management System - Dashboard")
    dashboard.geometry("900x600")
    dashboard.resizable(False, False)

    # ================= HEADER =================

    header = tk.Frame(dashboard, height=80)
    header.pack(fill="x")

    title = tk.Label(
        header,
        text="Student Management System",
        font=("Arial", 24, "bold")
    )
    title.pack(pady=20)

    # ================= WELCOME =================

    welcome = tk.Label(
        dashboard,
        text="Welcome to Dashboard",
        font=("Arial", 18, "bold")
    )
    welcome.pack(pady=25)

    # ================= BUTTON FRAME =================

    button_frame = tk.Frame(dashboard)
    button_frame.pack(pady=10)

    # ================= STUDENT MANAGEMENT =================

    def students():
        import students as students_module
        students_module.open_students()

    # ================= MARKS =================

    def marks():
        import marks as marks_module
        marks_module.open_marks()

    # ================= ATTENDANCE =================

    def attendance():
        import attendance as attendance_module
        attendance_module.open_attendance()

    # ================= REPORTS =================

    def reports():
        import reports as reports_module
        reports_module.open_reports()

    # ================= LOGOUT =================

    def logout():
        dashboard.destroy()

    # ================= BUTTONS =================

    student_button = tk.Button(
        button_frame,
        text="Student Management",
        width=25,
        height=2,
        command=students
    )
    student_button.grid(
        row=0,
        column=0,
        padx=15,
        pady=15
    )

    marks_button = tk.Button(
        button_frame,
        text="Marks",
        width=25,
        height=2,
        command=marks
    )
    marks_button.grid(
        row=0,
        column=1,
        padx=15,
        pady=15
    )

    attendance_button = tk.Button(
        button_frame,
        text="Attendance",
        width=25,
        height=2,
        command=attendance
    )
    attendance_button.grid(
        row=1,
        column=0,
        padx=15,
        pady=15
    )

    reports_button = tk.Button(
        button_frame,
        text="Reports",
        width=25,
        height=2,
        command=reports
    )
    reports_button.grid(
        row=1,
        column=1,
        padx=15,
        pady=15
    )

    # ================= LOGOUT BUTTON =================

    logout_button = tk.Button(
        dashboard,
        text="Logout",
        width=20,
        height=2,
        command=logout
    )
    logout_button.pack(pady=35)


# ================= TEST DASHBOARD =================

if __name__ == "__main__":

    root = tk.Tk()
    root.withdraw()

    open_dashboard()

    root.mainloop()