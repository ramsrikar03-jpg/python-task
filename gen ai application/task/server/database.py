import mysql.connector

from config import MYSQL_DB, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER


def get_db_connection():
    """Create and return a MySQL connection to movie_ticket_booking."""
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
    )


def get_database_name():
    return MYSQL_DB
