from flask import render_template, redirect, url_for, flash, request
from connectx_app import  app
from kaggle_environments import make, evaluate
from .form import options
from .utils import check_valid_move, winner
from .agent_minmax import my_agent_binary_negmax, check_winner

# Create the game environment
env = make("connectx", debug=True)
# Training agent in first position (player 1) against the default random agent.
trainer = env.train([None, 'random'])
obs = trainer.reset()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/options",methods=['GET', 'POST'])
def chose_options():
    # les options :
    dico_options = {"random":"random","MinMax":my_agent_binary_negmax}
    #choisir les options de la partie
    form = options()
    if form.validate_on_submit():
        print("validation")
        # Training agent in first position (player 1) against the default random agent.
        trainer = env.train([None, dico_options[form.adversaire.data]])
        obs = trainer.reset()
        return redirect(url_for('game'))
    return render_template("options.html", form=form)

@app.route("/game")
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
def winner():
    score = request.args.get('score')
    if score[0]:
        winner = 1
    else:
        winner = 2
    return render_template("winner.html",winner=winner)