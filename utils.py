from tkinter import *
import gc
import time
import numpy as np
import math
from math import hypot
import random
import pandas as pd
from tqdm import tqdm
import keras
from keras.models import Model
from keras.layers import Dense, Input, Flatten
import keras.backend as K
import tensorflow
from pynput.keyboard import Key, Controller, Listener
import copy
from multiprocessing.dummy import Pool as ThreadPool
from concurrent.futures import ThreadPoolExecutor
from tensorflow.python.client import device_lib

from piece import *
from bot import *
from genetic import *

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
            if board[i, j] == 1:
                board_plus_piece[i,j] = 1
            elif get_value(piece, i, j) == 1:
                board_plus_piece[i,j] = 2

    return board_plus_piece

def draw(board, board_draw):
    for i in range(0, 10):
        for j in range(0, 20):
            if board[i, j] == 1:
                board_draw[i, j].configure(background="black")
            elif board[i, j] == 2:
                board_draw[i, j].configure(background="red")
            else:
                board_draw[i, j].configure(background="white")

def clean_board_draw(root):
    board_draw = np.empty([10, 20], dtype=object)

    for i in range(0, 10):
        for j in range(0, 20):
            frame = Frame(root, width=40, height=40, background="white")
            frame.grid(row=j, column=i)
            board_draw[i,j] = frame

    return board_draw

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

    return piece

def game_over(board):
    for i in range(0, 10):
        if board[i, 0]:
            return True

    return False
