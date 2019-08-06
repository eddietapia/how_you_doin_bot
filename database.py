import os
import psycopg2
import pandas as pd

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
print("Connected", conn)
cursor = conn.cursor()
cursor.execute("SELECT version();")
record = cursor.fetchone()
print("You are connected to", record)


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = [
        """
        CREATE TABLE users(
            user_id INTEGER NOT NULL,
            block_id VARCHAR(255) NOT NULL,
            date VARCHAR(255) PRIMARY KEY NOT NULL,
            value INTEGER,
            feedback VARCHAR(255)
        )
        """,
        """
        CREATE TABLE vendors (
            vendor_id SERIAL PRIMARY KEY,
            vendor_name VARCHAR(255) NOT NULL
        )
        """,
        """ CREATE TABLE parts (
                part_id SERIAL PRIMARY KEY,
                part_name VARCHAR(255) NOT NULL
                )
        """,
        """
        CREATE TABLE part_drawings (
                part_id INTEGER PRIMARY KEY,
                file_extension VARCHAR(5) NOT NULL,
                drawing_data BYTEA NOT NULL,
                FOREIGN KEY (part_id)
                REFERENCES parts (part_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE vendor_parts (
                vendor_id INTEGER NOT NULL,
                part_id INTEGER NOT NULL,
                PRIMARY KEY (vendor_id , part_id),
                FOREIGN KEY (vendor_id)
                    REFERENCES vendors (vendor_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (part_id)
                    REFERENCES parts (part_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """]
    return commands
commands = create_tables()
for command in commands:
    print("EXECUTING")
    cursor.execute(command)

my_table = pd.read_sql('select * from users', conn)
my_table_2 = pd.read_sql('select * from vendor_parts', conn)
print("TABLE 1\n", my_table)
print("TABLE 2\n", my_table_2)

# Closing database connection.
if(conn):
    cursor.close()
    conn.close()
    print("PostgreSQL connection is closed")



