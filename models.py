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
        self.game_link = '/game/'+self.game_id

    def get_name(self):
        self.name = r.get(self.name_key)
        return self.name

    def get_game(self):
        self.game = pickle.loads(r.get(self.pickle_key))
        return self.game

    def get_players(self):
        self.players = r.smembers(self.players_key)
        return self.players

    def set_name_game_players(self, name, game, players):
        self.name = name
        self.game = game
        self.players = players
        r.set(self.name_key, name)
        r.set(self.pickle_key, pickle.dumps(game))
        for player in players:
            r.sadd(self.players_key, player)
            if not r.sismember('users', player):
                r.sadd('users', player)
            r.sadd('users:'+player, self.game_id)

def get_gameObjs(player=None):
    if player:
        raise NotImplemented()
    else:
        print [GameEntry(game_id) for game_id in r.smembers('games')]
        return [GameEntry(game_id) for game_id in r.smembers('games')]
