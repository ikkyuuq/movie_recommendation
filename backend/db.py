import mysql.connector
from urllib.parse import urlparse

def get_database_connection():
    config = {
        'use_pure': True,
    }
    
    conn = mysql.connector.connect(**config, **parse_database_url("mysql://ppat0rvqdjwpne0s:bbzl4wv26u9e2ia1@jsk3f4rbvp8ayd7w.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/ua67pti3q7zksp05"))
    return conn

def parse_database_url(url):
    parsed_url = urlparse(url)
    
    user = parsed_url.username
    password = parsed_url.password
    host = parsed_url.hostname
    port = parsed_url.port
    db = parsed_url.path.strip('/')
    
    return {
        'host': host,
        'port': port,
        'user': user,
        'password': password,
        'database': db
    }

def commit_and_close(connection):
    if connection.is_connected():
        connection.commit()
        connection.close()
        
def execute_query_and_commit(conn, cursor, query, params=None):
    cursor.execute(query, params)
    commit_and_close(conn)

def disable_foreign_key_checks(cursor, conn):
    DISABLE_FOREIGN_KEY_CHECKS_QUERY = "SET FOREIGN_KEY_CHECKS=0"
    cursor.execute(DISABLE_FOREIGN_KEY_CHECKS_QUERY)
    conn.commit()

def enable_foreign_key_checks(cursor, conn):
    ENABLE_FOREIGN_KEY_CHECKS_QUERY = "SET FOREIGN_KEY_CHECKS=1"
    cursor.execute(ENABLE_FOREIGN_KEY_CHECKS_QUERY)
    conn.commit()
