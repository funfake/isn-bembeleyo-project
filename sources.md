# These are web pages that I used to debug problems

### installing flask
- main tutorial : https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
- infos about commands and env variables : https://flask.palletsprojects.com/en/1.1.x/cli/
- because Windows is bullshit, to start Flask, you have to `python -m flask run` instead of `flask run` *+ env variables are set/exported/$env differently* https://github.com/pallets/flask/issues/2083
- flask debug : https://stackoverflow.com/questions/17309889/how-to-debug-a-flask-app
- flask dev environment : https://flask.palletsprojects.com/en/1.1.x/config/
- generate flask secret key : https://stackoverflow.com/questions/34902378/where-do-i-get-a-secret-key-for-flask *(in the project config file)*

## login and session system
- create webforms with flask and flask-wtforms : https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
- basic flask login system with one user : https://pythonspot.com/login-authentication-with-flask/
- complement about storing username in session : https://www.tutorialspoint.com/flask/flask_sessions.htm
- date picker for registration : https://www.cssscript.com/flat-style-javascript-date-picker-flatpickr/
- flask Form Fields : https://wtforms.readthedocs.io/en/stable/fields.html

## databases and python
- sqlite db with python introduction video : https://www.youtube.com/watch?v=pd-0G0MigUA
- prog orientée objet + sql requests == tuples ! :  https://www.w3schools.com/python/trypython.asp?filename=demo_tuple1
- add primary keys : https://www.tutorialspoint.com/sqlite/sqlite_primary_key.htm (ne marche pas)
- champ unique pour l'adresse mail et le nom d'utilisateur : https://www.sqlitetutorial.net/sqlite-unique-constraint/
- afficher les erreurs liées à la requête : https://www.programcreek.com/python/example/6844/sqlite3.Error

## hashage de mot de passe
- bcrypt ne fonctionne pas
- X shitty : https://pypi.org/project/bcrypt/ probleme module qui n'existe pas (.hashpwd)
- blake2b ; argon2 ; cipher
- module passlib (sous sha256 mais choix possible) : https://blog.tecladocode.com/learn-python-encrypting-passwords-python-flask-and-passlib/

## lists to show users with same birthdate (loops and lists)
- erreur list out or range : https://openclassrooms.com/forum/sujet/index-error-list-index-out-of-range
- fetchall() // fetchone() : http://zetcode.com/python/pymysql/
- dicts : https://realpython.com/iterate-through-dictionary-python/
- type error : https://www.reddit.com/r/learnpython/comments/34vqk1/typeerror_nonetype_object_is_not_subscriptable/
- create/happen element to a list : https://www.programiz.com/python-programming/list
- more lists : https://stackoverflow.com/questions/28709345/how-to-append-to-python-list-without-having-to-initialize-the-list/28709401