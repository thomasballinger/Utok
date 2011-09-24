#!/usr/bin/env python
"""Wipes, populates the database as we might expect to find it."""
import redis
import utok.game as game
import utok.mapreader as mapreader
import cPickle as pickle
from random import choice
import sys
import os
from models import GameEntry

r = redis.Redis()

def add_game(name, users, mapfile):
    g = mapreader.create_game(users, mapfile)
    gObj = GameEntry()
    gObj.set_name_game_players(name, g, users)
    return True

def populate():
    r.flushdb()
    r.set('gamecounter', 0)
    all_users = ['tomb', 'alex', 'ryan', 'mai-anh', 'paula', 'tali']
    for i in range(10):
        name = "".join([choice('asdf;lkjghzxc.v,mnbpoqweorityu') for i in range(10)])
        users = [choice(all_users) for i in range(3)]
        add_game(name, users, 'utok/worldmap.txt')

if __name__ == '__main__':
    populate()
