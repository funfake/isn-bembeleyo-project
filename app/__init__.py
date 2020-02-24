from flask import Flask
from config import Config
import sqlite3

app = Flask(__name__)
app.config.from_object(Config)

db = sqlite3.connect('database.db') # creates the db instance
cursor = db.cursor() # curseur pour se ballader dans la db

# cursor.execute("CREATE TABLE users (first_name text, last_name text, username text, birthdate integer, email text, password text)")

#db.commit() # saving to database

#db.close()

from app import routes