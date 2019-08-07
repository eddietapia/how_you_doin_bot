import os
import psycopg2
from psycopg2.extras import Json
import pandas as pd

DATABASE_URL = os.environ['DATABASE_URL']


def create_tables():
    """ Create tables in the PostgreSQL database"""
    commands = [
        """
        CREATE TABLE users(
            user_id INTEGER NOT NULL,
            block_id VARCHAR(255) NOT NULL,
            date VARCHAR(255) PRIMARY KEY NOT NULL,
            value INTEGER,
            feedback VARCHAR(255)
        )
        """
    ]
    return commands


# Establish a connection to our heroku database and verify it works
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()
cursor.execute("SELECT version();")
record = cursor.fetchone()
print("You are connected to", record)

# Create the table where we will store our data
commands = create_tables()
for command in commands:
    print("EXECUTING")
    cursor.execute(command)

# Commit to save the changes to the
# Check that the format was correctly created
my_table = pd.read_sql('select * from users', conn)
print("User table\n", my_table)

new_entry = {
    'user_id': '1',
    'block_id': 'emotion',
    'date': '2019-06-05',
    'value': 2,
    'feedback': ''
}
user_id = '1'
block_id = 'emotion'
date = '2019-06-05'
value = 2
feedback = 'Hello'
cursor.execute(sql, (user_id, block_id, date, value, feedback))

# Close the database connection
if conn:
    cursor.close()
    conn.close()
    print("PostgreSQL connection is closed")



