import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
print("Connected", conn)
cursor = conn.cursor()
print(cursor.execute("SELECT version();"))



