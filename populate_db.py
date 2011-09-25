#!/usr/bin/env python
"""Wipes, populates the database as we might expect to find it."""
import redis
import utok.game as game
import utok.mapreader as mapreader
import cPickle as pickle
from random import choice, randint, shuffle
import sys
import os
from models import GameEntry

r = redis.Redis()

def add_game(name, users, mapfile):
    gObj = mapreader.create_game(users, mapfile)
    g = GameEntry()
    g.set_name_game_players(name, gObj, users)
    return True

def populate():
    r.flushdb()
    r.set('ids:game_entry', 0)
    all_users = ['tomb', 'alex', 'ryan', 'mai-anh', 'paula', 'tali']
    for i in range(10):
        vowels = 'aeiouy'
        consonants = list('bbcdffghjklmmnnpqrrsssttvwxz') + ['th', 'sh', 'ch', ]
        def syl():
            case = randint(0, 2)
            return (choice(consonants) if case else '') + choice(vowels) + (choice(consonants) if (case - 1) else '')
        name = "".join([syl() for i in range(randint(1, 5))]).title()
        shuffle(all_users)
        users = all_users[:randint(2,5)]
        add_game(name, users, 'utok/worldmap.txt')

if __name__ == '__main__':
    populate()
