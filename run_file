import sqlite3
import hashlib

# Connect to the database
db_connection = sqlite3.connect('project.db')
cursor = db_connection.cursor()

# Hash the password
def hash_password(password):
    return hashlib.sha1(password.encode()).hexdigest()

# Function to insert account
def insert_account(username, password):
    hashed_password = hash_password(password)
    try:
        cursor.execute('''
            INSERT OR IGNORE INTO accounts (username, password, teacher, admin) 
            VALUES (?, ?, ?, ?)
        ''', (username, hashed_password, 'yes', 'yes'))
        db_connection.commit()
        print("Account inserted successfully.")
    except sqlite3.Error as e:
        print("Error inserting account:", e)

# Insert account if it doesn't exist
insert_account("", "")  # Provide the username and password here

# Close the database connection
db_connection.close()
