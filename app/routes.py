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

def update_username(user, new_username):
    try:
        db = sqlite3.connect('database.db') # creates the db instance
        c = db.cursor() # curseur pour se ballader dans la db
        c.execute("UPDATE users SET username = :new_username WHERE username=:username AND email=:email", {'username': user.username, 'email': user.email, 'new_username': new_username})
        db.commit() # saving to database
        db.close() # Ferme la connexion après utilisation
    except sqlite3.Error as e:
        error = type(e).__name__
        if error == "IntegrityError":
            flash("Le nom d'utilisateur entré est déjà utilisé") 
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

@app.route('/')
@app.route('/index')
def index():
    
    # cursor.execute("INSERT INTO users VALUES ('Baptiste', 'Dumy', 'baptiste', '16042002', 'contact@baptiste.fr', 'dummy')")
    # cursor.execute("SELECT * FROM users WHERE first_name='William'")
    # print(cursor.fetchone()) # opposed to fetchmany(max5) or fetchall()
   
    
    if not session.get('logged_in'):
        user = {'username': 'bel.lle inconnu.e'} # user en POO, valeur par défaut si pas connecté pour pas tout faire crasher
    else:
        user = {'username': session.get('username')} # stockage de l'utilisateur en POO (objet)
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Accueil', user=user, posts=posts) # on affiche l'accueil


@app.route('/login', methods=['GET', 'POST']) # compliqué pour faire marcher le système de "déjà connecté, obligé de le faire sur le traitement de la page en jinja"
def login():
    form = LoginForm()
    if form.validate_on_submit(): # le form est valide
        # try:
        username = request.form['username']
        sel_user = User(get_user_by_username(username)[0], get_user_by_username(username)[1], get_user_by_username(username)[2], get_user_by_username(username)[3], get_user_by_username(username)[4], get_user_by_username(username)[5],)
        password_to_check = request.form['password']
        try: # if hash is not recognized it gives an error
            if check_encrypted_password(password_to_check, sel_user.password): # password à vérifier, password déjà hashé :: return True or False
                session['logged_in'] = True # la session est marquée comme connectée 
                session['username'] = request.form['username'] # on stocke la variable utilisateur dans la session
                flash('Demande de connexion {}, remember_me={}'.format(
                    form.username.data, form.remember_me.data))  # on affiche la demande de connexion
                return redirect(url_for('index')) # puis on redirige
            else:
                flash('Mauvais mot de passe') # le mot de passe n'est pas bon
                return redirect(url_for('login')) # on redirige de nouveau vers la page de connexion
        except:
            flash('Erreur') # le hash n'a pas éte reconnu ou la procédure n'a pas marché
            return redirect(url_for('login')) # on redirige de nouveau vers la page de connexion
        flash('Utilisateur inconnu') # le mot de passe n'est pas bon
        return redirect(url_for('login')) # on redirige de nouveau vers la page de connexion
    return render_template('login.html', title='Se connecter', form=form) # si pas de formulaire envoyé, on l'affiche


@app.route("/logout")
def logout():
    session['logged_in'] = False # on met le statut "connecté à Faux"
    session.pop('username', None) # on enlève le nom d'utilisateur stocké en session
    return redirect(url_for('index')) # on redirige


@app.route('/register', methods=['GET', 'POST']) # compliqué pour faire marcher le système de "déjà connecté, obligé de le faire sur le traitement de la page en jinja"
def register():

    # update_username(user1, 'lomepal')
    # emp = get_user_by_username('baptiste')
    
    form = RegistrationForm()
    if form.validate_on_submit(): # le form est valide
        #if request.form['password'] == 'password' and request.form['username'] == 'admin': # verif que le mot de passe est le bon
        password = request.form['password'] # on récupère le mot de passe du form pour le traiter
        hashed = encrypt_password(password) # on l'encrypte avec la fonction ci-dessus
        # bcrypt.check_password_hash(pw_hash, 'hunter2') # returns True
        form_user = User(request.form['first_name'], request.form['last_name'], request.form['username'], request.form['birthdate'], request.form['email'], hashed)
        
        if insert_user(form_user) == True:
            session['logged_in'] = True # la session est marquée comme connectée 
            session['username'] = request.form['username'] # on stocke la variable utilisateur dans la session
            flash('Compte créé pour {}'.format(form.username.data))  # on affiche la demande de connexion
            return redirect(url_for('index')) # puis on redirige
        else:
            return redirect(url_for('register'))
    return render_template('register.html', title='S\'inscrire', form=form) # si pas de formulaire envoyé, on l'affiche