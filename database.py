import sqlite3

DB_NAME = "books.db"

def connect():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        year TEXT,
        genre TEXT,
        publisher TEXT
    )
    """)
    conn.commit()
    conn.close()

def insert_book(data):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO books (title, author, year, genre, publisher)
    VALUES (?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()

def get_books():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    data = cursor.fetchall()
    conn.close()
    return data

def update_book(book_id, data):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE books 
    SET title=?, author=?, year=?, genre=?, publisher=?
    WHERE id=?
    """, (*data, book_id))
    conn.commit()
    conn.close()


def delete_book(book_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()