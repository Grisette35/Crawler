import sqlite3

conn = sqlite3.connect('ma_base_de_donnees.db')

cursor = conn.cursor()


def _initialize_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS downloaded_pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                age INTEGER
            )
        ''')
        conn.commit()
        conn.close()


cursor.execute('''
    INSERT INTO utilisateurs (nom, age) VALUES (?, ?)
''', ('John Doe', 30))


conn.commit()
conn.close()
