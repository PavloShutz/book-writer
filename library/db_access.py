import sqlite3

connection = sqlite3.connect("library.db")

cur = connection.cursor()

cur.execute("DELETE FROM books")

connection.commit()

connection.close()
