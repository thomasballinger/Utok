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
from models import GameEntry
from models import get_gameObjs


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'development key'

@app.route('/', methods=['GET'])
def dashboard():
    gameEntries = get_gameObjs()
    game_players = [gameEntry.get_players() for gameEntry in gameEntries]
    game_names = [gameEntry.get_name() for gameEntry in gameEntries]
    games = [game_names[i]+':'+str(game_players[i]) for i in range(len(game_players))]
    print games
    print gameEntries
    print dir(gameEntries[0])
    return render_template('allgames.html', gameEntries=gameEntries)

@app.route('/game/text/<int:game_id>/', methods=['GET', 'POST'])
def display_game(game_id):
    g = GameEntry(game_id).get_game()

    if request.method == 'POST':
        cmd = request.form['cmd']
        g = play_cli.run_command_on_game(g, cmd)
        #At this point we need to save...
        GameEntry(game_id)

    else:
        cmd = None
    d = textDisplay.Display(g)
    s = d.get()
    return '<pre>' + (cmd+'\n' if cmd else '') + g.getWhosTurn() + '\n' + g.getTurnStage() + '\n' + s + '</pre>'+ """<form action="/game/text/"""+str(game_id)+"""/" method="post">
  Command: <input type="text" name="cmd" /><br />
      <input type="submit" value="Submit" />
      </form>"""

if __name__ == '__main__':
    import populate_db
    populate_db.populate()
    app.run()
