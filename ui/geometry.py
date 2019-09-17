#!/usr/bin/env python

""" IN COLLABORATION WITH AKHIL DATLA """

import arcade as game
import sys
import time
import math
import random

"""AKHIL'S CODE: SHAPE LOGIC"""


# dist returns the distance between two points
def dist(x1, y1, x2, y2):
    d = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return d


# slope returns the slope of the line between two points
def slope(x1, y1, x2, y2):
    if (x2 - x1) == 0:
        return None
    else:
        s = (y2 - y1)/(x2 - x1)
        return s


# isPerpendicular returns true if the lines are perpendicular
def isPerpendicular(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
    s1 = slope(ax1, ay1, ax2, ay2)
    s2 = slope(bx1, by1, bx2, by2)
    if (s1 == None and s2 == 0) or (s1 == 0 and s2 == None):
        return True
    elif (s1 * s2) == -1:
        return True
    else:
        return False


# isParallelogram returns true if the coordinates represent a parallelogram
def isParallelogram(ax1, ay1, bx1, by1, cx1, cy1, dx1, dy1):
    # compute lengths
    length_ab = dist(ax1, ay1, bx1, by1)
    length_bc = dist(bx1, by1, cx1, cy1)
    length_cd = dist(cx1, cy1, dx1, dy1)
    length_da = dist(dx1, dy1, ax1, ay1)
    # compute slopes
    slope_ab = slope(ax1, ay1, bx1, by1)
    slope_bc = slope(bx1, by1, cx1, cy1)
    slope_cd = slope(cx1, cy1, dx1, dy1)
    slope_da = slope(dx1, dy1, ax1, ay1)

    if ((length_ab == length_cd) and (slope_ab == slope_cd)) or \
    ((length_bc == length_da) and (slope_bc == slope_da)):
        return True
    else:
        return False


# Same as code above but takes in tuples
def isParallelogramTuple(coordA, coordB, coordC, coordD):
    # compute lengths
    ax1, ay1 = coordA
    bx1, by1 = coordB
    cx1, cy1 = coordC
    dx1, dy1 = coordD

    length_ab = dist(ax1, ay1, bx1, by1)
    length_bc = dist(bx1, by1, cx1, cy1)
    length_cd = dist(cx1, cy1, dx1, dy1)
    length_da = dist(dx1, dy1, ax1, ay1)
    # compute slopes
    slope_ab = slope(ax1, ay1, bx1, by1)
    slope_bc = slope(bx1, by1, cx1, cy1)
    slope_cd = slope(cx1, cy1, dx1, dy1)
    slope_da = slope(dx1, dy1, ax1, ay1)

    if ((length_ab == length_cd) and (slope_ab == slope_cd)) or \
    ((length_bc == length_da) and (slope_bc == slope_da)):
        return True
    else:
        return False
# print(isParallelogram(2, 4, 8, 4, 6, 0, 0, 0))


"""ADITYA'S CODE: USER INTERFACE"""

# Define Constants
HEIGHT = 750
WIDTH = 750
rows = 20
scale = 30
rowsVal = []
columnVal = []
code = []
lines = []
debug = True
debugExec = False
realindex = 0
undocount = 0


# Colors
class Colors:
    black = (0, 0, 0)
    gray = (130, 130, 130)
    white = (150, 150, 150)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

    colors = [gray, white, red, green, blue]


# Finds Distance Between Two Points
def exactDist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


# Draws Graph
def drawGrid():
    global HEIGHT, WIDTH, rows, scale, size

    for i in range(2):
        game.draw_xywh_rectangle_filled(0, 0, WIDTH, HEIGHT, Colors.black)

    x = 0
    y = 0

    size = WIDTH // rows

    for i in range(rows):
        x += size
        y += size

        rowsVal.append(x)
        columnVal.append(y)

        game.draw_line(x, HEIGHT, x, 0, Colors.gray, 0.3)
        game.draw_line(WIDTH, y, 0, y, Colors.gray, 0.3)

    game.draw_line(WIDTH // 2, 0, WIDTH // 2, HEIGHT, Colors.white, 2)
    game.draw_line(0, HEIGHT // 2, WIDTH, HEIGHT // 2, Colors.white, 2)


# Class holding all points and connections between them
class Point:
    def __init__(self):
        self.points = []
        self.count = 0

    # Add a point
    def append(self, coord):
        self.points.append(tuple(coord))

    # check if points make a parrallelogram using akhil's code
    def check(self):

        if len(self.points) == 4:
            print("Is Parrallelogram: {}".format(isParallelogramTuple(self.points[0], self.points[1], self.points[2], self.points[3])))

    def plot(self):
        values = input("Enter where you want to plot the point in this format: x, y\n")
        x, y = values.split(", ")
        realX = (int(x) + (rows // 2)) * size
        realY = (int(y) + (rows // 2)) * size

        self.points.append((realX, realY))

        if debug:
            print("{}, {}".format(realX, realY))

        code.append("game.draw_circle_filled({}, {}, self.radius, Colors.blue)\n".format(realX, realY))

    # Connect Points
    def connect(self):
        global lines, size, realindex

        record = 420420
        index = 0

        if len(self.points) > 0:

            for c, v in enumerate(self.points):
                if exactDist(v[0], v[1], self.points[-1][0], self.points[-1][1]) < record and self.points[-1] != v:
                    record = exactDist(v[0], v[1], self.points[-1][0], self.points[-1][1])
                    index = c
                    # print("Record: {}".format(record))
            if debug:
                print("Close to ({}, {}) at index {}".format(self.points[index][0] // size - (rows // 2), self.points[index][1] // size - (rows // 2), index))

            if index <= len(self.points) - 2:
                if debug:
                    print("Index - 1: {}, Index + 1: {}".format(exactDist(self.points[index-1][0] , self.points[index-1][1], self.points[-1][0], self.points[-1][1]), exactDist(self.points[index+1][0], self.points[index+1][1], self.points[-1][0], self.points[-1][1])))

            if index <= len(self.points) - 2:
                if exactDist(self.points[index-1][0], self.points[index-1][1], self.points[-1][0], self.points[-1][1]) > exactDist(self.points[index+1][0], self.points[index+1][1], self.points[-1][0], self.points[-1][1]):
                    self.points.insert(index+1, self.points[-1])
                    realindex = index + 1
                    if debug:
                        print("index <; -1 >; insterting at {}".format(index+1))
                else:
                    self.points.insert(index, self.points[-1])
                    realindex = index
                    if debug:
                        print("index <; +1 >; inserting at {}".format(index))
            else:
                print(index)

                if exactDist(self.points[index-1][0], self.points[index-1][1], self.points[-1][0], self.points[-1][1]) > exactDist(self.points[1][0], self.points[1][1], self.points[-1][0], self.points[-1][1]):
                    self.points.insert(1, self.points[-1])
                    realindex = 1
                    if debug:
                        print("index >; -1 >; inserting at {}".format(1))
                else:
                    self.points.insert(-2, self.points[-1])
                    realindex = -2
                    if debug:
                        print("index >; -1 <; inserting at {}".format(-2))

            if debug:
                print("Popped: ({}, {})".format(self.points[-1][0] // size - (rows // 2), self.points.pop()[1] // size - (rows // 2)))
                print()
            else:
                self.points.pop()

            for c, v in enumerate(self.points):
                if debug:
                    print("({}, {})".format(v[0] // size - (rows // 2), v[1] // size - (rows // 2)))
                lines.append("game.draw_line({}, {}, {}, {}, Colors.colors[point.count])\n".format(v[0], v[1],
                                                                                               self.points[c - 1][0],
                                                                                               self.points[c - 1][1]))

    # Clear the Grid and saved values
    def clear(self):
        global lines, code, undocount
        for i in range(3):
            self.points = []
            lines = []
            code = []
            game.start_render()
            for i in range(10):
                game.draw_xywh_rectangle_filled(0, HEIGHT, WIDTH, 0, Colors.black)
            game.finish_render()
        print("Reset")
        undocount = 0


point = Point()


# Make the game window
class Game(game.Window):

    def __init__(self, width, height, title):
        super(Game, self).__init__(width, height, title)
        self.radius = 3

    # Add point where mouse was pressed
    def on_mouse_press(self, x, y, button, modifier):
        global code, lines
        if button == game.MOUSE_BUTTON_LEFT:
            lines = []

            difference = 100
            indexR = 1
            indexC = 1

            # Place point at nearest grid space
            for count, val in enumerate(columnVal):
                if abs(y - val) < difference:
                    indexC = count
                    difference = abs(y - val)

            difference = 100

            for count, val in enumerate(rowsVal):
                if abs(x - val) < difference:
                    indexR = count
                    difference = abs(x - val)

            # print("Placing at ({}, {})".format(rowsVal[indexR], columnVal[indexC]))
            code.append("game.draw_circle_filled({}, {}, self.radius, Colors.blue)\n".format(rowsVal[indexR], columnVal[indexC]))

            point.append((rowsVal[indexR], columnVal[indexC]))
            point.connect()
            point.check()

    def on_key_press(self, key, modifiers):
        global undocount
        """Called whenever a key is pressed. """
        # Reset Screen
        if key == game.key.P:
            point.plot()
            point.connect()
        if key == game.key.R:
            point.clear()
        # Undo last Action
        if key == game.key.U:
            if undocount >= 10:
                point.clear()

            if debugExec:
                print("Before:")
                print(code)
                print(lines)
                print("After:")
            code.pop()
            lines.pop(realindex)
            point.points.pop(realindex)
            if debugExec:
                print(code)
                print(realindex)
                print(lines)
            point.connect()
            for i in range(2):
                game.draw_xywh_rectangle_filled(WIDTH, HEIGHT, 0, 0, Colors.black)
            undocount += 1
            point.check()

    def update(self, delta_time):
        pass

    # Execute all drawing commands
    def on_draw(self):
        drawGrid()
        for c in code:
            exec(c)

        for line in lines:
            exec(line)


# Make screen
screen = Game(HEIGHT, WIDTH, "Make a Shape!")

# Run code
game.run()
