from connectx_app import db,login_manager
import datetime 
from flask_login import UserMixin # allow to set variable is_active=True and to stay connected
import logging as lg
from werkzeug.security import generate_password_hash
import csv

@login_manager.user_loader
def load_user(user):
    return User.query.get(user)

class User(db.Model ,UserMixin):
    """Create a table Users on the candidature database
    Args:
        db.Model: Generates columns for the table
        UserMixin: Generates an easy way to provide a current_user
    """
    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
    pseudo = db.Column(db.String(length=50),nullable=False, unique=True)
    password_hash = db.Column(db.String(length=200), nullable=False)
    
    def __repr__(self):
        return f'{self.pseudo} '
    
    @classmethod
    def find_by_pseudo(cls, nom):
        return cls.query.filter_by(pseudo=nom).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()



class Score(db.Model ):
    """Create a table Users on the candidature database
    Args:
        db.Model: Generates columns for the table
        UserMixin: Generates an easy way to provide a current_user
    """
    id_score = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
    pseudo = db.Column(db.String(length=50),nullable=False, unique=False)
    adversaire = db.Column(db.String(length=50),nullable=False, unique=False)
    result = db.Column(db.Integer(),nullable=False, unique=False)
    
    def __repr__(self):
        return f'{self.pseudo} {self.adversaire} {self.result}'
    
    @classmethod
    def find_by_pseudo(cls, nom):
        return cls.query.filter_by(pseudo=nom).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
 
def init_db():
    print("Initialisation de la BDD")
    db.drop_all()
    db.create_all()
    User(pseudo = "puissance4", password_hash = generate_password_hash("1234", method="sha256")).save_to_db()
    print("BDD initialisée")

