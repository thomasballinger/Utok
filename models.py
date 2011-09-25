"""Everything to do with representing data in the database"""
import redis
import cPickle as pickle
from utok import game


r = redis.Redis()

class GameEntry():
    """Represents database information associated with a game."""

    def __init__(self, gid=None):
        if not gid:
            self.gid = str(r.incr('ids:game_entry'))
            r.sadd('game_entries', self.gid)
        else:
            self.gid = str(gid)
            self.game_link = '/game/text/' + str(gid)

    @property
    def name(self):
        return r.hget(self.key, 'name')

    @property
    def game(self):
        return pickle.loads(r.hget(self.key, 'pickle'))

    @property
    def players(self):
        return r.hget(self.key, 'players').split(',')

    @property
    def key(self):
        return 'game_entry:'+self.gid

    def set_name_game_players(self, name, gameObj, players):
        r.hset(self.key, 'name', name)
        r.hset(self.key, 'players', ','.join(players))
        r.hset(self.key, 'pickle', pickle.dumps(gameObj))
        #for player in players:
            #r.sadd(self.players_key, player)
            #if not r.sismember('users', player):
                #r.sadd('users', player)
            #r.sadd('users:'+player, self.game_id)

    def update_game(self, game):
        r.hset(self.key, 'pickle', pickle.dumps(game))

def get_players():
    return []

def get_gameEntries(player=None):
    if player:
        ids = r.smembers('')
        gameEntries =  [GameEntry(gid) for gid in r.smembers('game_entries')]
        return [gameEntry for gameEntry in gameEntries
                if player in gameEntry.players]
    else:
        print [GameEntry(gid) for gid in r.smembers('game_entries')]
        return [GameEntry(gid) for gid in r.smembers('game_entries')]
