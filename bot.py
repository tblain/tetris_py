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
from utils import *
from genetic import *

class Bot:
    def __init__(self, genes=[]):
        self.genes = genes
        self.fitness = 0
        self.score = 0
        self.penalite = 0
        self.nb_run = 0
        self.lines_cleared = 0

    def play(self, model): # joue un coup
        #data = self.board#.reshape((1, 200))
        data = np.zeros(10)
        for i in self.board:
            a = i.dot(2**np.arange(i.size)[::-1])
            data[i] = a
        data = data.reshape(1, 10)
        piece_input = np.array([self.piece.id, self.piece.rot_num]).reshape((1, 2))
        data = np.hstack((data, piece_input))
        #df = pd.DataFrame(data)
        #print("dataframe : ", df)
        #print(" rand : ", np.random.rand(200))
        #with tensorflow.Session(graph=tensorflow.Graph()) as sess:
        #    K.set_session(sess)
        prediction = model.predict_on_batch(data)

        choice = np.argmax(prediction)
        #print("prediction", prediction)
        #print("choice: ", choice)

        if choice == 10:
            self.rotate(3)
        else:
            for i in range(0, choice):
                self.move("right")
            self.direct_pose()

    def move(self, dir): # deplace la piece dans la direction indique
        if dir == "down":
            if self.outside([0, 1]) or self.overlap("down"):
                self.push_on_board()
            else:
                self.piece.pos += np.array([0, 1])
        elif dir == "right":
            self.penalite = 0
            if not self.overlap("right") and not self.outside([1, 0]):
                self.piece.pos += np.array([1,0])
        elif dir == "left":
            self.penalite = 0
            if not self.overlap("left") and not self.outside([-1, 0]):
                self.piece.pos += np.array([-1,0])

    def direct_pose(self):
        self.penalite = 9
        l = len(self.piece.tetro)
        px = self.piece.pos[0]
        py = self.piece.pos[1]

        if not self.overlap() and not self.outside([0, 0]):
            while not self.overlap("down") and not self.outside([0, 1]):
                self.piece.pos[1] += 1
            self.push_on()

    def calculate_board_score(self): # return the score for the current game
        b = self.board
        bs = 0

        for i in range(0, 10):
            full_combo = 20
            empty_combo = 1
            for j in range(0, 20):
                if b[i, j] == 1:
                    bs += full_combo
                    full_combo = max(1, full_combo-1)
                    empty_combo = 1
                else:
                    full_combo = max(1, full_combo-empty_combo)
                    empty_combo +=1

        return bs / 10

    def rotate(self, n=1):
        """
        rotate the tetro matrice
        """
        t = copy.copy(self.piece.tetro)
        l = len(t)
        for i in range(0, l // 2):
            for j in range(i, l - i -1):
                temp = t[i][j]
                t[i,j] = t[l - 1 - j,i]
                t[l - 1 - j,i] = t[l - 1 - i,l - 1 - j]
                t[l - 1 - i,l - 1 - j] = t[j,l - 1 - i]
                t[j,l - 1 - i] = temp

        self.piece.rot_num += 1
        if self.piece.rot_num == 3:
            self.piece.rot_num = 0


        if self.overlap() or self.outside([0, 0]):
           self.piece.tetro = t

        if n > 1:
            self.rotate(n-1)

    def push_on(self): # met la piece definitivement dans le board
        #self.score += 10 - self.penalite
        l = len(self.piece.tetro)
        px = self.piece.pos[0]
        py = self.piece.pos[1]

        for i in range(0, l):
            for j in range(0, l):
                if self.piece.tetro[i][j] == 1:
                    #print("p: ", self.piece.tetro, " | px: ", px+l, "| py ", py+l)
                    #print(self.board)
                    self.board[px+i][py+j] = 1
        self.remove_full_lines()

    def outside(self, dirvec): # renvoie si la piece est en dehors du tableau ou non apres avoir applique la direction en arg
        p = copy.copy(self.piece)
        l = len(p.tetro)
        px = p.pos[0] + dirvec[0]
        py = p.pos[1] + dirvec[1]

        for i in range(0, l):
            for j in range(0, l):
                if p.tetro[i,j] == 1 and (px+i >= 10 or px+i < 0 or py+j >=  20 or py+j < 0):
                    return True
        return False

    def overlap(self, action=None):
        l = len(self.piece.tetro)
        dirvec = [0, 0]
        px = self.piece.pos[0]
        py = self.piece.pos[1]

        if action == "down":
            py += 1
            dirvec = [0, 1]

        if action == "right":
            px += 1
            dirvec = [1, 0]

        if action == "left":
            px -= 1
            dirvec = [-1, 0]

        if not self.outside(dirvec):
            for i in range(0, l):
                for j in range(0, l):
                    if self.piece.tetro[i][j] == 1 and self.board[px+i][py+j] == 1:
                        return True
        return False

    def remove_full_lines(self):
        for j in range(0, 20):
            full = True
            for i in range(0, 10):
                if self.board[i, j] == 0:
                    full = False

            if full:
                #print("ligne cleared")
                self.lines_cleared += 1
                for y in range(j, 1, -1):
                    for x in range(0, 10-1):
                        self.board[x, y] = self.board[x, y-1]
    def get_fitness(self):
        return self.score / self.nb_run

    def get_lines_cleared(self):
        return self.lines_cleared / self.nb_run
