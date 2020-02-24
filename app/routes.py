from flask import render_template, flash, redirect, url_for, request, session, abort
from app import app
from app.forms import LoginForm, RegistrationForm
from app.models import User
import sqlite3

@app.route('/')
@app.route('/index')
def index():
    # DB connection
    db = sqlite3.connect('database.db') # creates the db instance
    cursor = db.cursor() # curseur pour se ballader dans la db
    # cursor.execute("INSERT INTO users VALUES ('Baptiste', 'Dumy', 'baptiste', '16042002', 'contact@baptiste.fr', 'dummy')")
    # cursor.execute("SELECT * FROM users WHERE first_name='William'")
    # print(cursor.fetchone()) # opposed to fetchmany(max5) or fetchall()
    db.commit() # saving to database
    db.close() # Ferme la connexion après utilisation
    
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
        if request.form['password'] == 'password' and request.form['username'] == 'admin': # verif que le mot de passe est le bon
            session['logged_in'] = True # la session est marquée comme connectée 
            session['username'] = request.form['username'] # on stocke la variable utilisateur dans la session
            flash('Demande de connexion {}, remember_me={}'.format(
                form.username.data, form.remember_me.data))  # on affiche la demande de connexion
            return redirect(url_for('index')) # puis on redirige
        else:
            flash('Mauvais mot de passe') # le mot de passe n'est pas bon
            return redirect(url_for('login')) # on redirige de nouveau vers la page de connexion
    return render_template('login.html', title='Se connecter', form=form) # si pas de formulaire envoyé, on l'affiche


@app.route("/logout")
def logout():
    session['logged_in'] = False # on met le statut "connecté à Faux"
    session.pop('username', None) # on enlève le nom d'utilisateur stocké en session
    return redirect(url_for('index')) # on redirige


@app.route('/register', methods=['GET', 'POST']) # compliqué pour faire marcher le système de "déjà connecté, obligé de le faire sur le traitement de la page en jinja"
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # le form est valide
        #if request.form['password'] == 'password' and request.form['username'] == 'admin': # verif que le mot de passe est le bon
        session['logged_in'] = True # la session est marquée comme connectée 
        session['username'] = request.form['username'] # on stocke la variable utilisateur dans la session
        flash('Demande de connexion {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))  # on affiche la demande de connexion
        return redirect(url_for('index')) # puis on redirige
    return render_template('register.html', title='S\'inscrire', form=form) # si pas de formulaire envoyé, on l'affiche