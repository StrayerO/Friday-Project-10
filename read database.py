import sqlite3

# Connect to the database
conn = sqlite3.connect('feedback_analysis.db')

# Create a cursor object
cursor = conn.cursor()

# Execute a query to list all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Iterate through tables and print their contents
for table in tables:
    print(f"Contents of table {table[0]}:")
    cursor.execute(f"SELECT * FROM {table[0]}")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    print()

# Close the connection
conn.close()
