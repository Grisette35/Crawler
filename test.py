import sqlite3

conn = sqlite3.connect('pages_db.db')
cursor = conn.cursor()

cursor.execute('''
        SELECT url, age FROM downloaded_pages
    ''')
result = cursor.fetchall()
print(result)


conn.close()