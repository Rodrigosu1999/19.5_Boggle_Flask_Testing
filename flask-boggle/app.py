from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import time

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

# Create instance of Boggle Game
boggle_game = Boggle()


@app.route("/")
def index():
    """
    Root route: Displays the home apge where a button will send us to "/game"
    We restart the board from the session and create "highscore" and "times_played"  
    instances in the session if it's the first time playing
    """
    session["board"] = []
    board = session["board"]
    times_played = session.get("times_played", 0)
    if not times_played:
        session["times_played"] = times_played
    highscore = session.get("highscore", 0)
    if not highscore:
        session["highscore"] = highscore
    return render_template("home.html", board=board,
                           highscore=highscore,
                           times_played=times_played)


@app.route("/game", methods=["POST"])
def start_game():
    """Game route: Board will be created and displayed using the "board.html" template"""
    board = boggle_game.make_board()
    times_played = session["times_played"]
    session["board"] = board
    return render_template("board.html", board=board, times_played=times_played)


@app.route("/score", methods=["POST"])
def post_score():
    """Receive score, update times_played and high score if the previous scroe was broken."""
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    times_played = session["times_played"]
    times_played = times_played + 1
    session["times_played"] = times_played
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)


@app.route("/check/<word>")
def check_guess(word):
    """ Checks if the word is valid or not and send a response to the front-end"""
    board = session["board"]
    word = word
    result = boggle_game.check_valid_word(board, word)
    return jsonify({'result': result})
