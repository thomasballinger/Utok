#!/usr/bin/env python

import pprint
import cPickle as pickle
from flask import Flask
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import abort
from flask import render_template
from flask import flash
from utok import textDisplay
from utok import game
from models import GameEntry
from models import get_gameObjs

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'development key'
print [l for l in locals().keys() if 'game' in l]

@app.route('/', methods=['GET'])
def dashboard():
    gameObjs = get_gameObjs()
    game_players = [gameObj.get_players() for gameObj in gameObjs]
    game_names = [gameObj.get_name() for gameObj in gameObjs]
    games = [game_names[i]+':'+str(game_players[i]) for i in range(len(game_players))]
    strings = games
    return render_template('dashboard.html', strings=games)

@app.route('/game/<int:game_id>/')
def display_game(game_id):
    g = GameEntry(game_id).get_game()
    d = textDisplay.Display(g)
    s = d.get()
    return '<pre>' + s + '</pre>'

if __name__ == '__main__':
    import populate_db
    populate_db.populate()
    app.run()
