#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      alex
#
# Created:     08/06/2020
# Copyright:   (c) alex 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy
from random import randint
import time
from math import sin, cos, pi
import moviepy.editor as mp

IMG_RATIO = 1.3477218225419665 # ration from width to height
IMG_HEIGHT = 1500 # in pixels, image used to draw
IMG_WIDTH = int (IMG_HEIGHT / IMG_RATIO)
BORDER = 0.05 # black border percentage around the image
ANIMATION_WIDTH = 0.5 # central percentage of IMG_WIDTH
ANIMATION_MAX_AMPLITUDE = 0.10 # proportinal to IMG_HEIGHT
POINTS_PER_LINE = int(IMG_WIDTH / 5) # number of points in the line (connected by lines)
LINES = 90 # number of horiontal lines/rows in the image
FREQUENCIES_PER_LINE = 16 # number of waves per line (May not be achieved, since theres a minimum disntace between waves
GIF_SIZE = 40 # number of frames in the gif file
RESIZE_RATIO = 0.5 #percentage of the GIF based on IMG_WIDTH and IMG_HEIGHT

GIF_SKIP_FRAME = 1 # 1 keeps every frame, 2 keeps 1 for every 2 frames, 3 keeps 1 for every 3 frames, etc

lines = []

images = []

frequencies = []
frequenciesCounter = []

step = 0
gifSkipFrameCounter = GIF_SKIP_FRAME - 1

NORMAL = [0.99, 0.95, 0.9, 0.75, 0.5, 0.25, 0.1, 0.05, 0.01]

def animationStep():
    global step
    step += 1
    for idx, line in enumerate(lines):
        for fidx, p in enumerate(frequencies[idx]):
            xf = p[0]
            yf = p[1]

            #if frequenciesCounter[idx][fidx] > 0:
                #frequenciesCounter[idx][fidx] -= 1

            #Found central x idx for this frequency
            centralX = -1
            for lidx, p in enumerate(line):
                if p[0] > xf:
                    centralX = lidx
                    break
            if centralX < 0:
                print("pau")

            x = line[centralX][0]
            y = line[centralX][1]
            if yf < 0:
                deltaY = -2
            else:
                deltaY = 2 # float(yf - y) / 20.0
            newY = y + deltaY
            #if newY < -50 or newY > 50:
            #    print(1)
            if step > 200:
                if xf == 580:
                    #print(1)
                    #print(deltaY, y, yf)
                    pass
            if yf < 0:
                if y < yf:
                    frequenciesCounter[idx][fidx] = 0
                    continue
            else:
                if y > yf:
                    frequenciesCounter[idx][fidx] = 0
                    continue
            line[centralX] = [x, y + deltaY]
            for deltaX, normalY in enumerate(NORMAL):
                dy = normalY * deltaY
                #deltaY -= 0.1
                try:
                    #if x == 181 and xf != 174:
                    #    print(1)
                    x = line[centralX + deltaX + 1][0]
                    y = line[centralX + deltaX + 1][1]
                    if abs(y + dy) < ANIMATION_MAX_AMPLITUDE * IMG_HEIGHT:
                        line[centralX + deltaX + 1] = [x, y + dy]

                except:
                    pass

                try:
                    #if x == 181 and xf != 174:
                    #    print(2)
                    x = line[centralX - deltaX - 1][0]
                    y = line[centralX - deltaX - 1][1]
                    if abs(y + dy) < ANIMATION_MAX_AMPLITUDE * IMG_HEIGHT:
                        line[centralX - deltaX - 1] = [x, y + dy]
                except:
                    pass

    return None

def randomizeFrequencies():
    #if randint(0,100) < 90:
    #    return

    '''if step < 30:
        limit = 0
    else:
        limit = 100'''

    for i in range(LINES):
        for f in range(len(frequencies[i])):
            if frequenciesCounter[i][f] > 0:
                continue

            if True: #randint(0,100) < 50:
                if step > 200:
                    if f == 2:
                        pass #$ print(1)
                frequenciesCounter[i][f] = randint(20, 50)
                xf,yf = frequencies[i][f]
                xfLimit1 = int(IMG_WIDTH / 2 - (IMG_WIDTH * ANIMATION_WIDTH / 2))
                xfLimit2 = int(IMG_WIDTH / 2 + (IMG_WIDTH * ANIMATION_WIDTH / 2))
                newX = randint(xfLimit1, xfLimit2)

                yfLimit2 = int(IMG_HEIGHT * ANIMATION_MAX_AMPLITUDE / 2)
                newY = randint(0, yfLimit2)
                if yf < 0:
                    newY = 0
                else:
                    newY = newY * - 1
                frequencies[i][f] = [xf, newY]

def calculateNormal():
    global NORMAL
    length = 3

    NORMAL = []
    for i in range(length):
        x = float(i/length) * (pi / 2)
        y = 0.5 + cos(x) / 2
        #print (i,y)
        NORMAL.append(y)
    for i in range(length):
        x = float(i/length) * (pi / 2)
        #y = sin(x) / 2 + 0.5
        y = 0.5-sin(x) / 2
        #print (i + length,y)
        NORMAL.append(y)

def drawImage():
    global cvImg
    global gifSkipFrameCounter

    im = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT))
    draw = ImageDraw.Draw(im)

    if len(lines) == 1:
        deltaY = IMG_HEIGHT / 2
    else:
        deltaY = (IMG_HEIGHT * (1 - 2 * BORDER)) / (len(lines) - 1 )

    for idx, line in enumerate(lines):
        yLine = (idx) * deltaY + (BORDER * IMG_HEIGHT)
        xa = 0
        ya = yLine
        poly = [(-1, IMG_HEIGHT + 1), (-1, yLine)]
        for x, y in line:
            yCalc = y + yLine + (randint(0, 1) - 2)
            poly.append((x, yCalc))
            xa = x
            ya = yCalc
        poly.append((IMG_WIDTH + 1, yLine))
        poly.append((IMG_WIDTH + 1, IMG_HEIGHT + 1))
        draw.line(poly, fill="#ffffff", width=3)
        draw.polygon(poly, fill=0, outline="#ffffff")

    font = ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf', 30)

    print("Frame:", step)
    #draw.text((5, 5), str(step), font = font, align ="left")


    # Clear the side borders with two black rectangles
    borderX1 = int(IMG_WIDTH * BORDER)
    borderX2 = int(IMG_WIDTH - IMG_WIDTH * BORDER)
    poly = [(0,0), (borderX1, 0), (borderX1, IMG_HEIGHT), (0, IMG_HEIGHT)]
    draw.polygon(poly, fill=0, outline=0)
    poly = [(IMG_WIDTH,0), (borderX2, 0), (borderX2, IMG_HEIGHT), (IMG_WIDTH, IMG_HEIGHT)]
    draw.polygon(poly, fill=0, outline=0)

    borderY2 = int(IMG_HEIGHT * (1-BORDER))
    #draw.text((540, 1430), "https://dalpix.com/unknown-pleasures", font = font, align ="right", fill="#909090")
    draw.text((borderX1, borderY2), "https://dalpix.com/unknown-pleasures", font = font, align ="right", fill="#909090")



    im = im.resize((int(IMG_WIDTH * RESIZE_RATIO), int(IMG_HEIGHT * RESIZE_RATIO)), resample=Image.LANCZOS)

    # add images to a list used to generate the GIF
    gifSkipFrameCounter += 1
    if gifSkipFrameCounter >= GIF_SKIP_FRAME:
        gifSkipFrameCounter = 0
        images.append(im.copy())
        if len(images) > int(GIF_SIZE / 2):
            images.pop(0)

    cvImg2 = numpy.array(im)
    cvImg2 = cv2.cvtColor(cvImg2, cv2.COLOR_RGB2BGR)

    return cvImg2


if __name__ == '__main__':

    calculateNormal()

    for i in range(LINES):
        lines.append([])
        for p in range(POINTS_PER_LINE):
            x = int(p * (float(IMG_WIDTH) / float(POINTS_PER_LINE)))
            y = 0
            lines[i].append([x,y])

        frequencies.append([])
        frequenciesCounter.append([])
        xfLimit1 = int(IMG_WIDTH / 2 - (IMG_WIDTH * ANIMATION_WIDTH / 2))
        xfLimit2 = int(IMG_WIDTH / 2 + (IMG_WIDTH * ANIMATION_WIDTH / 2))
        yfLimit1 = int(IMG_HEIGHT * ANIMATION_MAX_AMPLITUDE / 2 * -1)
        yfLimit2 = int(IMG_HEIGHT * ANIMATION_MAX_AMPLITUDE / 2)
        yfLimit2 = 0

        pixelsPerWave = int ((IMG_WIDTH / POINTS_PER_LINE) * len(NORMAL))
        xf = randint(xfLimit1, xfLimit1 + pixelsPerWave * 2)
        yf = randint(yfLimit1, yfLimit2)
        frequencies[i].append((xf, yf))
        frequenciesCounter[i].append(50)
        for f in range(FREQUENCIES_PER_LINE - 1):
            xf = randint(xf + pixelsPerWave, xf + pixelsPerWave * 2)
            yf = randint(yfLimit1, yfLimit2)
            if xf < xfLimit2:
                frequencies[i].append((xf, yf))
                frequenciesCounter[i].append(50)
        '''
        for f in range(FREQUENCIES_PER_LINE):
            xf = randint(xfLimit1, xfLimit2)
            yf = randint(yfLimit1, yfLimit2)
            frequencies[i].append((xf, yf))
            frequenciesCounter[i].append(50)

    frequencies =  [[(585, 17), [690, -29], (580, -28), [720, 7]]]
    frequenciesCounter = [[50, 47, 50, 35]]
    '''

    while(True):
        randomizeFrequencies()
        animationStep()
        cvImg = drawImage()
        cv2.imshow("main", cvImg)

        if cv2.waitKey(2) == 27:
            break

    print ("Saving GIF...")
    gif = []
    for img in images:
        gif.append(img)
    for img in gif[-2::-1][:-1]: # Get the reversed list, but without the first and last elements   #images[::-1]:
        gif.append(img)
    gif[0].save("unknwon_pleasures.gif", save_all=True, append_images=gif[1:], duration=50, loop=0)

    print ("Done. GIF contains %s frames" % (len(gif)))


