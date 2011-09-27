import game
import sys
from random import shuffle
def create_game(players, mapstring):
    if not mapstring:
        print 'no mapstring found'

    lines = [line+'\n' for line in mapstring.split('\n')]

    bonusesList = []
    nodeNetwork = {}
    mapLines = []
    mapString = ''
    mapFile = ''
    coordinatesMap = {}
    settingsMap = {}

    mode = 'comment'
    for line in lines:
        #print 'was interpreted in mode',mode
        #print line
        if '<end' in line:
            mode = 'comment'
            continue
        if '<start-map>' in line:
            mode = 'map'
            continue
        if '<start-nodeNetwork>' in line:
            mode = 'network'
            continue
        if '<start-bonuses>' in line:
            mode = 'bonus'
            continue
        if '<start-coordinates>' in line:
            mode = 'coordinates'
            continue
        if '<start-mapFile>' in line:
            mode = 'mapFile'
            continue
        if '<start-settings>' in line:
            mode = 'settings'
            continue
        if mode == 'settings':
            inputs = line.split()
            settingsMap[inputs[0]]=inputs[1]
            continue
        if mode == 'comment':
            continue
        if mode == 'coordinates':
            inputs = line.split()
            coordinatesMap[inputs[0]]=(int(inputs[1]),int(inputs[2]))
            continue
        if mode == 'mapFile':
            mapFile = line.split()[0]
            nodeNetwork[countries[0]]=countries[1:len(countries)]
            continue
        if mode == 'network':
            countries = line.split()
            nodeNetwork[countries[0]]=countries[1:len(countries)]
            continue
        if mode == 'bonus':
            bonusesList.append(line.split())
            continue
        if mode == 'map':
            mapLines.append(line)
            continue
        else:
            print 'logic error'
            sys.exit

    mapString = "".join(mapLines)
    shuffle(players)
    countries = list(nodeNetwork)
    shuffle(countries)

    #print 'starting new map with these characteristics:'
    #print 'nodeNetwork',nodeNetwork
    #print 'bonuses',bonusesList
    #print 'players',players
    #print 'map'
    #print mapString

    for bonus in bonusesList:
        for country in bonus[0:-1]:
            if country not in countries:
                print "SPELL YOUR COUNTRIES CORRECTLY!!!"
                print "(bonuses reference one I can't find:",country,')'
                sys.exit()

    g = game.Game(nodeNetwork, players, bonusesList, mapString, coordinatesMap, mapFile, settingsMap)
    #print 'finished making game!'
    rules = g.rules
    i = 0
    for country in countries:
        rules.assignCountry(country,players[i%len(players)])
        if 'initialTroopsInCountries' in settingsMap:
            toAdd = int(settingsMap['initialTroopsInCountries'])-1
            if toAdd > 0:
                rules.addUnits(country,toAdd)
        i+=1
    #print 'turn order:',players
    g._giveReinforcements()
    return g

if __name__ == '__main__':
    create_game(['ryan', 'tomb'], open('data/worldmap.txt').read())
