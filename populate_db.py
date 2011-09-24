#!/usr/bin/env python

import redis
import utok.game as game
import utok.mapreader as mapreader
import cPickle as pickle
from random import choice
import sys

r = redis.Redis()

def add_game(name, users, mapfile):
    g = mapreader.create_game(users, mapfile)
    s = pickle.dumps(g)
    game_id = str(r.incr('gamecounter'))
    game_pickle_key = 'game:'+game_id+':pickle'
    game_user_set_key = 'game:'+game_id+':players'
    for user in users:
        r.sadd(game_user_set_key, user)
    r.set(game_pickle_key, s)
    r.sadd('games', game_id)
    for user in users:
        if not r.sismember('users', user):
            print 'user DNE, creating'
            r.sadd('users', user)
        r.sadd('users:'+user, game_pickle_key)
        return False
    return True


if __name__ == '__main__':
    r.flushdb()
    r.set('gamecounter', 0)
    users = ['tomb', 'alex', 'ryan', 'mai-anh', 'paula', 'tali']
    for i in range(10):
        name = "".join([choice('asdf;lkjghzxc.v,mnbpoqweorityu') for i in range(10)])
        users = [choice(users) for i in range(2)]
        add_game(name, users, 'utok/worldmap.txt')
