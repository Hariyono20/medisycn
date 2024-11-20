import mysql.connector
from mysql.connector import Error

def create_connection():
    """ Membuat koneksi ke database MySQL """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='MediSycn',  
            user='root', 
            password=''  
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
        else:
            print("Failed to connect")
            return None
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def create_table():
    """ Membuat tabel user jika belum ada """
    connection = create_connection()
    if connection is None:
        print("Failed to connect to database. Table creation skipped.")
        return  

    try:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            phone VARCHAR(20) NOT NULL,
            password VARCHAR(255) NOT NULL
        )
        """)
        connection.commit()
        print("Table 'users' created successfully (if not already exists).")
    except Error as e:
        print(f"Error while creating table: {e}")
    finally:
        cursor.close()
        connection.close()
