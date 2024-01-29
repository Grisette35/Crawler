import sqlite3

class Crawler_db:
    def create_conn(self):
        """
        Establishes a connection to the SQLite database and returns the connection and cursor objects.

        Returns:
        - conn: SQLite database connection object.
        - cursor: SQLite database cursor object.
        """
        conn = sqlite3.connect('pages_db.db')
        cursor = conn.cursor()
        return conn, cursor

    def close_conn(self, conn):
        """
        Closes the SQLite database connection.

        Parameters:
        - conn: SQLite database connection object to be closed.
        """
        conn.close()

    def initialize_database(self, conn, cursor):
        """
        Initializes the SQLite database by creating the 'downloaded_pages' table if it does not exist.

        Parameters:
        - conn: SQLite database connection object.
        - cursor: SQLite database cursor object.
        """
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
        """
        Inserts a new record into the 'downloaded_pages' table with the provided URL, content, and age (initially set to 0).

        Parameters:
        - conn: SQLite database connection object.
        - cursor: SQLite database cursor object.
        - url (str): URL of the downloaded page.
        - content (str): Content of the downloaded page.
        """
        cursor.execute('''
        INSERT INTO downloaded_pages (url, content, age) VALUES (?, ?, ?)
    ''', (url, content, 0))
        conn.commit()

    def url_in_db(self, conn, cursor, current_url):
        """
        Checks if a given URL already exists in the 'downloaded_pages' table.

        Parameters:
        - conn: SQLite database connection object.
        - cursor: SQLite database cursor object.
        - current_url (str): URL to be checked.

        Returns:
        - int: The count of occurrences of the URL in the table (0 if not present, 1 otherwise).
        """
        cursor.execute('''
        SELECT COUNT(*) FROM downloaded_pages WHERE url = ?
    ''', (current_url,))
        result = cursor.fetchone()
        return result[0]

    def mettre_a_jour_age(self, conn, cursor, current_url):
        """
        Updates the 'age' column for existing records in the 'downloaded_pages' table.
        Increases the age for all records except the one with the specified URL, which has its age reset to 0.

        Parameters:
        - conn: SQLite database connection object.
        - cursor: SQLite database cursor object.
        - current_url (str): URL of the page whose age is reset to 0.
        """
        cursor.execute('''
        UPDATE downloaded_pages SET age = age + 1 WHERE url <> ?
        ''', (current_url,))

        cursor.execute('''
        UPDATE downloaded_pages SET age = 0 WHERE url = ?
        ''', (current_url,))

        conn.commit()
