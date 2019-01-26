from tkinter import *
import time
import numpy as np
import math
import random
import pandas as pd
from math import hypot
from pynput.keyboard import Key, Controller, Listener
import copy

root = Tk()
canv = Canvas(root, highlightthickness=5)

root.geometry('%sx%s+%s+%s' %(900, 1000, 100, 100))

draw = True

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
    copy_t = copy.copy(t)
    l = len(t)
    for i in range(0, l // 2):
        for j in range(i, l - i -1):
            temp = t[i][j]
            t[i][j] = t[l - 1 - j][i];
            t[l - 1 - j][i] = t[l - 1 - i][l - 1 - j];
            t[l - 1 - i][l - 1 - j] = t[j][l - 1 - i];
            t[j][l - 1 - i] = temp;

    if overlap(piece, board) or outside(piece, [0, 0]):
       piece.tetro = copy_t
       return piece

    if n > 1:
        return rotate(piece, n-1)

    return piece

def get_value(piece, x, y):
    p = piece
    t = p.tetro
    l = len(t)
    px = p.pos[0]
    py = p.pos[1]

    #print("     px: %s | py: %s | x: %s | y:%s | l:%s" % (px, py, x, y, l))

    if px <= x <= px + l -1 and py <= y <= py + l -1:
#        print(t[x-px][y-py])
        return t[x-px][y-py]
    else:
        return 0

def draw(board, piece):
    for i in range(0, 10):
        for j in range(0, 20):
            if board[i, j] == 1 or get_value(piece, i, j) == 1:
                frame = Frame(root, width=40, height=40, background="black")
            else:
                frame = Frame(root, width=40, height=40, background="white")
            frame.grid(row=j, column=i)

def outside(piece, dirvec):
    p = piece
    t = p.tetro
    l = len(t)
    px = p.pos[0] + dirvec[0]
    py = p.pos[1] + dirvec[1]

    for i in range(0, l):
        for j in range(0, l):
            if t[i][j] == 1 and (px+i > 10 or px+i < 0 or py+j >=  20 or py+j < 0):
                print("outside")
                return True
    return False

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
    global board
    if dir == "down":
        if outside(copy.copy(piece), [0, 1]) or overlap(piece, board, "down"):
            piece, board = push_on(piece, board)
        else:
            piece.pos += np.array([0, 1])
#            print("pos0 ", piece.pos[0], "pos1 ", piece.pos[1])
    elif dir == "right":
        if overlap(piece, board, "right"):
            piece, board = push_on(piece, board)
        elif not outside(copy.copy(piece), [1, 0]):
            piece.pos += np.array([1,0])
    elif dir == "left":
        if overlap(piece, board, "left"):
            piece, board = push_on(piece, board)
        elif not outside(copy.copy(piece), [-1, 0]):
            piece.pos += np.array([-1,0])

    return piece

def overlap(piece, board, action=None):
    p = piece
    t = p.tetro
    l = len(t)
    dirvec = [0, 0]
    px = p.pos[0]
    py = p.pos[1] + 1

    if action == "down":
        py == 1
        dirvec = [0, 1]

    if action == "right":
        px += 1
        dirvec = [1, 0]

    if action == "left":
        px -= 1
        dirvec = [-1, 0]

    if not outside(piece, dirvec):
        for i in range(0, l-1):
            for j in range(0, l-1):
                if t[i][j] == 1 and board[px+i][py+j] == 1:
                    print("overlap")
                    return True
    return False

def push_on(piece, board):
    p = piece
    t = p.tetro
    l = len(t)
    px = p.pos[0]
    py = p.pos[1]

    for i in range(0, l):
        for j in range(0, l):
            if t[i][j] == 1:
                board[px+i][py+j] = 1
    print("fin push on")
    return rand_piece(), board

def on_press(key):
    pass

def on_release(key):
    global piece
    global board
    # print('{0}'.format(key))
    # print(key)
    # print(piece)
    if key == Key.down:
        piece = move("down", piece)
        return False
    elif key == Key.right:
        piece = move("right", piece)
        return False
    elif key == Key.left:
        piece = move("left", piece)
        return False
    elif key == Key.up:
        piece = rotate(piece, 1)
        return False
    elif key == Key.space:
        piece, board = push_on(piece, board)
        print(board)
        return False

    if key == Key.esc:
        finish = True
        print("exit")
        return False

# board = np.random.randint(0, 2, size=(20, 10))
board = np.zeros((10, 20))
keyboard = Controller()
finish = False
#df = pd.DataFrame(columns=['Names', 'Births'])

piece = rand_piece()

while not finish:
    with Listener(
        on_press=on_press,
        on_release=on_release) as listener: listener.join()
    print(board)
    if draw:
        draw(board, piece)
    canv.update()

root.mainloop()
