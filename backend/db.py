import mysql.connector
from config import HOST, DB_USER, DB_PASSWORD, DATABASE

def get_database_connection():
    config = {
        'host': HOST,
        'user': DB_USER,
        'password': DB_PASSWORD,
        'database': DATABASE,
        'connect_timeout': 5000,
    }
    return mysql.connector.connect(**config)

def commit_and_close(connection):
    if connection.is_connected():
        connection.commit()
        connection.close()

def disable_foreign_key_checks(cursor, conn):
    DISABLE_FOREIGN_KEY_CHECKS_QUERY = "SET FOREIGN_KEY_CHECKS=0"
    cursor.execute(DISABLE_FOREIGN_KEY_CHECKS_QUERY)
    conn.commit()

def enable_foreign_key_checks(cursor, conn):
    ENABLE_FOREIGN_KEY_CHECKS_QUERY = "SET FOREIGN_KEY_CHECKS=1"
    cursor.execute(ENABLE_FOREIGN_KEY_CHECKS_QUERY)
    conn.commit()
