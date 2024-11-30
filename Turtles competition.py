import turtle as t
import random as r

def register_player(color,sethead,startx,starty):
    player = t.Turtle()
    player.shape("turtle")
    player.setheading(sethead)
    player.color(color)
    player.up()
    player.goto(startx,starty)
    player.down()
    
    return player
    

mys = t.Screen()
mys.setup(1.0,1.0)
mys.bgcolor("Green")
mys.title("Turtle competition")

pen = t.Turtle()
pen.pensize(100)
pen.color("Brown")
pen.speed(0)
pen.up()
pen.goto(350,350)
pen.setheading(-90)
pen.down()

road_lenth = 700

each_roads = []

for i in range(4):
    for j in range(2):
        pen.forward(road_lenth)
        pen.right(90)
        each_roads.append(road_lenth)
    road_lenth -= 150

players = []

players.append(register_player("Red", -90, 335, 325))
players.append(register_player('Blue', -90, 345, 325))
players.append(register_player('yellow', -90, 355, 325))
players.append(register_player('purple', -90, 365, 325))

state = True

finally_lenth = 0
for i in each_roads:
    finally_lenth += i

each_lenths = [0,0,0,0]
counter = 0
c2 = 0

while state:
    
    
    for i in range(len(players)):
        p = players[i]
        lenth = r.randint(5, 20)
        
        p.forward(lenth)
        each_lenths[i] += lenth
        
        if each_lenths[i] >= each_roads[counter] and counter < len(each_roads) - 1:
            p.right(90)
            each_lenths[i] = 0
            c2 += 1
            
        elif p.pos()[0] >= pen.pos()[0] and counter == len(each_roads) - 1:
            p.write('I won', font=("tahoma",30))
            state = False
            break
        
    
    if c2 == len(players):
        counter += 1
        c2 = 0

