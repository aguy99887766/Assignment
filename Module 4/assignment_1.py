from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base




import sqlite3
import csv
import os

if os.path.exists('books.db'):
	os.remove('books.db')


books = sqlite3.connect("books.db")
cur = books.cursor()
cur.execute("CREATE TABLE book (title VARCHAR(20), author VARCHAR(20), year INT)")


Base = declarative_base()
engine = create_engine('sqlite:///books.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

class Books(Base):
	__tablename__ = 'book'
	
	title = Column(String, primary_key=True)
	author = Column(String)

# New Lib ???

def convert_to_sql(file_name: str, database: str, *keys) -> None:
	if not file_name.endswith(f".csv"):
		raise Exception("Not a valid file type")
	
	database_values = ", ".join(keys)
	placeholders = ', '.join(['?'] * len(keys))

	with open(file_name, 'r') as file:
		reader = csv.DictReader(file)


		for row in reader:
			
			ins = f'INSERT INTO {database} ({database_values}) VALUES({placeholders})'	
			cur.execute(ins, tuple(row[key] for key in keys))
	

	books.commit()

def output_rows(database: str) -> None:
	cur.execute(f'SELECT * from {database}')
	rows = cur.fetchall()
	print(rows)



if __name__ == '__main__':


	convert_to_sql('books2.csv', 'book', 'title', 'author', 'year')

	books = session.query(Books).order_by(Books.title.asc()).all()
	for book in books:
		print(book.title)

