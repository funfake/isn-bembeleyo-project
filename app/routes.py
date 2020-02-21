from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'William'}
    return render_template('index.html', title='Accueil', user=user)