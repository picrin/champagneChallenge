from Tkinter import *

import sys

master = Tk()

w = Canvas(master, width=1000, height=1000)
w.pack()

currentX = 0
currentY = 0

def lookupVariable(value, varDict):
    try:
        return int(value)
    except ValueError:
        if value[0] == "-":
            return -1 * int(varDict[value[1:]])
        else:
            return int(varDict[value])

def move(line, variables):
    global currentX
    global currentY
    currentX += lookupVariable(line[1], variables)
    currentY += lookupVariable(line[2], variables)

def line(line, variables):
    moveX = lookupVariable(line[1], variables)
    moveY = lookupVariable(line[2], variables)
    w.create_line(currentX, currentY, currentX + moveX, currentY + moveY)
    move(line, variables)

def position(line, variables):
    global currentX
    global currentY
    currentX = lookupVariable(line[1], variables)
    currentY = lookupVariable(line[2], variables)

def program(lines, variables):
    definitions = {}
    willRecurse = False
    i = 0
    defineCount = None
    while i < len(lines):
        l = lines[i]
        if not willRecurse:
            if l[0] == "position":
                position(l, variables)
            elif l[0] == "line":
                line(l, variables)
            elif l[0] == "move":
                move(l, variables)
            elif l[0] == "define":
                willRecurse = True
                defineCount = 1
            elif l[0] in definitions:
                defName, defVars = definitions[l[0]]
                nextVariables = {key : value for key, value in zip(defVars, l[1:])}
                program(defName, nextVariables)
            i += 1
        else:
            j = 0
            while j < len(lines) - i:
                l = lines[i + j]
                if l[0] == "define":
                    defineCount += 1
                if l[0] == "end":
                    defineCount -= 1
                if defineCount == 0:
                    willRecurse = False
                    recursiveProgram = lines[i:i + j]
                    variables = lines[i - 1][2:]
                    definitions[lines[i - 1][1]] = (recursiveProgram, variables)
                    break
                j += 1
            i += j

with open(sys.argv[1], "r") as f:
    lines = [l.strip().split() for l in f.readlines()]
    program(lines, {}) 

mainloop()
