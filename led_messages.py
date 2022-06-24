import threading
import random
import time
import math
from time import sleep

def team_name():
    sense.show_message(" Hello from team DELTA-T !",text_colour=(156,19,0))

def mask():
    sense.show_message("Do you guys wear masks ?",text_colour=(0,0,46))
    
def feelings():
    sense.show_message("How are you feeling ?",text_colour=(240,246,31))
    
def homesick():
    sense.show_message("Do you sometimes feel homesick ?",text_colour=(0,12,143))
    
def movie():
    sense.show_message("What is your favourite movie ?",text_colour=(246,31,209))
    
def icecream():
    sense.show_message("What is your favourite ice cream flavour ?",text_colour=(224,173,66))
    
def animals():
    sense.show_message("What is your favourite animal ?",text_colour=(66,202,224))
    
def career():
    sense.show_message("What made you want to be an astronaut ?",text_colour=(57,37,128))
    
def wish():
    sense.show_message("Hope you are feeling well !",text_colour=(26,130,208))
    
def random_colour():
    r=0
    g=0
    b=0
    while (r+g+b)<100:   
        r=random.randint(0,255)
        g=random.randint(0,255)
        b=random.randint(0,255)
    return (r,g,b)

def sgn(x):
    if x<0:
        return -1
    else:
        return 1
    
def spiral_arm(start,length,direction):
    for i in range(length):
        x=start[0] + i * direction[0]
        y=start[1] + i * direction[1]
        sense.set_pixel(x,y,random_colour())
        sleep(0.1)
        
def spiral():
    sense.clear()
    directions=[(1,0),(0,1),(-1,0),(0,-1)]
    start=[0,0]
    length=8
    direction=[1,0]
    i=0
    while length>=0:
        spiral_arm(start,length,direction)
        delta = [direction[0] * length , direction[1] * length]
        delta[0] += abs(direction[0]) * -sgn(direction[0])
        delta[1] += abs(direction[1]) * -sgn(direction[1])
        start[0] += delta[0]
        start[1] += delta[1]
        i+=1
        if i%2 == 1:
            length-=1
        direction=directions[i%4]
        start[0] += direction[0]
        start[1] += direction[1]
    
def girofar():
    red = (255, 0, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    dark = (0, 0, 0)
    lines = 3
    
        
    for i in range(100):
        list_ = []
        for i in range(lines):
            list_ += [blue, blue, blue, yellow, yellow, red, red, red]
        for i in range(int(len(list_)/3)):
            index = random.randint(0, len(list_)-1)
            list_.insert(index, dark)
            list_.pop(index + 1)
        for i in range(64 - len(list_)):
            list_.append(dark)
        sense.set_pixels(list_)
        time.sleep(0.1)

def color_shape():
    rc = -1
    b = (0,0,0)

    pixels = [b,b,b,b,b,b,b,b,
          b,rc,b,rc,b,rc,b,b,
          b,b,rc,b,rc,b,b,b,
          b,rc,b,rc,b,rc,b,b,
          b,rc,b,rc,b,rc,b,b,
          b,b,rc,b,rc,b,b,b,
          b,rc,b,rc,b,rc,b,b,
          b,b,b,b,b,b,b,b,
              ]
    

    for i in range(15):
        for i in range(len(pixels)):
                if pixels[i] == rc:
                    pixels[i] = random_colour()
        sense.set_pixels(pixels)
        sense.set_rotation(random.randint(0, 3) * 90)
        sleep(0.39)
        
def color_from_angle(angle):
    sin_r = (math.sin(angle) + 1)/2
    sin_g = (math.sin(angle + 2*math.pi/3) + 1)/2
    sin_b = (math.sin(angle + 4*math.pi/3) + 1)/2
    r = int (sin_r * 255)
    g = int (sin_g * 255)
    b = int (sin_b * 255)
    return (r,g,b)

def wave_rainbow():

    angle = 0

    for _ in range(1500):
        pixels = []
        for i  in range(64):
            pixel_angle = math.cos(angle + i) * 10
            pixels += [color_from_angle(pixel_angle)]
        angle += 0.02
        sense.set_pixels(pixels)
        sleep(0.01)

def arrow():
    dark = (0, 0, 0)
    w = (255, 255, 255)

    arrows = []

    for i in range(4):
        line = (i + 1) * 2
        arrow = []
        for y in range(8):
            arrow.append(w)
        for x in range(line):
            arrow[int((8-line)/2)+x] = dark
        for v in range(len(arrow)):
            arrows.append(arrow[v])

    for i in range(int((64-len(arrows))/8)):
        arrows += [w, w, w, dark, dark, w, w, w]
        
    sense.set_pixels(arrows)
    for i in range(30):
        sense.set_rotation(abs(random.randint(0, 3) * 90 - sense.rotation))
        time.sleep(1)

def symbol():
    yellow = (255,255,0)
    white = (255, 255, 255)
    b = (0,0,0)


    nuke = [
            white,white,white,white,white,white,white,white,
            white,white,white,b,b,white,white,white,
            white,white,b,yellow,yellow,b,white,white,
            white,b,yellow,b,b,yellow,b,white,
            white,b,yellow,b,b,yellow,b,white,
            white,white,b,yellow,yellow,b,white,white,
            white,white,white,b,b,white,white,white,
            white,white,white,white,white,white,white,white]

    sense.set_pixels(nuke)
    time.sleep(5)

messages = [wave_rainbow, color_shape, girofar, spiral, wish, career, animals, icecream, movie, homesick, feelings, mask, team_name, arrow, symbol]

show_messages = True

def message_loop():
    while show_messages:
        sense.clear()
        sense.rotation = 270
        message = random.choice(messages)
        message()
    

#displaying messages on the LED matrix from a different thread
#this allows the main thread to perform measurements without interruptions
thread = threading.Thread(target=message_loop)

def start_loop():
    thread.start()

def stop_loop():
    global show_messages
    show_messages = False
    thread.join()
