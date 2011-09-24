"""Everything to do with representing data in the database"""
import redis
import cPickle as pickle
from utok import game


r = redis.Redis()

class GameEntry():
    """Represents database information associated with a game."""

    def name(self):
        return r.hget(self.key(), 'name')

    def game(self):
        return pickle.loads(r.hget(self.key(), 'pickle'))

    def players(self):
        return r.hget(self.key(), 'players').split(',')

    def __init__(self, gid=None):
        if not gid:
            self.gid = str(r.incr('ids:game_entry'))
            r.sadd('game_entries', self.gid)
        else:
            self.gid = str(gid)
            self.name = self.name()
            self.players = self.players()
            self.game = self.game()

    def key(self):
        return 'game_entry:'+self.gid

    def set_name_game_players(self, name, gameObj, players):
        r.hset(self.key(), 'name', name)
        r.hset(self.key(), 'players', ','.join(players))
        r.hset(self.key(), 'pickle', pickle.dumps(gameObj))
        #for player in players:
            #r.sadd(self.players_key, player)
            #if not r.sismember('users', player):
                #r.sadd('users', player)
            #r.sadd('users:'+player, self.game_id)

def get_gameEntries(player=None):
    if player:
        raise NotImplemented()
    else:
        print [GameEntry(gid) for gid in r.smembers('game_entries')]
        return [GameEntry(gid) for gid in r.smembers('game_entries')]
