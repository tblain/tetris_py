from tkinter import *
import time
import numpy as np
import math
import random
from math import hypot
from pynput.keyboard import Key, Controller, Listener
import copy

root = Tk()
canv = Canvas(root, highlightthickness=5)

root.geometry('%sx%s+%s+%s' %(900, 1000, 100, 100))

"""
board 10:20
"""

# Pieces def

class Piece:
    id = 0
    name = ""
    rot_num = 0
    tetro = []

    def __init__(self):
        pass

class PieceI(Piece):
    id = 0
    name = "I"
    rot_num = 0
    pos = np.array([3, 1])
    tetro = np.array([[0, 0, 0, 0, 0],
                      [0, 0, 1, 0, 0],
                      [0, 0, 1, 0, 0],
                      [0, 0, 1, 0, 0],
                      [0, 0, 1, 0, 0]])

    def __init__(self):
        pass

class PieceJ(Piece):
    id = 1
    name = "J"
    rot_num = 0
    pos = np.array([3, 1])
    tetro = np.array([[1, 1, 0],
                      [0, 1, 0],
                      [0, 1, 0]])

    def __init__(self):
        pass

class PieceL(Piece):
    id = 2
    name = "L"
    rot_num = 0
    pos = np.array([3, 1])
    tetro = np.array([[0, 1, 0],
                      [0, 1, 0],
                      [0, 1, 1]])

    def __init__(self):
        pass

class PieceO(Piece):
    id = 3
    name = "O"
    rot_num = 0
    pos = np.array([3, 1])
    tetro = np.array([[1, 1],
                      [1, 1]])

    def __init__(self):
        pass

class PieceS(Piece):
    id = 4
    name = "S"
    rot_num = 0
    pos = np.array([3, 1])
    tetro = np.array([[0, 1, 0],
                      [1, 1, 0],
                      [1, 0, 0]])

    def __init__(self):
        pass

class PieceT(Piece):
    id = 5
    name = "T"
    rot_num = 0
    pos = np.array([3, 1])
    tetro = np.array([[0, 1, 0],
                      [1, 1, 0],
                      [0, 1, 0]])

    def __init__(self):
        pass

class PieceZ(Piece):
    id = 6
    name = "Z"
    rot_num = 0
    pos = np.array([3, 1])
    tetro = np.array([[1, 0, 0],
                      [1, 1, 0],
                      [0, 1, 0]])

    def __init__(self):
        pass

def rotate(piece, n=1):
    """
    rotate the tetro matrice
    """
    t = piece.tetro
    l = len(t)
    for i in range(0, l // 2):
        for j in range(i, l - i -1):
            temp = t[i][j]
            t[i][j] = t[l - 1 - j][i];
            t[l - 1 - j][i] = t[l - 1 - i][l - 1 - j];
            t[l - 1 - i][l - 1 - j] = t[j][l - 1 - i];
            t[j][l - 1 - i] = temp;

    if n > 1:
        rotate(piece, n-1)

def get_value(piece, x, y):
    p = piece
    t = p.tetro
    l = len(t)
    px = p.pos[0]
    py = p.pos[1]

    #print("     px: %s | py: %s | x: %s | y:%s | l:%s" % (px, py, x, y, l))

    if px <= x < px + l -1 and py <= y < py + l -1:
#        print(t[x-px][y-py])
        return t[x-px][y-py]
    else:
        return 0

def draw(board, piece):
    for i in range(0, 10):
        for j in range(0, 20):
            if board[i, j] == 1 or get_value(piece, i, j) == 1:
                frame = Frame(root, width=45, height=45, background="black")
            else:
                frame = Frame(root, width=45, height=45, background="white")
            frame.grid(row=j, column=i)

def outside(piece, b):
    p = piece
    t = p.tetro
    l = len(t)
    px = p.pos[0]
    py = p.pos[1]

    for i in range(0, l):
        for j in range(0, l):
            if t[i][j] == 1 and (10 < px+i >= 0 or 20 < py+j >= 0):
                return True

def rand_piece():
    n = random.randint(0, 6)
    print("rand n: ", n)

    if n == 0:
        return PieceI()
    elif n == 1:
        return PieceJ()
    elif n == 2:
        return PieceL()
    elif n == 3:
        return PieceO()
    elif n == 4:
        return PieceS()
    elif n == 5:
        return PieceT()
    elif n == 6:
        return PieceZ()

def move(dir, piece):
    if dir == "down":
        if overlap(piece, "down"):
            pass
        else:
#            print("pos0 ", piece.pos[0], "pos1 ", piece.pos[1])
            piece.pos += np.array([0, 1])
#            print("pos0 ", piece.pos[0], "pos1 ", piece.pos[1])
    elif dir == "right":
        if overlap(piece, "right"):
            pass
        else:
            piece.pos += np.array([1,0])
    elif dir == "left":
        print("pos", piece.pos[1])
        if overlap(piece, "left"):
            pass
        elif not outside(piece, board):
            piece.pos += np.array([-1,0])

def overlap(piece, action):
    return False
    if action == "down":
        tp = copy.copy(piece)
        tp.pos

def on_press(key):
    pass 

def on_release(key):
    # print('{0}'.format(key))
    print(key)
    # print(piece)
    if key == Key.down:
        move("down", piece)
        return False
    elif key == Key.right:
        move("right", piece)
        return False
    elif key == Key.left:
        move("left", piece)
        return False
    elif key == Key.up:
        rotate(piece, 1)
        print("test")
        return False

    if key == Key.esc:
        finish = True
        print("exit")
        return False

# board = np.random.randint(0, 2, size=(20, 10))
board = np.zeros((10, 20))
keyboard = Controller()
finish = False

piece = rand_piece()

while not finish:
    with Listener(
        on_press=on_press,
        on_release=on_release) as listener: listener.join()
#    print(board)
    draw(board, piece)
    canv.update()

root.mainloop()
