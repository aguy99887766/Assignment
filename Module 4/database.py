import sqlite3

def get_connection(db_name: str) -> sqlite3:
	return sqlite3.connect(db_name)

def create_table(connection: sqlite3) -> None:
	query = """
	CREATE TABLE IF NOT EXISTS books (
		id INTEGER PRIMARY KEY,
		book_name TEXT NOT NULL,
		author TEXT NOT NULL,
		publisher TEXT NOT NULL
	)
	"""
	try:
		with connection:
			connection.execute(query)
	except Exception as e:
		print(f"[-] {e}")


def insert_book(connection: sqlite3, book_name: str, author: str, publisher: str) -> None:
	query = "INSERT INTO books (book_name, author, publisher) VALUES (?, ?, ?)"

	with connection:
		connection.execute(query, (book_name, author, publisher))
	print(f"[+] {book_name} has been added")

def get_books(connection: sqlite3, condition: str | None = None) -> list[tuple]: 
	query = "SELECT * FROM books"
	if condition:
		query += f" WHERE {condition}"
	try:
		with connection:
			rows = connection.execute(query).fetchall()
		return rows
	except Exception as e:
		print(f"[-] {e}")

def remove_book(connection: sqlite3, book_id: int) -> None:
	query = "DELETE FROM books WHERE id = ?"
	try:
		with connection:
			connection.execute(query, (book_id,))
		print(f"[+] {book_id} has been deleted")
	except Exception as e:
		print(f"[-] {e}")


def update_book_name(connection: sqlite3, book_name: str, old_book_name: str) -> None:
	query = "UPDATE books SET book_name = ? WHERE book_name = ?"
	with connection:
		connection.execute(query, (old_book_name, book_name))
	print(f"[+] {book_name} has been updated to {old_book_name}")
		

if __name__ == '__main__':
	connection = get_connection("books.db")
	create_table(connection)
	# insert_book(connection, "My Book 1", "Person 1", "Person 2")
	# insert_book(connection, "My Book 2", "Person 1", "Person 2")
	# insert_book(connection, "My Book 3", "Person 1", "Person 2")
	update_book_name(connection, "My Book 1", "Cool Thing")
	books = get_books(connection)
	print(books)
