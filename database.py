import mysql.connector

from config import MYSQL_PASSWORD

def create_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=MYSQL_PASSWORD,
        database="student_management"
    )

    return connection


# Test connection
try:
    conn = create_connection()
    print("MySQL Database Connected Successfully!")
    conn.close()
except mysql.connector.Error as e:
    print("Database connection failed:", e)