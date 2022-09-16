from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash
from connectx_app import  app
from kaggle_environments import make, evaluate
from .form import options, LoginForm
from .utils import check_valid_move, winner
from .agent_minmax import my_agent_binary_negmax, check_winner
#from .agent_ppo2 import agent_theo
from .model import User, Score
from werkzeug.security import generate_password_hash

# Create the game environment
env = make("connectx", debug=True)
# Training agent in first position (player 1) against the default random agent.
trainer = env.train([None, 'random'])
obs = trainer.reset()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(pseudo=form.pseudo.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
 
            flash("Logged in with success", category="success")
            return redirect(url_for('home'))
        else:
            flash("Mail address or password invalid", category="danger")
    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out with success", category="success")
    return redirect(url_for("home"))

@app.route("/newuser", methods=["GET","POST"])
def newuser():
    form=LoginForm()
    if form.validate_on_submit():
        list_user = User.query.filter_by(pseudo=form.pseudo.data).all()
        if list_user==[]:
            User(pseudo = form.pseudo.data, password_hash = generate_password_hash(form.password.data)).save_to_db()
            print(f"user {form.pseudo.data} add to db")
            print(form.password.data)
            return redirect(url_for("home"))
        else:
            flash("User already exists", category="danger")
    return render_template('login.html', form=form)

@app.route("/options",methods=['GET', 'POST'])
@login_required
def chose_options():
    # les options :
    #dico_options = {"random":"random","MinMax":my_agent_binary_negmax,"Super Agent":agent_theo}
    dico_options = {"random":"random","MinMax":my_agent_binary_negmax}

    #choisir les options de la partie
    form = options()
    if form.validate_on_submit():
        print("validation")
        # Training agent in first position (player 1) against the default random agent.
        trainer = env.train([None, dico_options[form.adversaire.data]])
        obs = trainer.reset()
        env.__dict__["agents"]["adversaire"]=form.adversaire.data
        return redirect(url_for('game'))
    return render_template("options.html", form=form)

@app.route("/game")
@login_required
def game():

    move = request.args.get('move')


    #on recupère le board
    obs = env.__dict__["state"][0]["observation"]
    if move==None:
        obs = trainer.reset()
        return render_template("game.html",board=obs["board"])

    # si le move es valide on joue
    if check_valid_move(board=obs["board"],move=int(move)):
        obs, reward, done, info = trainer.step(int(move))
    else:
        #flash("move invalid",category="erreur")
        print("false move")
        return render_template("game.html",board=obs["board"])

    #tant que la partie n'est pas terminée on continue
    if not done:
        return render_template("game.html",board=obs["board"])
    #partie terminée, on reset le board
    else:
        print("la partie est terminée")
        score = check_winner(obs["board"])
        print(score)
        #flash(f"player {win} win !",category="success")
        obs = trainer.reset()
        return redirect(url_for('winner',score=score))

@app.route("/winner")
@login_required
def winner():
    score = request.args.get('score')
    if score[0]=="1":
        winner = 1
        Score(pseudo = "puissance4", adversaire=env.__dict__['agents']['adversaire'],result=1).save_to_db()
    else:
        winner = 2
        Score(pseudo = "puissance4", adversaire=env.__dict__['agents']['adversaire'],result=0).save_to_db()
    
    return render_template("winner.html",winner=winner)