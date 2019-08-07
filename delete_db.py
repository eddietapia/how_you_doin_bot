import os
import psycopg2
import pandas as pd

DATABASE_URL = os.environ['DATABASE_URL']


# Establish a connection to our heroku database and verify it works
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()
cursor.execute("SELECT version();")
record = cursor.fetchone()
print("You are connected to", record)

# Check that the format was correctly created
my_table = pd.read_sql('select * from users', conn)
print("User table\n", my_table)

# Create the sql query to add a new row into the database
# sql = """DROP TABLE users;"""

cursor.execute(sql)

# Save the update to the database
conn.commit()

# Close the database connection
if conn:
    cursor.close()
    conn.close()
    print("PostgreSQL connection is closed")