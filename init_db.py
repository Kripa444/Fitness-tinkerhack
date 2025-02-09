import sqlite3

# Connect to the database
conn = sqlite3.connect('payments.db')  # This creates the database file if it doesn't exist
cursor = conn.cursor()

# Create the 'payments' table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        upi_id TEXT NOT NULL,
        status TEXT NOT NULL
    )
''')

# Insert a test payment record to check if insertion works
try:
    cursor.execute("INSERT INTO payments (upi_id, status) VALUES (?, ?)", ('testuser@upi', 'success'))
    conn.commit()  # Commit the changes
    print("Database initialized successfully and test data inserted.")
except sqlite3.Error as e:
    print(f"Error during database operations: {e}")

# Close the connection
conn.close()
