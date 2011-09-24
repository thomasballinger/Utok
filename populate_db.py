import redis
import game
import mapreader
import cPickle as pickle
from random import choice
import cmd
import game
import mapreader
import textDisplay
import sys
import cmd
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

class RiskCmd(cmd.Cmd):

    def __init__(self, game):
        self.game = game
        self.d = textDisplay.Display(game)
        cmd.Cmd.__init__(self)

    def do_display(self, args):
        self.d.show()
        print self.game.whosTurn
        print self.game.turnStage
        if self.game.turnStage == 'reinforce':
            print 'left to reinforce:', self.game.reinforcementsToPlace
        return

    def do_reinforce(self, args):
        user = self.game.whosTurn
        try:
            country, num = args.split()
            num = int(num)
        except:
            print 'reinforce country num'
            return
        print self.game.reinforce(country, num, user)

    def do_attack(self, args):
        user = self.game.whosTurn
        try:
            origin, dest, num = args.split()
            num = int(num)
        except:
            print 'attack origin dest num'
            return
        print self.game.attack(origin, dest, num, user)

    def do_freemove(self, args):
        user = self.game.whosTurn
        try:
            origin, dest, num = args.split()
            num = int(num)
        except:
            print 'freemove origin dest num'
            return
        print self.game.freeMove(origin, dest, num, user)

    def do_fortify(self, args):
        user = self.game.whosTurn
        try:
            origin, dest, num = args.split()
            num = int(num)
        except:
            print 'fortify origin dest num'
            return
        print self.game.fortify(origin, dest, num, user)

    def do_pass(self, args):
        user = self.game.whosTurn
        print self.game.skip(user)

    def do_done(self, args):
        return True

    def complete_attack(self, text, line, beginindex, endindex):
        user = self.game.whosTurn
        if not text:
            a = [x for x in self.game.getCountries()]
            return a
        else:
            a = [x for x in self.game.getCountries()
                    and text.lower() in x.lower()]
            return a

    def complete_fortify(self, text, line, beginindex, endindex):
        user = self.game.whosTurn
        if not text:
            a = [x for x in self.game.getCountries()
                    if self.game.isOwned(x, user)]
            return a
        else:
            a = [x for x in self.game.getCountries()
                    if self.game.isOwned(x, user)
                    and text.lower() in x.lower()]
            return a



    def complete_reinforce(self, text, line, beginindex, endindex):
        user = self.game.whosTurn
        if not text:
            a = [x for x in self.game.getCountries()
                    if self.game.isOwned(x, user)]
            return a
        else:
            a = [x for x in self.game.getCountries()
                    if self.game.isOwned(x, user)
                    and text.lower() in x.lower()]
            return a


def load_game(gamekey):
    g = pickle.loads(str(r.get(gamekey)))
    RiskCmd(g).cmdloop()

def main():
    r.flush()
    r.set('gamecounter', 0)
    allusers = ['tomb', 'alex', 'ryan', 'mai-anh', 'paula', 'tali']
    for i in range(10):
        name = "".join([choice('asdf;lkjghzxc.v,mnbpoqweorityu') for i in range(10)])
        users = [choice(allusers) for i in range(2)]
        add_game(name, users, 'worldmap.txt')


if __name__ == '__main__':
    main()
    load_game('game:2:pickle')

