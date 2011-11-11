from rules import Rules

class Game:
    """Represents the current state of a risk game

    Includes full specification of the map, rules, players and current game state.
    Includes the NAME ONLY of the graphical map file, along with coordinates of territories on this map."""
    def __init__(self,nodeNetwork=None, players={}, bonuses=[], mapString=None, coordinates=None, mapFile=None, settingsMap={}):
        self.mapFile = mapFile
        self.coordinates = coordinates
        self.rules = Rules(map=nodeNetwork, players=players)
        self.whosTurn = self.rules.players[0]
        self.turnStage = 'reinforce'
        self.reinforcementsToPlace = {}
        self.lastAttack = None
        self.fortifies = 1
        if 'fortifies' in settingsMap:
            self.fortifies = int(settingsMap['fortifies'])
        self.fortifiesLeft = self.fortifies
        self.bonuses=bonuses
        for player in self.rules.players:
            self.reinforcementsToPlace[player]=0
        self.reinforced = False
        if not mapString and not (coordinates and mapFile):
            print "this game has no pretty visualization available"
        self.mapString = mapString
        self.settingsMap = settingsMap
        self.fog = False
        if 'fog' in self.settingsMap:
            self.fog = self.settingsMap['fog']
        self.selectionList = []
        self.showAttackResult = False
        self.justMadeFreeMove = False

    def _giveReinforcements(self):
        if self.reinforced == True:
            return False
        else:
            self.reinforced = True
            self.reinforcementsToPlace[self.whosTurn]=self.getDeservedReinforcements(self.whosTurn)

    def player_getFortifiesLeft(self,player):
        """Returns 0 if not the current players turn, otherwise the number of fortifying moves left in the turn"""
        if self.whosTurn != player:
            return 0
        else:
            return self.fortifiesLeft

    def updateTurn(self):
        if self.whosTurn not in self.playersAlive and self.turnStage != 'fortify': # lose condition
            self.turnStage = 'fortify'
            self.fortifiesLeft = 0
            self.updateTurn()
        if len(self.playersAlive) == 1 and self.playersAlive[0] == self.whosTurn:
            self.turnStage = 'reinforce'  # win condition
            self.reinforcementsToPlace[self.whosTurn] = 1
        elif self.turnStage == 'reinforce' and self.reinforcementsToPlace[self.whosTurn]==0:
                self.turnStage = 'attacks'
        elif (self.turnStage == 'fortify' and self.fortifiesLeft == 0) or self.whosTurn not in self.playersAlive:
            players = self.players  # begin new turn
            for i in range(len(players)):
                if self.whosTurn == players[i]:
                    self.whosTurn = players[(i+1)%len(players)]
                    self.reinforcementsToPlace[self.whosTurn] = self.getDeservedReinforcements(self.whosTurn)
                    self.fortifiesLeft = self.fortifies
                    self.turnStage = 'reinforce'
                    self.selectionList = []
                    self.lastAttack = None
                    self.justMadeFreeMove = False
                    self.updateTurn()
                    break

    def getDeservedReinforcements(self,player):
        count = 0
        countriesPerTroop = 3
        if 'countriesPerTroop' in self.settingsMap:
            countriesPerTroop = int(self.settingsMap['countriesPerTroop'])
        countries = self.countries
        for country in countries:
            if self.isOwned(country, player):
                count +=1
        for bonus in self.bonuses:
            deserveBonus = True
            for country in bonus[0:-1]:
                if not self.isOwned(country,player):
                    deserveBonus = False
            if deserveBonus:
                count+=(countriesPerTroop*int(bonus[-1]))
        return max(int(count/countriesPerTroop),3)


    def player_reinforce(self,country,howMany,player):
        pass
        # check for correct turn, right time, have reinforcements, etc.
        if type(player) != type('string') and type(player) != type(u'string'):
            return False
        if self.whosTurn != player:
            return False
        if self.turnStage != 'reinforce':
            return False
        if self.reinforcementsToPlace[player]<=0:
            return False
        if type(country) != type('string') and type(country) != type(u'string'):
            return False
        if country not in self.countries:
            return False
        if not self.isOwned(country, player):
            return False
        if type(howMany) != type(1):
            return False
        if howMany>self.reinforcementsToPlace[player]:
            return False
        if howMany < 0:
            return False
        if self.rules.addUnits(country, howMany):
            self.reinforcementsToPlace[player]=self.reinforcementsToPlace[player]-howMany
            self.updateTurn()
            return True
        else:
            return False

    def player_reinforce_availableCountries(self, player):
        """Returns countries available to be reinforced"""
        if self.reinforcementsToPlace[player]<=0:
            return []
        return self.getCountriesOwned(player)

    def player_reinforce_availableNumbers(self, player, country):
        return range(1, self.getReinforcements(player)+1)

    def player_attack(self,fromCountry,toCountry,howMany,player):
        if self.whosTurn != player:
            #raise Exception, 'player error'
            return False
        if self.turnStage != 'attacks':
            #raise Exception, 'its not in the attack stage'
            return False
        if type(fromCountry)!=type('string') and type(fromCountry) != type(u'string'):
            #raise Exception, 'from country is not a string'
            return False
        if type(toCountry)!=type('string') and type(fromCountry) != type(u'string'):
            #raise Exception, 'to country is not a string'
            return False
        if type(player)!=type('string') and type(player) != type(u'string'):
            #raise Exception, 'player is not a string'
            return False
        if type(howMany)!=type(1):
            #raise Exception, 'how many is not a number'
            return False
        if not fromCountry in self.countries:
            #raise Exception, 'from country is not a country'
            return False
        if not toCountry in self.countries:
            #raise Exception, 'to country is not a country'
            return False
        if not player in self.players:
            #raise Exception, 'player is not in this game'
            return False
        if not self.isTouching(fromCountry, toCountry):
            #raise Exception, 'those countries do not touch'
            return False
        if not self.isOwned(fromCountry, player):
            #raise Exception, 'attacker does not own from country'
            return False
        if self.isOwned(toCountry, player):
            #raise Exception, 'attacker owns destination country'
            return False
        if self.getTroops(fromCountry) < howMany+1:
            #raise Exception, 'not enough troops in fromCountry'
            return False
        if howMany < 1:
            #raise Exception, 'attacking with less than one troop'
            return False
        output = self.rules.attack(fromCountry,toCountry,howMany)
        if not output:
            raise Exception, 'rules.attack failed'
            return False
        else:
            self.lastAttack = output
            self.updateTurn()
            self.showAttackResult = True
            self.justMadeFreeMove = False
            return output

    def player_attack_availableFroms(self, player):
        player_countries = self.getCountriesOwned(player)
        return [c for c in player_countries if (self.getTroops(c) > 1 and self.getAdjacentAttacks(c))]

    def player_attack_availableTos(self, player, from_):
        return self.getAdjacentAttacks(from_)

    def player_attack_availableNumbers(self, player, from_, to):
        return range(1, min(self.getTroops(from_), 4))

    def player_freeMove(self,fromCountry,toCountry,howMany,player):
        if type(player)!=type('string') and type(player) != type(u'string'):
            return False
        if self.whosTurn != player:
            return False
        if self.turnStage != 'attacks':
            return False
        if type(fromCountry)!=type('string') and type(fromCountry) != type(u'string'):
            return False
        if type(toCountry)!=type('string') and type(toCountry) != type(u'string'):
            return False
        if type(howMany)!=type(1):
            return False
        if not self.lastAttack['captured']:
            return False
        if fromCountry != self.lastAttack['from']:
            return False
        if toCountry != self.lastAttack['to']:
            return False
        if not player in self.players:
            return False
        if not self.isTouching(fromCountry, toCountry):
            return False
        if not self.isOwned(fromCountry, player):
            return False
        if not self.isOwned(toCountry, player):
            return False
        if self.getTroops(fromCountry) < howMany+1:
            return False
        if self.rules.moveUnits(fromCountry, toCountry, howMany):
            self.updateTurn()
            self.showAttackResult = False
            self.justMadeFreeMove = True
            return True
        else:
            raise Exception, 'rules failed'
            return False

    def player_freemove_availableNumbers():
        return range(1, self.getTroops(from_))

    def player_fortify(self,fromCountry,toCountry,howMany,player):
        if type(player)!=type('string') and type(player) != type(u'string'):
            return False
        if self.whosTurn != player:
            return False
        if self.turnStage != 'fortify' and self.turnStage != 'attack':
            return False
        if self.fortifiesLeft <1:
            return False
        if type(fromCountry)!=type('string') and type(fromCountry) != type(u'string'):
            return False
        if type(toCountry)!=type('string') and type(toCountry) != type(u'string'):
            return False
        if type(howMany)!=type(1):
            return False
        if not self.isTouching(fromCountry, toCountry):
            return False
        if not self.isOwned(fromCountry, player):
            return False
        if not self.isOwned(toCountry, player):
            return False
        if self.getTroops(fromCountry) < howMany+1:
            return False
        if self.rules.moveUnits(fromCountry, toCountry, howMany):
            self.turnStage = 'fortify'
            self.fortifiesLeft -=1
            self.updateTurn()
            return True
        else:
            return False

    def player_fortify_availableFroms(self, player):
        return [c for c in self.getCountriesOwned(player) if
                (self.getTroops(c) > 1 and any(
                [c2 for c2 in self.getAdjacentCountries(c)
                    if self.isOwned(c2, player)]))
                ]

    def player_fortify_availableTos(self, player, from_):
        return [c for c in self.getAdjacentCountries(from_) if self.isOwned(c, player)]

    def player_fortify_availableNumbers(self, player, from_, to):
        return range(1, self.getTroops(from_))

    def player_skip(self, player):
        if self.whosTurn != player:
            return False
        else:
            if self.turnStage == 'reinforce':
                if self.reinforcementsToPlace[self.whosTurn] <= 0:
                    self.updateTurn()
                else:
                    return False
            elif self.turnStage == 'attacks':
                self.turnStage = 'fortify'
                self.showAttackResult = False
                self.updateTurn()
                return True
            elif self.turnStage == 'fortify':
                self.fortifiesLeft = 0
                self.updateTurn()
                return True
            else:
                return False

    def player_getLastAttack(self,player):
        if self.whosTurn != player:
            return False
        else:
            return self.lastAttack

    def getReinforcements(self,player):
        """Returns the number of reinforcements the player has yet to place"""
        return self.reinforcementsToPlace[player]

    def getCoordinates(self, country):
        return self.coordinates[country]

    def getCountriesOwned(self, player):
        return [c for c in self.countries() if self.isOwned(c, player)]

    def getAdjacentAttacks(self, country):
        possibleAttacks = []
        player = self.getOwner(country)
        for adjCountry in self.getAdjacentCountries(country):
            if self.getOwner(adjCountry) != player:
                possibleAttacks.append(adjCountry)
        return possibleAttacks

    def getAdjacentCountries(self,country):
        return self.rules.getAdjacentCountries(country)

    def isTouching(self, country1, country2):
        return self.rules.isTouching(country1, country2)

    def isOwned(self, country, player):
        return self.rules.isOwned(country, player)

    def setSelection(self, list):
        self.selectionList = list[:]

    def getSelection(self):
        return self.selectionList[:]

    def clearSelection(self):
        self.selectionList = []

    def isCountry(self,country):
        return country in self.countries

    def getOwner(self, country):
        return self.rules.getOwner(country)

    def getTroops(self, country):
        return self.rules.getTroops(country)

    def getFortifies(self):
        return self.fortifies

    @property
    def countries(self):
        return self.rules.board.getCountries()

    @property
    def players(self):
        return self.rules.players

    @property
    def playersAlive(self):
        return self.rules.getPlayersAlive()

    @property
    def states(self):
        return self.rules.board.getCountryStates()

# debugging tools
mymap = {'USA':['Canada','Mexico'],'Canada':['USA','Greenland'],'Mexico':['USA','Cuba','England'],'Cuba':['Mexico'],'Greenland':['Canada','Iceland'],'Iceland':['England','Greenland'],'England':['Mexico','Iceland'],'Alaska':['Canada']}

def demo():
    game = Game(nodeNetwork=mymap, players=['tom', 'alex'], mapString="".join((open('data/worldmap.txt').readlines()[32:51])))

    rules = game.rules
    print 'assign usa to tom',rules.assignCountry('USA','tom')
    print 'assign canada to tom',rules.assignCountry('Canada','tom')
    print 'assign mexico to alex',rules.assignCountry('Mexico','alex')
    print 'assign cuba to alex',rules.assignCountry('Cuba','alex')
    print 'add units to usa',rules.addUnits('USA',3)
    print 'add units to canada',rules.addUnits('Canada',4)
    print 'add units to canada',rules.addUnits('Mexico',4)
    print 'move unit from canada to usa',rules.moveUnits('Canada','USA',1)
    raw_input()
    print game.whosTurn
    print game.turnStage
    game.reinforcementsToPlace['tom'] = 3
    print 'reinforce usa with 3 for tom:',
    print game.player_reinforce('USA', 3, 'tom')
    print 'attack mexico with 2 for tom:',
    print game.player_attack('USA','Mexico', 2, 'tom')
    print 'freemove from usa to mexico with 1 for tom:',
    print game.player_freeMove('USA', 'Mexico', 1, 'tom')
    print 'skip:',
    print game.player_skip('tom')
    print 'fortify usa from canada with 1:',
    print game.player_fortify('Canada','USA',1,'tom')
    print 'reinforce cuba once',game.player_reinforce('Cuba',1,'alex')
    print 'reinforce cuba twice',game.player_reinforce('Cuba',2,'alex')
    raw_input()

    print 'whosTurn',game.whosTurn
    print 'turnStage',game.turnStage
    print 'toReinforce',game.reinforcementsToPlace

    print game.states

if __name__=='__main__':
    demo()
