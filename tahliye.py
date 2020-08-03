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
    kalem = turtle.Turtle()
    kalem.speed(0)
    kalem.color("Black")
    kalem.penup()
    kalem.setposition(-465,-360)

    kalem.pendown()
    kalem.pensize(3)

    kalem.fd(935)
    kalem.lt(90)
    kalem.fd(720)
    kalem.lt(90)
    kalem.fd(935)
    kalem.lt(90)
    kalem.fd(720)
    kalem.hideturtle()

    #grid
    kalem.penup()
    grid_x = -463
    grid_y = 359
    kalem.setpos(grid_x,grid_y)
    kalem.speed(0)
    kalem.pensize(1)
    kalem.pendown()

    while grid_x <= 469:
        kalem.goto(grid_x, -360)
        kalem.penup()
        grid_x += 15
        kalem.goto(grid_x, grid_y)
        kalem.pendown()
    
    grid_x = -464
    grid_y = 359
    kalem.penup()
    kalem.setpos(grid_x,grid_y)

    while grid_y >= -361:
        kalem.goto(466, grid_y)
        kalem.penup()
        grid_y -= 15
        kalem.goto(grid_x, grid_y)
        kalem.pendown()

    #Algoritma Kısmı
    maze = np.full((48,62),0)

    #Duvar işaretleme
    
    def grid_click(x,y):

        kalem.pen(pencolor="black", fillcolor="grey", pensize=1, speed=0)
        x1 = x - x%15 + 2           #en yakın karenin x koordinatı
        y1 = y - y%15 - 1           #en yakın karenin y koordinatı
        matris_x = int((359-y1-15)/15)   #matriste x karşılığı
        matris_y = int((x1+463)/15)      #matriste y karşılığı

        if matris_x == 19 and matris_y == 21:
            messagebox.showerror("Hata!", "Çıkışı Duvar Olarak Seçemezsiniz!")
        elif matris_x == 26 and matris_y == 61:
            messagebox.showerror("Hata!", "Çıkışı Duvar Olarak Seçemezsiniz!")
        else:
            kalem.penup()
            kalem.goto(x1, y1)
            kalem.pendown()
            maze[matris_x][matris_y] = 1
            kalem.begin_fill()
            kalem.goto(x1+15, y1)
            kalem.goto(x1+15, y1+15)
            kalem.goto(x1, y1+15)
            kalem.goto(x1, y1)
            kalem.end_fill()

    turtle.onscreenclick(grid_click, 1)

    #Koridor işaretleme
    
    def grid_click2(x,y):

        kalem.pen(pencolor="black", fillcolor="greenyellow", pensize=1, speed=0)
        x1 = x - x%15 + 2           #en yakın karenin x koordinatı
        y1 = y - y%15 - 1           #en yakın karenin y koordinatı
        matris_x = int((359-y1-15)/15)   #matriste x karşılığı
        matris_y = int((x1+463)/15)      #matriste y karşılığı

        if matris_x == 19 and matris_y == 21:
            messagebox.showerror("Hata!", "Çıkışı Duvar Olarak Seçemezsiniz!")
        elif matris_x == 26 and matris_y == 61:
            messagebox.showerror("Hata!", "Çıkışı Duvar Olarak Seçemezsiniz!")
        else:
            kalem.penup()
            kalem.goto(x1, y1)
            kalem.pendown()
            maze[matris_x][matris_y] = 2
            kalem.begin_fill()
            kalem.goto(x1+15, y1)
            kalem.goto(x1+15, y1+15)
            kalem.goto(x1, y1+15)
            kalem.goto(x1, y1)
            kalem.end_fill()

    turtle.onscreenclick(grid_click2, 3)

    start = input("Başlangıç noktasını giriniz: ")
    start = tuple(int(x) for x in start.split(","))

    checkpoint = [(12,2), (12, 4), (12, 10), (12, 13), (12, 18), (12, 21), (13, 25), (12, 28), (12, 32), (12, 35), (12, 40), (12, 44), (12, 49), (14, 51), (15, 51), 
                (20, 57), (21, 48), (21, 38), (21, 33), (23, 48), (28, 48), (31, 48), (36, 48), (39, 48), (44, 48), (13, 16)]

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
    personel.turtlesize(0.5)
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