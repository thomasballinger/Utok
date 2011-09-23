from gamestate import Board
from random import randint
class Rules():
    game = None
    def __init__(self,players=None,map=None):
        if players:
            self.players = players
        else:
            self.players = ['tom',"alex"]
        self.board = Board()
        curTurn = self.players[0]
        if map:
            self.makeMap(map)
    
    def getPlayersAlive(self):
        """returns a list of players with units on the board"""
        playersAlive = set([])
        for country in self.getCountries():
            playersAlive = playersAlive.union(set([self.board.getCountryState(country)[0]]))
        return list(playersAlive)
     
    def attack(self, fromCountry, toCountry, howMany):
        fromState = self.board.getCountryState(fromCountry)[:]
        toState = self.board.getCountryState(toCountry)[:]
        if fromState[0] == toState[0]:
            print("attacking country owned by same person")
            return False
        if fromState[1]<2:
            print("too few to attack from that country")
            return False
        if fromState[1]<howMany+1:
            print("too few to attack from that country with that many")
            return False
        if toState[1]<1:
            print("error; attacked country has zero armies")
            return False
        output = {'captured':False,'from':fromCountry,'to':toCountry}
        attackersKilled = 0
        defendersKilled = 0
        attackRolls = []
        defenseRolls = []
        defenders = min(2,toState[1])
        numCasualties = min(howMany,defenders)
        for i in range(howMany):
            attackRolls.append(randint(1,6))
        attackRolls.sort()
        output['attack'] = attackRolls[:]
        for i in range(defenders): 
            defenseRolls.append(randint(1,6))
        defenseRolls.sort()
        output['defense'] = defenseRolls[:]
        for i in range(numCasualties):
            if max(attackRolls)>max(defenseRolls):
                defendersKilled +=1
            else:
                attackersKilled +=1
            attackRolls.remove(max(attackRolls))
            defenseRolls.remove(max(defenseRolls))
        output['attackersKilled']=attackersKilled
        output['defendersKilled']=defendersKilled
        fromState = [fromState[0], fromState[1] - attackersKilled]
        toState   = [toState[0],   toState[1]   - defendersKilled]
        self.board.setCountryState(fromCountry, fromState)
        self.board.setCountryState(toCountry  , toState)
        if toState[1] == 0:
            self.board.setCountryState(toCountry,[fromState[0], howMany - attackersKilled])
            self.board.setCountryState(fromCountry,[fromState[0], fromState[1]-howMany])
            output['captured']=True
        return output

    def addUnits(self, toCountry, howMany):
        state = self.board.getCountryState(toCountry)
        self.board.setCountryState(toCountry,[state[0],state[1]+howMany])
        return True

    def makeMap(self, mapOfCountryConnections):
        """List should be in format {"USA":["Mexico","Canada"], etc.]"""
        for country in mapOfCountryConnections:
            self.board.addCountry(country, mapOfCountryConnections[country])
    
    def moveUnits(self, fromCountry, toCountry, howMany):
        if not self.board.isTouching(fromCountry, toCountry):
            print "those countries don't touch!"
            return False
        fromState = self.board.getCountryState(fromCountry)
        toState = self.board.getCountryState(toCountry)
        if howMany+1 > fromState[1]:
            print "not enough in fromState to move that many"
            return False
        self.board.setCountryState(fromCountry,[fromState[0],fromState[1]-howMany])
        self.board.setCountryState(toCountry,[toState[0],toState[1]+howMany])
        return True

    def isOwned(self, country, player):
        if player not in self.players:
            print 'player dne'
            return False
        if self.board.getCountryState(country)[0] == player:
            return True
        else:
            return False

    def getStates(self):
        return self.board.getCountryStates()
    
    def allOwned(self, listOfCountries, player):
        if player not in self.players:
            print 'player dne'
            return False
        for country in listOfCountries:
            if not self.isOwned(country, player):
                return False
        return True
        
    def assignCountry(self, country, player):
        if player not in self.players:
            print 'player dne'
            return False
        self.board.setCountryState(country,[player, 1])
    
    def getOwner(self, country):
        return self.board.getCountryState(country)[0]

    def getTroops(self, country):
        return self.board.getCountryState(country)[1]

    def getCountries(self):
        return self.board.getCountries()

    def getAdjacentCountries(self, country):
        return self.board.getAdjacentCountries(country)

    def isTouching(self, country1, country2):
        return self.board.isTouching(country1, country2) 
if __name__ == '__main__':
    rules = Rules()
    rules.makeMap({"USA":["Canada","Mexico"],"Canada":['USA'],'Mexico':['USA']})
    print rules.board.getCountries()
    rules.assignCountry('USA','tom')
    rules.assignCountry('Canada','tom')
    rules.assignCountry('Mexico','alex')
    print rules.board.countryStates
    rules.addUnits('USA',3)
    rules.addUnits('Canada',4)
    rules.moveUnits('Canada','USA',1)
    print rules.board.countryStates
    print rules.attack('USA','Mexico',3)
    print rules.board.countryStates


