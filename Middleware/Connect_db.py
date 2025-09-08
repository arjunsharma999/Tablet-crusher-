import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="BeagleBone99",  
            database="JSR"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        raise RuntimeError(f"? Error while connecting to MySQL: {e}")
