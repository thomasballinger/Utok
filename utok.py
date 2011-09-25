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

@app.route('/game/text/<int:game_id>/', methods=['GET', 'POST'])
def display_game(game_id):
    g = models.GameEntry(game_id).game

    if request.method == 'POST':
        cmd = request.form['cmd']
        g = play_cli.run_command_on_game(g, cmd)
        models.GameEntry(game_id).update_game(g)
    else:
        cmd = None

    d = textDisplay.Display(g)
    s = d.get()
    return '<pre>' + (cmd+'\n' if cmd else '') + g.getWhosTurn() + '\n' + g.getTurnStage() + '\n' + s + '\n' + "Ex:\nreinforce Canada 3\nattack Canada USA 3\nfreemove Canada USA 1\nfortify Canada Greenland 1" + '\n' '</pre>'+ """<form action="/game/text/"""+str(game_id)+"""/" method="post">
  Command: <input type="text" name="cmd" /><br />
      <input type="submit" value="Submit" />
      </form>"""

if __name__ == '__main__':
    import populate_db
    populate_db.populate()
    app.run()
