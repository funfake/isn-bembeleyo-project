from flask import render_template, flash, redirect, url_for, request, session, abort
from app import app
from app.forms import LoginForm, RegistrationForm
from app.models import User
import sqlite3
from passlib.context import CryptContext
from app.requests import get_user_by_username, get_users_by_birthdate, insert_user, check_encrypted_password, encrypt_password, remove_user, update_names

@app.route('/')
@app.route('/index')
def index():
    
    # cursor.execute("INSERT INTO users VALUES ('Baptiste', 'Dumy', 'baptiste', '16042002', 'contact@baptiste.fr', 'dummy')")
    # cursor.execute("SELECT * FROM users WHERE first_name='William'")
    # print(cursor.fetchone()) # différent de fetchmany(max5) ou fetchall()
    sel_users_list = [] # on initialise la liste
    
    if not session.get('logged_in'):
        user = {'username': 'bel.lle inconnu.e'} # user en POO, valeur par défaut si pas connecté pour pas tout faire crasher
        sel_users = None
        # tolog = True
    else:
        username = session.get('username') # on recupere le nom d'uttilisateur encrypté dans la session
        user = User(get_user_by_username(username)[0], get_user_by_username(username)[1], get_user_by_username(username)[2], get_user_by_username(username)[3], get_user_by_username(username)[4], None) # on recupere cet utilisateur en tant qu'objet db
        sel_users = get_users_by_birthdate(user.birthdate) # on recupere une liste (raw) de tous les utilisateurs avec la meme date de naissance
        for sel_user in sel_users:
            new_user = User(get_user_by_username(sel_user[2])[0], get_user_by_username(sel_user[2])[1], get_user_by_username(sel_user[2])[2], get_user_by_username(sel_user[2])[3], get_user_by_username(sel_user[2])[4], None) # on transofrme l'utilisateur issu de la liste (Raw) en objet
            sel_users_list.append(new_user) # on l'ajoute a la liste
        # tolog = False
    return render_template('index.html', title='Accueil', user=user, sel_users_list=sel_users_list) # on affiche l'accueil


@app.route('/login', methods=['GET', 'POST']) # compliqué pour faire marcher le système de "déjà connecté, obligé de le faire sur le traitement de la page en jinja"
def login():
    form = LoginForm(request.form)
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
    
    bd = request.args.get('birthdate', '') # on récupère la date de naissance passée dans la requete GET, si nulle remplacement par "rien"
    
    form = RegistrationForm(request.form)
    
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
        
    return render_template('register.html', title='S\'inscrire', form=form, bd=bd) # si pas de formulaire envoyé, on l'affiche


@app.route('/settings', methods=['GET', 'POST']) # compliqué pour faire marcher le système de "déjà connecté, obligé de le faire sur le traitement de la page en jinja"
def settings():
    if session.get('logged_in'):
        username = session.get('username')
        sel_user = User(get_user_by_username(username)[0], get_user_by_username(username)[1], get_user_by_username(username)[2], get_user_by_username(username)[3], get_user_by_username(username)[4], get_user_by_username(username)[5],)
       
        # on pré-remplis le formulaire avec les données de l'utilisateur
        form = RegistrationForm(obj=sel_user)
        
        # on peut modifier le formulaire avec form.<NAME>.data
        form.username.data = sel_user.username
        form.birthdate.data = sel_user.birthdate
        form.password.data = sel_user.password
        form.password2.data = sel_user.password
        
        # on valide le formulaire
        if request.method == 'POST' and form.validate():
            update_names(sel_user, form.first_name.data, form.last_name.data, form.email.data) # fonction définie plus haut permettant d'intéragir avec la bdd
            flash('Informations mises à jour')
                
        return render_template('settings.html', title='Paramètres', form=form) # si pas de formulaire envoyé (POST), on l'affiche
    else:
        return redirect(url_for('index'))