'''
# Code has already been run, DO NOT RUN IT AGAIN

import sqlite3

# Create or connect to a database
conn = sqlite3.connect('expenseTracker.db')

# Create a cursor
cursor = conn.cursor()

# Create table

cursor.execute("""CREATE TABLE expenseTracker (
    expenseName text,
    amount integer,
    date text,
    category text,
    paymentType text)""")

'''
