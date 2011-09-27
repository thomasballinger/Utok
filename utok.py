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
from utok import play_cli
import models


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'development key'

@app.route('/')
def frontpage():
    gameEntries = models.get_gameEntries()
    players = models.get_players()
    return render_template('frontpage.html', gameEntries=gameEntries, players=players)

@app.route('/games/')
def allgames():
    gameEntries = models.get_gameEntries()
    return render_template('allgames.html', gameEntries=gameEntries)

@app.route('/player/<player>/games/')
def player_games(player):
    gameEntries = models.get_gameEntries(player=player)
    return render_template('playergames.html', gameEntries=gameEntries, player=player)

@app.route('/game/<int:game_id>/text', methods=['GET', 'POST'])
def display_game_text(game_id):
    """View and play a risk game in text mode"""
    gameEntry = models.GameEntry(game_id)
    g = gameEntry.game

    if request.method == 'POST':
        cmd = request.form['cmd']
        g = play_cli.run_command_on_game(g, cmd)
        models.GameEntry(game_id).update_game(g)
    else:
        cmd = None

    d = textDisplay.Display(g)
    s = d.get()
    return render_template('textgame.html', gameEntry=gameEntry, game=g, command=cmd, gamestring=s)

@app.route('/game/<int:game_id>/cmd/<path:command>')
def input_command(game_id, command):
    words = command.split('/')

    gameEntry = models.GameEntry(game_id)
    g = gameEntry.game
    g = play_cli.run_command_on_game(g, ' '.join(words))
    gameEntry.update_game(g)

    d = textDisplay.Display(g)
    s = d.get()
    return render_template('textgame.html', gameEntry=gameEntry, game=g, command=' '.join(words), gamestring=s)


@app.route('/game/graphics/<int:game_id>/')
def display_game_graphics(game_id):
    pass

if __name__ == '__main__':
    import populate_db
    populate_db.populate()
    app.run()
