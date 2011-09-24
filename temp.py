#!/usr/bin/env python

from flask import Flask
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import abort
from flask import render_template
from flask import flash
import redis
import pprint
import game
import textDisplay
import cPickle as pickle
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'development key'
r = redis.Redis()

@app.route('/', methods=['GET'])
def dashboard():
    game_ids = [str(x) for x in r.smembers('games')]
    game_pickles = []
#    for game_id in game_ids:
#        game_pickles.append(r.get('game:'+game_id+':pickle'))
    game_pickles = [r.get('game:'+game_id+':pickle') for game_id in game_ids]
    game_players = [r.smembers('game:'+game_id+':players') for game_id in game_ids]
    games = [game_ids[i]+':'+str(game_players[i]) for i in range(len(game_players))]

    strings = games
    return render_template('dashboard.html', strings=games)

@app.route('/game/<int:game_id>/')
def game(game_id):
    game = pickle.loads(str(r.get('game:'+str(game_id)+':pickle')))
    d = textDisplay.Display(game)
    s = d.get()
    return '<pre>' + s + '</pre>'

def gamelist():
    game_ids = str(r.smembers('games'))

if __name__ == '__main__':
    app.run()
