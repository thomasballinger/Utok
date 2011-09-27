#!/usr/bin/env python
"""Wipes, populates the database as we might expect to find it."""
import redis
import utok.game as game
import utok.mapreader as mapreader
import cPickle as pickle
from random import choice, randint, shuffle
import sys
import os
import models

r = redis.Redis()

def add_map(name, mapfile):
    mapstring = open(mapfile).read()
    m = models.MapEntry()
    m.set_string_and_name(mapstring, name)

def add_game(name, users, mapEntry):
    mapstring = mapEntry.string
    gObj = mapreader.create_game(users, mapstring)
    gameEntry = models.GameEntry()
    gameEntry.set_name_game_players(name, gObj, users)
    return True

def populate():
    r.flushdb()
    r.set('ids:game_entry', 0)
    r.set('ids:map_entry', 0)
    add_map('Atlantic Map', 'utok/data/worldmap.txt')
    add_map('Office Map', 'utok/data/map2.txt')
    add_map('Southeast Asia Map', 'utok/data/map4labels.txt')
    mapEntry_ids = range(1,4)
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
        mapEntry_id = choice(mapEntry_ids)
        add_game(name, users, models.MapEntry(mapEntry_id))

if __name__ == '__main__':
    populate()
