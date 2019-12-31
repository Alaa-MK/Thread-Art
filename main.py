from PIL import Image, ImageDraw
import numpy as np
import math
import random

#PARAMETERS
W = 64                  #number of pins on the horizontal size
H = 64                  #number of pins on the veritcal size
THRESHOLD = 0.72        #minimum matching percentage for a line to be considered in drawing
DENSITY = 0.99          #controls the density of the lines in the picture
SCALING_FACTOR = 16     #the output image size is SCALING_FACTOR * input_image.size()

def line_equation(line):    #assume slope is not infinite
    A, B = line
    m=(A[1]-B[1])/(A[0]-B[0])
    c=A[1]-m*A[0]
    return m, c

def line_gain(line, pixels):     #evaluates to a value between 0 and 1 indicating how matching a line is in this position
    gain = 0
    count = 0
    if (line[0][0] == line[1][0]):
        for y in range(min(line[0][1], line[1][1]), max(line[0][1], line[1][1])):
            x = line[0][0]
            gain+=255-pixels[x][y]
            count+=1   
    else:
        m, c = line_equation(line)
        for x in range(min(line[0][0], line[1][0]), max(line[0][0], line[1][0])):
            y = math.floor(m*x+c)
            if y == len(pixels[0]):
                continue
            gain+=255-pixels[x][y]
            count+=1
    if count == 0: 
        return 0
    return gain/count/255

def get_lines_to_draw(all_lines, pixels):
    to_draw = []
    for line in all_lines:
        p = line_gain(line, pixels)
        if random.random() < p * DENSITY and p > THRESHOLD:
            to_draw.append(line)
    return to_draw

def draw_image (lines_to_draw, size, factor):
    new_size = (size[0]*factor, size[1]*factor)
    img = Image.new('L', new_size)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0,0), new_size], fill=255)
    for line in lines_to_draw:
        temp = [(line[0][0]*factor, line[0][1]*factor), (line[1][0]*factor, line[1][1]*factor)]
        draw.line(temp, fill=0)
    return img.rotate(90).transpose(Image.FLIP_TOP_BOTTOM)
    
    


def main():
    image_name = 'the-mona-lisa.jpg'
    img = Image.open('examples/' + image_name).convert('L')
    img_width, img_height = img.size
    pixels = np.reshape(img.getdata(), img.size)
    
    pins = [(math.floor(x*img_width/W),0) for x in range(0, W)] \
    + [(math.floor(x*img_width/W),img_height) for x in range(0, W)] \
    + [(0,math.floor(y*img_height/H)) for y in range(0, H)] \
    + [(img_width, math.floor(y*img_height/H)) for y in range(0, H)]
        
    lines = [(x,y) for x in pins for y in pins if not(x[0] == y[0] and x[0] in(0, img_width)) and not(x[1]==y[1] and x[1] in (0, img_height))]    
    lines_to_draw = get_lines_to_draw(lines, pixels)
    print(len(lines_to_draw))
    result = draw_image(lines_to_draw, img.size, SCALING_FACTOR)
    result.show()
    result.save(image_name[:image_name.rfind('.')] + "(thread art).BMP")
    
    
    
    

if __name__=='__main__':
    main()