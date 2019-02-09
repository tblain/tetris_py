from tkinter import *
import time
import numpy as np
import math
import random
import pandas as pd
import keras
from keras.models import Model
from keras.layers import Dense, Input, Flatten
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

def rotate(piece, board, n=1):
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
    if piece.rot_num == 3:
        piece.rot_num = 0


    if overlap(piece, board) or outside(piece, [0, 0]):
       piece.tetro = copy_t
       return piece

    if n > 1:
        return rotate(piece, board, n-1)

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
    #print("rand n: ", n)
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

def move(dir, piece, board):
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
                print
                if t[i][j] == 1 and board[px+i][py+j] == 1:
                    return True
    return False

def remove_full_lines(board):
    global score
    lines_removed = 0

    for j in range(0, 20):
        full = True
        for i in range(0, 10):
            if board[i, j] == 0:
                full = False

        if full:
            print("column ", i, " is full ")
            score += 100
            for y in range(j, 1, -1):
                for x in range(0, 10-1):
                    board[x, y] = board[x, y-1]

    return board

def push_on(piece, board):
    global score
    score += 10
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

def gen_NN(genes=None):
    inputs = Input(shape=(20,10))
    x = Flatten()(inputs)
    x = Dense(10, activation='relu')(x)
    x = Dense(10, activation='relu')(x)
    x = Dense(10, activation='relu')(x)
    predictions = Dense(5, activation='softmax')(x)

    model = Model(inputs=inputs, outputs=predictions)

    return model

class Bot:
    def __init__(self, genes=None):
        self.model = gen_NN(genes)
        self.fitness = 0

def ia_move(model, piece, board):
    data = board
    data = data.reshape((1, 20, 10))
    #df = pd.DataFrame(data)
    #print("dataframe : ", df)
    #print(" rand : ", np.random.rand(200))
    prediction = model.predict(data, batch_size=1)

    choice = np.argmax(prediction)
    #print("prediction", prediction)
    #print("choice: ", choice)

    if choice == 0:
        return move("down", piece, board), board
    elif choice == 1:
        return move("right", piece, board), board
    elif choice == 2:
        return move("left", piece, board), board
    elif choice == 3:
        return rotate(piece, board, 3), board
    elif choice == 4:
        return direct_pose(piece, board)


def game_run(bot, draw_enable=False, human=False):
    global score
    global board_draw
    score = 0
    nb_move = 0
    finish = False
    board = np.zeros((10, 20))
    keyboard = Controller()
    piece = rand_piece()
    model = bot.model

    while not finish:
        if human:
            with Listener(
                on_press=on_press,
                on_release=on_release) as listener: listener.join()
        else:
            piece, board = ia_move(model, piece, board)
            weights = np.array(model.get_weights())
            new_weights = []
            for weight in weights:
                #print("shape : ", weight.shape)
                #print("weight ", weight)
                if len(weight.shape) > 1:
                    new_weights.append(np.array(weight) + np.random.rand(weight.shape[0], weight.shape[1]))
                else:
                    new_weights.append(weight)

            model.set_weights(new_weights)
            nb_move += 1

        if game_over(board) or nb_move > 100:
            finish = True
            #print("GAME OVER")
        board_plus_piece = get_board_plus_piece(board, piece)
        # print(board_plus_piece)
        if draw_enable:
            draw(board_plus_piece, board_draw)
            canv.update()
            time.sleep(0.05)

    #print("score ", score)
    fitness = score
    bot.fitness = fitness


score = 0
draw_enable = False

if draw_enable:
    root = Tk()
    canv = Canvas(root, highlightthickness=5)
    root.geometry('%sx%s+%s+%s' %(900, 1000, 100, 100))
    board_draw = clean_board_draw()


list_bot = []

print("gen bots")
# generation des bots
for i in range(0, 20):
    list_bot.append(Bot())

print("game run")
i = 0
# calcul des fintess
for bot in list_bot:
    game_run(bot)
    i += 1
    print(i/len(list_bot) * 100)

# triage des bots par ordre de fintess
list_bot.sort(key=lambda x: x.fitness, reverse=True)
new_list_bot = []

# selection des 10 meilleurs bots
for i in range(0, 10):
    new_list_bot.append(list_bot[i])

list_bot = new_list_bot
for bot in list_bot:
    print(bot.fitness)
if draw_enable:
    root.mainloop()
