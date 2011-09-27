
# First convert a picture to ascii text, then use this to put numbers on it.
import re

s = open('map4.txt').read()

cors = s[(s.index('<start-cordinates>')+19):(s.index('<end-cordinates>')-1)]
print cors
spots = {}
for line in cors.split('\n'):
    spot, x, y = [x for x in line.split()]
    spots[spot] = (x, y)

print spots

pic = s[(s.index('<start-map>')+12):(s.index('<end-map>')-1)]
safe_pic = re.sub(r'\d','O', pic)
lines = safe_pic.split('\n')
#print s
text_width = len(lines[12])
text_height = len(lines)


import PIL
from PIL import Image
im = Image.open('toConvertOriginal.png')

im_width, im_height = im.size

im_width

for spot in spots:
    new_x = int(int(spots[spot][0])*(float(text_width)/im_width))
    new_y = int(int(spots[spot][1])*(float(text_height)/im_height))-3
    print spot, new_x, new_y
    print 0, new_x, text_width
    print 0, new_y, text_height
    lines[new_y] = lines[new_y][:(new_x-4)]+'  '+('    '+str(spot))[-4:]+'  '+lines[new_y][(new_x+4):]
    lines[new_y+1] = lines[new_y+1][:(new_x-4)]+'  '+(str(spot)+'*****')[:6]+lines[new_y+1][(new_x+4):]

new_pic = '\n'.join(lines)
print pic
print new_pic

f = open('map4labels.txt', 'w')

new_s = s.replace(pic, new_pic)
f.write(new_s)
