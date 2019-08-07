import os
import psycopg2
import pandas as pd

DATABASE_URL = os.environ['DATABASE_URL']


def upload_response(response):
    if not response or len(response) != 5:
        return 0

    # Establish a connection to our heroku database and verify it works
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to", record)

    # Create the sql query to add a new row into the database
    sql = """INSERT INTO users(user_id, block_id, date, value, feedback)
            VALUES(%s, %s, %s, %s, %s);"""
    user_id = response[0]
    block_id = response[1]
    date = response[2]
    value = response[3]
    feedback = response[4]
    cursor.execute(sql, (user_id, block_id, date, value, feedback))

    # Check that the format was correctly created
    my_table = pd.read_sql('select * from users', conn)
    print("User table after pushing new row\n", my_table)

    # Save the update to the database
    conn.commit()

    # Close the database connection
    if conn:
        cursor.close()
        conn.close()
        print("PostgreSQL connection is closed")