import os
import sqlite3

DATABASE_PATH = 'database.db'

if os.path.exists(DATABASE_PATH):
    os.remove(DATABASE_PATH)

connection = sqlite3.connect(DATABASE_PATH)

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
connection.commit()
connection.close()