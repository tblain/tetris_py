from tkinter import *
import time
import numpy as np
import math
import random
import pandas as pd
import keras
from keras.models import Sequential
from keras.layers import Dense
import tensorflow
from math import hypot
from pynput.keyboard import Key, Controller, Listener
import copy


"""
board 10:20
"""

# Pieces def

class Piece:

    def __init__(self):
        pass

class PieceI(Piece):

    def __init__(self):
        self.id = 0
        self.name = "I"
        self.rot_num = 0
        self.pos = np.array([3, -1])
        self.tetro = np.array([[0, 0, 0, 0, 0],
                               [0, 0, 1, 0, 0],
                               [0, 0, 1, 0, 0],
                               [0, 0, 1, 0, 0],
                               [0, 0, 1, 0, 0]])

class PieceJ(Piece):

    def __init__(self):
        self.id = 1
        self.name = "J"
        self.rot_num = 0
        self.pos = np.array([3, 0])
        self.tetro = np.array([[1, 1, 0],
                               [0, 1, 0],
                               [0, 1, 0]])

class PieceL(Piece):

    def __init__(self):
        self.id = 2
        self.name = "L"
        self.rot_num = 0
        self.pos = np.array([3, 0])
        self.tetro = np.array([[0, 1, 0],
                               [0, 1, 0],
                               [0, 1, 1]])

class PieceO(Piece):

    def __init__(self):
        self.id = 3
        self.name = "O"
        self.rot_num = 0
        self.pos = np.array([3, 0])
        self.tetro = np.array([[1, 1],
                              [1, 1]])

class PieceS(Piece):

    def __init__(self):
        self.id = 4
        self.name = "S"
        self.rot_num = 0
        self.pos = np.array([3, 0])
        self.tetro = np.array([[0, 1, 0],
                               [1, 1, 0],
                               [1, 0, 0]])

class PieceT(Piece):

    def __init__(self):
        self.id = 5
        self.name = "T"
        self.rot_num = 0
        self.pos = np.array([3, 0])
        self.tetro = np.array([[0, 1, 0],
                               [1, 1, 0],
                               [0, 1, 0]])

class PieceZ(Piece):

    def __init__(self):
        self.id = 6
        self.name = "Z"
        self.rot_num = 0
        self.pos = np.array([3, 0])
        self.tetro = np.array([[1, 0, 0],
                               [1, 1, 0],
                               [0, 1, 0]])

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
            t[i,j] = t[l - 1 - j,i]
            t[l - 1 - j,i] = t[l - 1 - i,l - 1 - j]
            t[l - 1 - i,l - 1 - j] = t[j,l - 1 - i]
            t[j,l - 1 - i] = temp

    piece.rot_num += 1
    if piece.rotate == 3:
        piece.rot_num = 0


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
        return t[x-px,y-py]
    else:
        return 0

def get_board_plus_piece(board, piece):
    board_plus_piece = np.zeros([10, 20])

    for i in range(0, 10):
        for j in range(0, 20):
            if board[i, j] == 1 or get_value(piece, i, j) == 1:
                board_plus_piece[i,j] = 1

    return board_plus_piece

def draw(board, board_draw):
    for i in range(0, 10):
        for j in range(0, 20):
            if board[i, j] == 1:
                board_draw[i, j].configure(background="black")
            else:
                board_draw[i, j].configure(background="white")

def clean_board_draw():
    board_draw = np.empty([10, 20], dtype=object)

    for i in range(0, 10):
        for j in range(0, 20):
            frame = Frame(root, width=40, height=40, background="white")
            frame.grid(row=j, column=i)
            board_draw[i,j] = frame

    return board_draw

def outside(piece, dirvec):
    p = piece
    t = p.tetro
    l = len(t)
    px = p.pos[0] + dirvec[0]
    py = p.pos[1] + dirvec[1]

    for i in range(0, l):
        for j in range(0, l):
            if t[i,j] == 1 and (px+i >= 10 or px+i < 0 or py+j >=  20 or py+j < 0):
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
        if not overlap(piece, board, "right") and not outside(copy.copy(piece), [1, 0]):
            piece.pos += np.array([1,0])
    elif dir == "left":
        if not overlap(piece, board, "left") and not outside(copy.copy(piece), [-1, 0]):
            piece.pos += np.array([-1,0])

    return piece

def overlap(piece, board, action=None):
    p = piece
    t = p.tetro
    l = len(t)
    dirvec = [0, 0]
    px = p.pos[0]
    py = p.pos[1]

    if action == "down":
        py += 1
        dirvec = [0, 1]

    if action == "right":
        px += 1
        dirvec = [1, 0]

    if action == "left":
        px -= 1
        dirvec = [-1, 0]

    if not outside(piece, dirvec):
        for i in range(0, l):
            for j in range(0, l):
                if t[i][j] == 1 and board[px+i][py+j] == 1:
                    print("overlap")
                    return True
    return False

def remove_full_lines(board):
    lines_removed = 0

    for j in range(0, 20):
        full = True
        for i in range(0, 10):
            if board[i, j] == 0:
                full = False

        if full:
            print("column ", i, " is full ")
            for y in range(j, 1, -1):
                for x in range(0, 10-1):
                    board[x, y] = board[x, y-1]

    return board

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

    return rand_piece(), remove_full_lines(board)

def direct_pose(piece, board):
    p = piece
    t = p.tetro
    l = len(t)
    px = p.pos[0]
    py = p.pos[1]

    while not overlap(piece, board, "down") and not outside(piece, [0, 1]):
        piece.pos[1] += 1

    return push_on(piece, board)

def game_over(board):
    for i in range(0, 10):
        if board[i, 0]:
            return True

    return False

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
        piece = rotate(piece, 3)
        return False
    elif key == Key.space:
        piece, board = direct_pose(piece, board)
        return False

    if key == Key.esc:
        finish = True
        print("exit")
        return False

# board = np.random.randint(0, 2, size=(20, 10))

draw_enable = True
human = False
finish = False

if draw_enable:
    root = Tk()
    canv = Canvas(root, highlightthickness=5)
    root.geometry('%sx%s+%s+%s' %(900, 1000, 100, 100))
    board_draw = clean_board_draw()

board = np.zeros((10, 20))
keyboard = Controller()

piece = rand_piece()


model = Sequential()

model.add(Dense(units=20, activation='relu', input_dim=1))
model.add(Dense(units=5, activation='softmax'))

def ia_move(piece, board):
    data = board.flatten()
    prediction  = model.predict_classes(data)

    choice = np.argmax(prediction)
    print("prediction", prediction)
    print("choice: ", choice)

    if choice == 0:
        return move("down", piece), board
    elif choice == 1:
        return move("right", piece), board
    elif choice == 2:
        return move("left", piece), board
    elif choice == 3:
        return rotate(piece, 3, board)
    elif choice == 4:
        return direct_pose(piece, board)


while not finish:
    if human:
        with Listener(
            on_press=on_press,
            on_release=on_release) as listener: listener.join()
    else:
        piece, board = ia_move(piece, board)
        #print(model.get_layer(index=0).get_weights())
        weights = model.get_layer(index=0).get_weights()
        #print("weights", weights[0], "\n")
        print("-----------")
        #model.get_layer(index=0).set_weights([weights[0]+np.random.rand(20,1)-0.5, weights[1]])

    if game_over(board):
        finish = True
        print("GAME OVER")
        print("GAME OVER")
        print("GAME OVER")
        print("GAME OVER")
        print("GAME OVER")
        print("GAME OVER")
        print("GAME OVER")
    board_plus_piece = get_board_plus_piece(board, piece)
    # print(board_plus_piece)
    if draw_enable:
        draw(board_plus_piece, board_draw)
        canv.update()
        time.sleep(0.01)

if draw_enable:
    root.mainloop()
