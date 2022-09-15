from flask_wtf import FlaskForm
from wtforms import SubmitField , SelectField, StringField, PasswordField
from wtforms.validators import DataRequired
from .agent_minmax import my_agent_binary_negmax


class options(FlaskForm):
    """[Form to choose options of the game]
    
    """

    adversaire = SelectField(label="Adversaire", choices=[('random', 'random'),( "MinMax","MinMax")])
   
    submit = SubmitField(label="Valider")

class LoginForm(FlaskForm):
    """Form to login to the app
    """
    pseudo = StringField(label="pseudo", validators=[DataRequired()])
    password = PasswordField(label="password", validators=[DataRequired()])
    submit = SubmitField(label="Log in")