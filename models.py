"""Everything to do with representing data in the database"""
import redis
import cPickle as pickle
from utok import game


r = redis.Redis()

class GameEntry():
    """Represents database information associated with a game."""
    def __init__(self, game_id=None):
        if not game_id:
            game_id = str(r.incr('gamecounter'))
            r.sadd('games', game_id)
        self.game_id = str(game_id)
        self.pickle_key = 'game:'+self.game_id+':pickle'
        self.players_key = 'game:'+self.game_id+':players'
        self.name_key = 'game:'+self.game_id+':name'

    def get_name(self):
        return r.get(self.name_key)

    def get_game(self):
        return pickle.loads(r.get(self.pickle_key))

    def get_players(self):
        return r.smembers(self.players_key)

    def set_name_game_players(self, name, game, players):
        r.set(self.name_key, name)
        r.set(self.pickle_key, pickle.dumps(game))
        for player in players:
            r.sadd(self.players_key, player)
            if not r.sismember('users', player):
                r.sadd('users', player)
            r.sadd('users:'+player, self.game_id)
