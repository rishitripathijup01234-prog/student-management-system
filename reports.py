import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from config import MYSQL_PASSWORD

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=MYSQL_PASSWORD,
        database="student_management"
    )


def open_reports():

    window = tk.Toplevel()
    window.title("Student Management System - Reports")
    window.geometry("1000x650")
    window.resizable(False, False)

    # Title
    title = tk.Label(
        window,
        text="Student Reports",
        font=("Arial", 24, "bold")
    )
    title.pack(pady=20)

    # Search Frame
    search_frame = tk.Frame(window)
    search_frame.pack(pady=10)

    tk.Label(
        search_frame,
        text="Student ID:",
        font=("Arial", 12)
    ).grid(row=0, column=0, padx=10)

    student_id_entry = tk.Entry(
        search_frame,
        width=20,
        font=("Arial", 12)
    )
    student_id_entry.grid(row=0, column=1, padx=10)

    # Report Text
    report_text = tk.Text(
        window,
        width=90,
        height=25,
        font=("Arial", 11)
    )
    report_text.pack(pady=20)

    def generate_report():

        student_id = student_id_entry.get().strip()

        if student_id == "":
            messagebox.showwarning(
                "Warning",
                "Please enter Student ID"
            )
            return

        try:
            student_id = int(student_id)

            conn = create_connection()
            cursor = conn.cursor()

            # Student Details
            cursor.execute(
                """
                SELECT id, name, email, phone, gender, course, semester
                FROM students
                WHERE id = %s
                """,
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

            # Marks
            cursor.execute(
                """
                SELECT subject, marks
                FROM marks
                WHERE student_id = %s
                """,
                (student_id,)
            )

            marks_data = cursor.fetchall()

            # Attendance
            cursor.execute(
                """
                SELECT attendance_date, status
                FROM attendance
                WHERE student_id = %s
                ORDER BY attendance_date
                """,
                (student_id,)
            )

            attendance_data = cursor.fetchall()

            cursor.close()
            conn.close()

            # Clear old report
            report_text.delete("1.0", tk.END)

            # Student Details
            report_text.insert(
                tk.END,
                "========== STUDENT REPORT ==========\n\n"
            )

            report_text.insert(
                tk.END,
                f"Student ID : {student[0]}\n"
            )
            report_text.insert(
                tk.END,
                f"Name       : {student[1]}\n"
            )
            report_text.insert(
                tk.END,
                f"Email      : {student[2]}\n"
            )
            report_text.insert(
                tk.END,
                f"Phone      : {student[3]}\n"
            )
            report_text.insert(
                tk.END,
                f"Gender     : {student[4]}\n"
            )
            report_text.insert(
                tk.END,
                f"Course     : {student[5]}\n"
            )
            report_text.insert(
                tk.END,
                f"Semester   : {student[6]}\n\n"
            )

            # Marks
            report_text.insert(
                tk.END,
                "------------- MARKS -------------\n"
            )

            if marks_data:
                total = 0

                for subject, marks in marks_data:
                    report_text.insert(
                        tk.END,
                        f"{subject} : {marks}\n"
                    )
                    total += marks

                average = total / len(marks_data)

                report_text.insert(
                    tk.END,
                    f"\nTotal Marks   : {total}\n"
                )
                report_text.insert(
                    tk.END,
                    f"Average Marks : {average:.2f}\n"
                )
            else:
                report_text.insert(
                    tk.END,
                    "No marks records found.\n"
                )

            # Attendance
            report_text.insert(
                tk.END,
                "\n---------- ATTENDANCE ----------\n"
            )

            if attendance_data:

                present = 0
                absent = 0

                for attendance_date, status in attendance_data:

                    report_text.insert(
                        tk.END,
                        f"{attendance_date} : {status}\n"
                    )

                    if status.lower() == "present":
                        present += 1
                    elif status.lower() == "absent":
                        absent += 1

                total_attendance = present + absent

                if total_attendance > 0:
                    percentage = (
                        present / total_attendance
                    ) * 100
                else:
                    percentage = 0

                report_text.insert(
                    tk.END,
                    f"\nPresent : {present}\n"
                )
                report_text.insert(
                    tk.END,
                    f"Absent  : {absent}\n"
                )
                report_text.insert(
                    tk.END,
                    f"Attendance Percentage : {percentage:.2f}%\n"
                )

            else:
                report_text.insert(
                    tk.END,
                    "No attendance records found.\n"
                )

        except ValueError:
            messagebox.showerror(
                "Error",
                "Student ID must be a number"
            )

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    # Generate Report Button
    tk.Button(
        search_frame,
        text="Generate Report",
        width=18,
        height=2,
        command=generate_report
    ).grid(row=0, column=2, padx=10)


# Test directly
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    open_reports()

    root.mainloop()