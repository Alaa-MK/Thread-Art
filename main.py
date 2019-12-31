from PIL import Image, ImageDraw
import numpy as np
import math
import random

W = 64
H = 64
THRESHOLD = 0.72
DENSITY = 0.99

def line_equation(line):    #assume slope is not infinite
    A, B = line
    m=(A[1]-B[1])/(A[0]-B[0])
    c=A[1]-m*A[0]
    return m, c

def line_probability(line, pixels):
    cost = 0
    count = 0
    if (line[0][0] == line[1][0]):
        for y in range(min(line[0][1], line[1][1]), max(line[0][1], line[1][1])):
            x = line[0][0]
            cost+=255-pixels[x][y]
            count+=1   
    else:
        m, c = line_equation(line)
        for x in range(min(line[0][0], line[1][0]), max(line[0][0], line[1][0])):
            y = math.floor(m*x+c)
            if y == len(pixels[0]):
                continue
            cost+=255-pixels[x][y]
            count+=1
    if count == 0: 
        return 0
    return cost/count/255   #gives a value in [0,1]

def get_lines_to_draw(all_lines, pixels):
    to_draw = []
    for line in all_lines:
        p = line_probability(line, pixels)
        if random.random() < p * DENSITY and p > THRESHOLD:
            to_draw.append(line)
    return to_draw

def draw_image (lines_to_draw, size):
    factor = 32
    new_size = (size[0]*factor, size[1]*factor)
    img = Image.new('L', new_size)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0,0), new_size], fill=255)
    for line in lines_to_draw:
        temp = [(line[0][0]*factor, line[0][1]*factor), (line[1][0]*factor, line[1][1]*factor)]
        draw.line(temp, fill=0)
    return img.rotate(90).transpose(Image.FLIP_TOP_BOTTOM)
    
    


def main():
    img = Image.open('big.png').convert('L')
#    img.show()
    img_width, img_height = img.size
    pixels = np.reshape(img.getdata(), img.size)
    
    pins = [(math.floor(x*img_width/W),0) for x in range(0, W)] \
    + [(math.floor(x*img_width/W),img_height) for x in range(0, W)] \
    + [(0,math.floor(y*img_height/H)) for y in range(0, H)] \
    + [(img_width, math.floor(y*img_height/H)) for y in range(0, H)]
    
#    print(pins)
    
    lines = [(x,y) for x in pins for y in pins if not(x[0] == y[0] and x[0] in(0, img_width)) and not(x[1]==y[1] and x[1] in (0, img_height))]
#    print(lines)
    
    lines_to_draw = get_lines_to_draw(lines, pixels)
    print(len(lines_to_draw))
    result = draw_image(lines_to_draw, img.size)
    result.show()
    
    
    
    

if __name__=='__main__':
    main()