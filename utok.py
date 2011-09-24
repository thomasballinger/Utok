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
from models import get_gameEntries

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'development key'

@app.route('/', methods=['GET'])
def dashboard():
    #gameEntries = [GameEntry(x) for x in r.smembers('game_entries')]
    #players = [gameEntry.players() for gameEntry in gameEntries]
    #names = [gameEntry.name() for gameEntry in gameEntries]
    #games = [names[i]+':'+str(players[i]) for i in range(len(players))]
    #return render_template('dashboard.html', strings=names)
    gameEntries = get_gameEntries()
    return render_template('allgames.html', gameEntries=gameEntries)

@app.route('/game/<int:game_id>/')
def display_game(game_id):
    g = GameEntry(game_id).game()
    d = textDisplay.Display(g)
    s = d.get()
    return '<pre>' + s + '</pre>'

if __name__ == '__main__':
    import populate_db
    populate_db.populate()
    app.run()
