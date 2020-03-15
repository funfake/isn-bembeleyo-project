from flask import render_template, flash, redirect, url_for, request, session, abort
from app import app
from app.forms import LoginForm, RegistrationForm
from app.models import User
import sqlite3
from passlib.context import CryptContext

pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
)

def encrypt_password(password):
    return pwd_context.encrypt(password)

def check_encrypted_password(password, hashed):
    return pwd_context.verify(password, hashed)

def insert_user(user):
    try:
        db = sqlite3.connect('database.db') # creates the db instance
        c = db.cursor() # curseur pour se ballader dans la db
        c.execute("INSERT INTO users VALUES (:first_name, :last_name, :username, :birthdate, :email, :password)", {'first_name': user.first_name, 'last_name': user.last_name, 'username': user.username, 'birthdate': user.birthdate, 'email': user.email, 'password': user.password})
        db.commit() # saving to database
        db.close() # Ferme la connexion après utilisation
        return True
    except sqlite3.Error as e:
        error = type(e).__name__
        if error == "IntegrityError":
            flash("Le nom d'utilisateur entré ou l'adresse email sont déjà utilisés") 
        else:
            flash(error) 
            
def get_user_by_username(username):
    try:
        db = sqlite3.connect('database.db') # creates the db instance
        c = db.cursor() # curseur pour se ballader dans la db
        c.execute("SELECT * FROM users WHERE username=:username", {'username': username})
        # db.close() # Ferme la connexion après utilisation
        return c.fetchone() # returns a tuple
    except sqlite3.Error as e:
        error = type(e).__name__
        flash(error) 

def update_names(user, new_first_name, new_last_name):
    try:
        db = sqlite3.connect('database.db') # creates the db instance
        c = db.cursor() # curseur pour se ballader dans la db
        c.execute("UPDATE users SET first_name = :new_first_name, last_name = :new_last_name WHERE username=:username AND email=:email", {'username': user.username, 'email': user.email, 'new_first_name': new_first_name, 'new_last_name': new_last_name})
        db.commit() # saving to database
        db.close() # Ferme la connexion après utilisation
    except sqlite3.Error as e:
        error = type(e).__name__
        if error == "IntegrityError":
            flash("Une erreur s'est produite") 
        else:
            flash(error) 

def remove_user(user):
    try:
        db = sqlite3.connect('database.db') # creates the db instance
        c = db.cursor() # curseur pour se ballader dans la db
        c.execute("DELETE from users WHERE username=:username AND email=:email", {'username': user.username, 'email': user.email})
        db.commit() # saving to database
        db.close() # Ferme la connexion après utilisation
    except sqlite3.Error as e:
        error = type(e).__name__
        flash(error) 
        
def get_users_by_birthdate(birthdate):
    try:
        db = sqlite3.connect('database.db') # creates the db instance
        c = db.cursor() # curseur pour se ballader dans la db
        c.execute("SELECT * FROM users WHERE birthdate=:birthdate", {'birthdate': birthdate})
        # db.close() # Ferme la connexion après utilisation
        return c.fetchall() # returns a tuple
    except sqlite3.Error as e:
        error = type(e).__name__
        flash(error) 