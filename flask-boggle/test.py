from unittest import TestCase
import app
from app import app
from flask import session, request, render_template, jsonify, Flask
from boggle import Boggle
from random import choice
import string


class FlaskTests(TestCase):

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("<button>Click to start game</button>", html)
            self.assertIn("board", session)
            self.assertEqual(session.get("highscore"), 0)
            self.assertEqual(session.get("times_played"), 0)

    def test_gamepage(self):
        """Make sure information is in the session and HTML board is displayed"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["times_played"] = 300
            res_get = client.get("/")
            res = client.post("/game")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Enter your guess", html)
            self.assertEqual(session["times_played"], 300)

    def test_word(self):
        """Test if word is valid by modifying the board in the session"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [
                    ["H", "E", "L", "L", "O"],
                    ["J", "K", "L", "U", "T"],
                    ["W", "Q", "H", "G", "G"],
                    ["E", "R", "T", "Y", "U"],
                    ["B", "M", "P", "O", "I"]]
        res = client.get("/check/hello")
        self.assertEqual(res.json['result'], 'ok')
        res2 = client.get("/check/tyu")
        self.assertEqual(res2.json['result'], 'not-word')
        res3 = client.get("/check/yes")
        self.assertEqual(res3.json['result'], 'not-on-board')
