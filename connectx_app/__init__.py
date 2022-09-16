from doctest import testfile
from flask import Flask
import os

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

# import sentry_sdk
# from flask import Flask
# from sentry_sdk.integrations.flask import FlaskIntegration

# sentry_sdk.init(
#     dsn="https://fdfe7ca44fa24a889405ccf6ad6a6546@o1303890.ingest.sentry.io/6543419",
#     integrations=[
#         FlaskIntegration(),
#     ],

#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     # We recommend adjusting this value in production.
#     traces_sample_rate=1.0
# )

app = Flask(__name__)


# app.config["SECRET_KEY"] = "very secret"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///..//connectx.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["WTF_CSRF_SECRET_KEY"] = "very secret"
load_dotenv()
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["WTF_CSRF_SECRET_KEY"] = os.getenv("WTF_CSRF_SECRET_KEY")

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

# # insight pour les logs sur azure :
# insight = ApplicationInsights(instrumentation_key='7269625c-4137-42ed-b32b-1d89e1835928')
# insight.init_app(app)

from .routes import *
from .model import *

# from stable_baselines import PPO2
# weight = PPO2.load('connectx_app/agents_weights/ppo2weight')
# import numpy as np
# import random

# def agent_theo(obs, config):
#     # Use the best model to select a column
#     col, _ = weight.predict(np.array(obs['board']).reshape(6,7,1))
#     # Check if selected column is valid
#     is_valid = (obs['board'][int(col)] == 0)
#     # If not valid, select random move. 
#     if is_valid:
#         return int(col)
#     else:
#         return random.choice([col for col in range(config.columns) if obs.board[int(col)] == 0])

