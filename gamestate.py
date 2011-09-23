class Board:
    """Represents a game and its current state.

    self.nodeNetwork is of format {"USA":["Austria"],"Austria":[0,1,2],"Uzbekistan":[0,1,2],"Jamaica":["USA"]}
    self.countryStates is of format {"USA":["PlayerName", 10],"Austria":["Player2Name, 3]}
    Any information can be stored in self.countryStates; Board object doesn't care what."""

    def __init__(self, nodeNetwork=None, countryStates=None):
        self.nodeNetwork = {}
        self.countryStates = {}
        if nodeNetwork:
            self.nodeNetwork = nodeNetwork
        if countryStates:
            self.countryStates = countryStates

    def addCountry(self, name, connections=[]):
        if name in self.countryStates:
            print 'A Country of that name already exists'
            return False
        self.countryStates[name] = [None]
        self.nodeNetwork[name] = connections

    def getCountries(self):
        return self.countryStates.keys()

    def bidirectionalize(self):
        for country in self.getCountries():
            if self.nodeNetwork[country]:
                for connection in self.nodeNetwork[country]:
                    if connection in self.countryStates and country not in self.nodeNetwork[connection]:
                        self.nodeNetwork[connection]=self.nodeNetwork[connection]+[country]

    def getConnections(self,country):
        if not country in self.nodeNetwork:
            print "country not found that you want the connections of"
        else:   
            connectionsList = []
            if not self.nodeNetwork[country]:
                return connectionsList 
            else:
                for connection in self.nodeNetwork[country]:
                    if connection in self.countryStates:
                        connectionsList.append(connection)
                    else:
                        print connection,'not found in list of countries, but connected'
                return connectionsList

    def getCountryState(self,country):
        if country not in self.countryStates:
            print 'No Country by that name exists', country
            print 'existing countries:',self.countryStates
            return None
        return self.countryStates[country] 
    
    def setCountryState(self,country,state):
        if country not in self.countryStates:
            print 'No Country by that name exists', country
            print 'existing countries:',self.countryStates
            return False
        else:
            self.countryStates[country]=state
            return True

    def getCountryStates(self):
        return self.countryStates

    def isTouching(self,fromCountry,toCountry):
        if fromCountry not in self.countryStates or toCountry not in self.countryStates:
            print 'at least one of those countries is no good'
            return False
        if toCountry in self.nodeNetwork[fromCountry]:
            return True
        else:
            return False

    def getAdjacentCountries(self, country):
        if country not in self.countryStates:
            print 'country is no good'
            return False
        return self.nodeNetwork[country]

if __name__ == '__main__':
    game = Board()
    game.addCountry("USA")
    game.addCountry("Mexico",["USA"])
    game.addCountry("Canada",["USA","Alaska"])
    print game.getCountries()
    print game.getConnections("USA")
    game.bidirectionalize()
    print game.getCountries()       
    print game.getConnections("USA")
    print game.getCountryState("USA")
    print game.setCountryState("USA",['tom',12])
    print game.getCountryState("USA")
