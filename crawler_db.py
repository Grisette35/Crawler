class Crawler_db:
    def create_conn(self):
        conn = sqlite3.connect('pages_db.db')
        cursor = conn.cursor()
        return conn, cursor

    def close_conn(self, conn):
        conn.close()

    def initialize_database(self, conn, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS downloaded_pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                content TEXT NOT NULL,
                age INTEGER
            )
        ''')
        conn.commit()

    def save_to_database(self, conn, cursor, url, content):
        cursor.execute('''
        INSERT INTO downloaded_pages (url, content, age) VALUES (?, ?)
    ''', (url, content, 0))
        conn.commit()

    def url_in_db(self, conn, cursor, current_url):
        cursor.execute('''
        SELECT COUNT(*) FROM downloaded_pages WHERE url = ?
    ''', (current_url,))
        result = cursor.fetchone()
        return result[0]

    def mettre_a_jour_age(self, conn, cursor, current_url):
        cursor.execute('''
        UPDATE pages SET age = age + 1 WHERE url <> ?
        ''', (current_url,))

        cursor.execute('''
        UPDATE pages SET age = 0 WHERE url = ?
        ''', (current_url,))

        conn.commit()