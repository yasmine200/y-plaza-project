import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='y_plaza_db',
            user='root',
            password=''
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Erreur MySQL: {e}")
        return None