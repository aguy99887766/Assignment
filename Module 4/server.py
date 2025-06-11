from flask import Flask, jsonify, request
import database

def get_db_connection():
	connection = database.get_connection("books.db")
	return connection

app = Flask(__name__)

@app.route("/")
def homepage() -> None:
	return "Hello"

@app.route("/get-books")
def get_books() -> None:
	connection = get_db_connection()
	books = database.get_books(connection)
	print(books)
	if not books:
		return ["No books found"]
	data = []
	for book in books:
		data.append({
			"BOOK NAME": book[1],
			"AUTHOR": book[2],
			"PUBLISHER": book[3],
			"ID": book[0]
		})
				
	return jsonify(data)

@app.route("/put-book", methods=["PUT"])
def put_book() -> None:
	data = request.get_json()
	if not data:
		return jsonify({'message': 'No request body'})

	book_name = data.get("book_name")
	author = data.get("author")
	publisher = data.get("publisher")

	connection = get_db_connection()
	try:
		database.insert_book(connection, book_name, author, publisher)		
	except Exception as e:
		print(f"[-] {e}")
		return jsonify({"message": "Err: Invalid request"})
		
	return jsonify({"message": f"{book_name} was added"})		

@app.route("/delete", methods=["DELETE"])
def delete_book() -> None:
	data = request.get_json()
	if not data:
		return jsonify({'message': 'No request body'})
	
	book_id = data.get('id')

	connection = get_db_connection()
	try:
		database.remove_book(connection, book_id)
	except Exception as e:
		print(f"[-] {e}")
		return jsonify({"message": f"BOOK ID: {book_id} could not be deleted"})
	
	return jsonify({"message": f"BOOK ID: {book_id} was deleted"})
	
@app.route("/update", methods=["PUT"])
def update_book() -> None:
	data = request.get_json()
	if not data:
		return jsonify({'message': 'No request body'})
	
	book_name = data.get('book_name')
	new_book_name = data.get('new_book_name')

	connection = get_db_connection()
	try:
		database.update_book_name(connection, book_name, new_book_name)
	except Exception as e:
		print(f"[-] {e}")
		return jsonify({"message": f"BOOK NAME: {book_name} could not be updated"})
	return jsonify({"message": f"BOOK_NAME: {book_name} has been updated to {new_book_name}"})
	

app.run(debug = True)
