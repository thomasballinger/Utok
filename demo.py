import game
import mapreader
import textDisplay

g = mapreader.create_game(['ryan', 'tomb'], 'worldmap.txt')
d = textDisplay.Display(g)
d.show()

