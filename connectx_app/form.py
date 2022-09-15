from flask_wtf import FlaskForm
from wtforms import SubmitField , SelectField, StringField, PasswordField
from wtforms.validators import DataRequired
from .agent_minmax import my_agent_binary_negmax


class options(FlaskForm):
    """[Form to choose options of the game]
    
    """

    adversaire = SelectField(label="Adversaire", choices=[('random', 'random'),( "MinMax","MinMax"),("PPO2","PPO2")])
   
    submit = SubmitField(label="Valider")

class Login(FlaskForm):
    """[Form to login]
    """
    pseudo = StringField(label="pseudo: ", validators = [DataRequired()])
    password = PasswordField(label="Mot de passe:", validators = [DataRequired()])
    submit = SubmitField(label="Se connecter")