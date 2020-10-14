from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker 
import os

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind = engine))

def create_table_users():
	db.execute("CREATE TABLE %s (id SERIAL PRIMARY KEY, username VARCHAR(255), password VARCHAR(255));" % "users") 
	db.commit()

def create_table_books():
	db.execute("CREATE TABLE %s (isbn VARCHAR(10), title TEXT, author TEXT, year VARCHAR(4), PRIMARY KEY (isbn));" % "books") 
	db.commit()

def fill_books():
	sql = "INSERT INTO books (isbn, title, author, year) VALUES ('%s', '%s', '%s', '%s')"
	with open("books.csv", "r") as f_r:
		line = f_r.readline()
		line = f_r.readline()
		while line:
			if line.find("\"") < 0 and line.find("\'") < 0:
				line = line.strip("\n").split(",")
				db.execute(sql % tuple(line))
			line = f_r.readline()
	db.commit()

def create_table_reviews():
	db.execute("CREATE TABLE %s (id SERIAL PRIMARY KEY, user_id INT, isbn VARCHAR(10), comment TEXT, rating INT, time TIMESTAMP(6));" % "reviews") 
	db.commit()