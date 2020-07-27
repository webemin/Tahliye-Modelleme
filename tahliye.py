import turtle
import os
from tkinter import messagebox
import numpy as np
import pygame as pg

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.k = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.k = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.k = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] == 1:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            check = False
            for closed_child in closed_list:
                if child == closed_child:
                    check = True
                    continue
            if check:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            if maze[child.position[0]][child.position[1]] == 0:
                child.k = 10*((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)

            child.f = child.g + child.h + child.k

            # Child is already in the open list
            check = False
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    check = True
                    continue
            if check:
                continue

            # Add the child to the open list
            open_list.append(child)

def main():
    #Pencere
    wn = turtle.Screen()
    wn.bgpic("tahliye_kroki1.png")
    wn.setup(width=1.0, height=1.0)
    wn.title("Tahliye")

    #Kenarlık
    kenarlik_ciz = turtle.Turtle()
    kenarlik_ciz.speed(0)
    kenarlik_ciz.color("Black")
    kenarlik_ciz.penup()
    kenarlik_ciz.setposition(-465,-360)

    kenarlik_ciz.pendown()
    kenarlik_ciz.pensize(3)

    kenarlik_ciz.fd(935)
    kenarlik_ciz.lt(90)
    kenarlik_ciz.fd(720)
    kenarlik_ciz.lt(90)
    kenarlik_ciz.fd(935)
    kenarlik_ciz.lt(90)
    kenarlik_ciz.fd(720)
    kenarlik_ciz.hideturtle()

    #grid
    grid_ciz = turtle.Turtle()
    grid_ciz.penup()
    grid_x = -463
    grid_y = 359
    grid_ciz.setpos(grid_x,grid_y)
    grid_ciz.speed(0)
    grid_ciz.pendown()

    while grid_x <= 469:
        grid_ciz.goto(grid_x, -360)
        grid_ciz.penup()
        grid_x += 15
        grid_ciz.goto(grid_x, grid_y)
        grid_ciz.pendown()
    
    grid_x = -464
    grid_y = 359
    grid_ciz.penup()
    grid_ciz.setpos(grid_x,grid_y)

    while grid_y >= -361:
        grid_ciz.goto(466, grid_y)
        grid_ciz.penup()
        grid_y -= 15
        grid_ciz.goto(grid_x, grid_y)
        grid_ciz.pendown()

    #Koordinat bulma için hareket
    """
    hiz = 15
    def sag():
        x = personel.xcor()
        x += hiz
        personel.setx(x)

    def sol():
        x = personel.xcor()
        x -= hiz
        personel.setx(x)

    def yukari():
        y = personel.ycor()
        y += hiz
        personel.sety(y)

    def asagi():
        y = personel.ycor()
        y -= hiz
        personel.sety(y)

    def bilgi():
        messagebox.showinfo("koordinat", personel.pos())

    #tus atamaları
    
    turtle.listen()
    turtle.onkey(sol, "Left")
    turtle.onkey(sag, "Right")

    turtle.listen()
    turtle.onkey(yukari, "Up")
    turtle.onkey(asagi, "Down")

    turtle.listen()
    turtle.onkeypress(bilgi,"a")
    """
    #Algoritma Kısmı
    maze = np.full((48,62),2)

    #Yol işaretleme
    yol_isaret = turtle.Turtle()
    yol_isaret.color("red")
    yol_isaret.hideturtle()
    
    def grid_click(x,y):
        x1 = x - x%15 + 2           #en yakın karenin x koordinatı
        y1 = y - y%15 - 1           #en yakın karenin y koordinatı
        yol_isaret.penup()
        yol_isaret.goto(x1, y1)
        yol_isaret.pendown()
        yol_isaret.goto(x1+15, y1)
        yol_isaret.goto(x1+15, y1+15)
        yol_isaret.goto(x1, y1+15)
        yol_isaret.goto(x1, y1)
        matris_x = int((359-y1-15)/15)   #matriste x karşılığı
        matris_y = int((x1+463)/15)      #matriste y karşılığı
        maze[matris_x][matris_y] = 1

    turtle.onscreenclick(grid_click, 1)

    start = input("Başlangıç noktasını giriniz: ")
    start = tuple(int(x) for x in start.split(","))

    checkpoint = [(11,2), (11, 4), (11, 10), (11, 13), (11, 18), (11, 21), (12, 25), (11, 28), (11, 32), (11, 35), (11, 40), (11, 44), (11, 49), (13, 51), (14, 51), 
                (19, 57), (20, 48), (20, 38), (20, 33), (22, 48), (27, 48), (30, 48), (35, 48), (38, 48), (43, 48), (12, 16)]

    end1 = (19, 21)
    end2 = (26, 61)

    dummy = [(11,2), (11, 4), (11, 10), (11, 13), (11, 18), (11, 21), (11, 25), (11, 28), (11, 32), (11, 35), (11, 40), (11, 44), (11, 49), (13, 51), (14, 51), 
                (19, 57), (20, 48), (20, 38), (20, 33), (22, 48), (27, 48), (30, 48), (35, 48), (38, 48), (43, 48)]

    for i in checkpoint:
        check = astar(maze, start, i)
        if len(check) < len(dummy):
            dummy = check
        
    print(dummy)
    print(dummy[-1])

    path1 = astar(maze, dummy[-1], end1)
    path2 = astar(maze, dummy[-1], end2)

    if len(path1) < len(path2):
        path = dummy + path1
    else:
        path = dummy + path2

    print(path)

    dots = []
    for item in path:
        item = list(item)
        item[0], item[1] = item[1], item[0]
        item[0] = item[0]*15 - 463
        item[1] = -(item[1]*15) + 359
        dots.append(item)
    
    print(dots)
    #-463, 359
    #Personel Yerlestirme
    personel = turtle.Turtle()
    personel.color("Blue")
    personel.shape("circle")
    personel.turtlesize(0.25)
    personel.penup()
    personel.setposition(dots[0])

    personel.pendown()
    personel.pensize(2)

    ###Nokltarı Yerleştirme

    for dot in dots:
        personel.setposition(dot[0],dot[1])
        personel.pendown()

    input("Tusa Basiniz")

if __name__ == '__main__':
    main()