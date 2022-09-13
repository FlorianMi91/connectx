from flask_wtf import FlaskForm
from wtforms import SubmitField , SelectField, StringField, PasswordField
from wtforms.validators import DataRequired


class options(FlaskForm):
    """[Form to choose options of the game]
    """

    adversaire = SelectField(label="Adversaire", choices=[('Random', 'random')])
   
    submit = SubmitField(label="Valider")

class Login(FlaskForm):
    """[Form to login]
    """
    pseudo = StringField(label="pseudo: ", validators = [DataRequired()])
    password = PasswordField(label="Mot de passe:", validators = [DataRequired()])
    submit = SubmitField(label="Se connecter")