from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')
    
class RegistrationForm(FlaskForm):
    first_name = StringField('Prénom', validators=[DataRequired()])
    last_name = StringField('Nom de famille', validators=[DataRequired()])
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    birthdate = DateField('Date de naissance', format='%d/%m/%Y')
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), EqualTo('password2', message='Les mots de passe doivent correspondre')])
    password2 = PasswordField(
        'Confirmer votre mot de passe', validators=[DataRequired()])
    submit = SubmitField('S\'inscrire')

    # def validate_username(self, username):
        # user = User.query.filter_by(username=username.data).first()
        # if user is not None:
        #     raise ValidationError('Please use a different username.')

    # def validate_email(self, email):
        # user = User.query.filter_by(email=email.data).first()
        # if user is not None:
        #     raise ValidationError('Please use a different email address.')