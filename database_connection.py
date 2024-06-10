from mysql.connector import connect, Error

def get_connection():
    try:
        connection = connect(
            host="localhost",
            user="root",
            password="nmims@123",
            database="mysociety_2",
        )
        return connection
    except Error as e:
        print("Error:", e)
        return None
