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

import os
# desactivate un message de le cli
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

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

def gen_NN(genes=[]):
    inputs = Input(shape=(202,))
    #x = Flatten()(inputs)
    x = Dense(10, activation='relu')(inputs)
    x = Dense(60, activation='relu')(x)
    x = Dense(60, activation='relu')(x)
    predictions = Dense(4, activation='softmax')(x)

    model = Model(inputs=inputs, outputs=predictions)

    if len(genes) > 0:
        model.set_weights(genes)
    model._make_predict_function()

    return model

class Bot:
    def __init__(self, genes=[]):
        self.model = gen_NN(genes)
        self.fitness = 0
        self.score = 0
        self.penalite = 0

    def play(self): # joue un coup
        data = self.board.reshape((1, 200))
        piece_input = np.array([self.piece.id, self.piece.rot_num]).reshape((1, 2))
        data = np.hstack((data, piece_input))
        #df = pd.DataFrame(data)
        #print("dataframe : ", df)
        #print(" rand : ", np.random.rand(200))
        #with tensorflow.Session(graph=tensorflow.Graph()) as sess:
        #    K.set_session(sess)
        prediction = self.model.predict_on_batch(data)

        choice = np.argmax(prediction)
        #print("prediction", prediction)
        #print("choice: ", choice)

        if choice == 0:
            self.move("left")
        elif choice == 1:
            self.move("right")
        elif choice == 2:
            self.direct_pose()
        elif choice == 3:
            self.rotate(3)
        elif choice == 4:
            self.move("down")

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

        while not self.overlap("down") and not self.outside([0, 1]):
            self.piece.pos[1] += 1

        self.push_on()

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
        self.score += 10 - self.penalite
        l = len(self.piece.tetro)
        px = self.piece.pos[0]
        py = self.piece.pos[1]

        for i in range(0, l):
            for j in range(0, l):
                if self.piece.tetro[i][j] == 1:
                    self.board[px+i][py+j] = 1
        self.remove_full_lines()
        self.piece = rand_piece()

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
                print("column ", i, " is full ")
                print("column ", i, " is full ")
                print("column ", i, " is full ")
                print("column ", i, " is full ")
                print("column ", i, " is full ")
                print("column ", i, " is full ")
                print("column ", i, " is full ")
                print("column ", i, " is full ")
                print("column ", i, " is full ")
                print("column ", i, " is full ")
                print("column ", i, " is full ")
                print("column ", i, " is full ")
                print("column ", i, " is full ")
                print("column ", i, " is full ")
                print("column ", i, " is full ")
                print("column ", i, " is full ")
                print("column ", i, " is full ")
                print("column ", i, " is full ")
                print("column ", i, " is full ")
                print("column ", i, " is full ")
                self.score += 100
                for y in range(j, 1, -1):
                    for x in range(0, 10-1):
                        self.board[x, y] = self.board[x, y-1]

    def get_fitness(self):
        return self.score

def game_run(bot, draw_enable=False, human=False, nb_move=100):
    score = 0
    move_played = 0
    finish = False
    board = np.zeros((10, 20))
    piece = rand_piece()

    bot.board = board
    bot.piece = piece

    while not finish:
        if human:
            with Listener(
                on_press=on_press,
                on_release=on_release) as listener: listener.join()
        else:
            #piece, board = ia_move(model, piece, board)
            bot.play()
            move_played += 1

        if game_over(board) or move_played > nb_move:
            finish = True
            #print("GAME OVER")
        # print(board_plus_piece)
        if draw_enable:
            board_plus_piece = get_board_plus_piece(board, piece)
            draw(board_plus_piece, board_draw)
            canv.update()
            time.sleep(0.05)

    #print("score ", score)

def croisement(args):
    """
    b1.fitness > b2.fitness
    renvoie le croisement entre les poids des 2 parents
    c'est a dire 2 enfants avec des poids qui seront un mixte des parents
    """
    b1 = args[0]
    b2 = args[1]
    nb_enfants = args[2]
    bw1 = b1.model.get_weights()
    bw2 = b2.model.get_weights()

    list_enfants = []
    list_p = []

    for i in range(0, nb_enfants):
        # poids des deux enfants qu'on initialise avec les poids des parents
        list_enfants.append(b1.model.get_weights())
        # nombre aleatoire compris entre - 0.5 et 1.5 utiliser pour faire le croisement
        list_p.append(random.uniform(-0.5, 1.5))


    # on parcourt les couches des parents en simultanne

    for k in range(0, len(bw1)):
        lbw1 = bw1[k]
        lbw2 = bw2[k]
        if len(lbw1.shape) > 1: # on skip les couches qui qui n'ont pas de poids
            nb_col = lbw1.shape[0]
            nb_row = lbw2.shape[1]

            # on update les poids de la couche
            for i in range(0, nb_col):
                for j in range(0, nb_row):
                    v1 = lbw1[i, j]
                    v2 = lbw2[i, j]
                    for e in range(0, len(list_enfants)):
                        p = list_p[e]
                        list_enfants[e][k][i, j] = p * v1 + (1-p) * v2 + random.uniform(-2, 2)

    print("finis: ", nb_enfants)
    return list_enfants

draw_enable = False

if draw_enable:
    root = Tk()
    canv = Canvas(root, highlightthickness=5)
    root.geometry('%sx%s+%s+%s' %(900, 1000, 100, 100))
    board_draw = clean_board_draw()



list_bot = []

#sess = tensorflow.Session()
#sess.run(tensorflow.global_variables_initializer())
#default_graph = tensorflow.get_default_graph()

# generation de la pop de depart
print("gen bots de depart")
for i in tqdm(range(0, 30)):
    list_bot.append(Bot())

print("gen finis")
for i in range(1, 40):

    print("game run, nb bots:", len(list_bot))
    #pool = ThreadPool(4)
    #resuls = pool.map(game_run, list_bot)
    #with concurrent.futures.ThreadPoolExecutor(2) as executor:
    #    results = [x for x in executor.map(game_run, list_bot)]
    #print("results")
    # calcul des fitness
    for bot in tqdm(list_bot):
        game_run(bot, nb_move=40)
        #print(i/len(list_bot) * 100, "%")

    # triage des bots par ordre de fintess
    list_bot.sort(key=lambda x: x.get_fitness(), reverse=True)
    new_list_bot = []

    list_fitness = []
    # selection des 10 meilleurs bots
    for j in range(0, 5):
        new_list_bot.append(list_bot[j])
        list_fitness.append(list_bot[j].get_fitness())

    print("weights")
    for layer in new_list_bot[0].model.get_weights():
        print(layer.shape)

    print("resultat des boss: ", list_fitness)
    if i > 100:
        print("test avec plus de move")
        root = Tk()
        canv = Canvas(root, highlightthickness=5)
        root.geometry('%sx%s+%s+%s' %(900, 1000, 100, 100))
        board_draw = clean_board_draw()
        game_run(new_list_bot[0], draw_enable=True, nb_move=150)

    list_bot = []

    print("croisement")
    l = len(new_list_bot)
    list_croisement = []
    b1 = new_list_bot[l-1]
    for k in range(1, l):
        #print(i/len(list_bot) * 100, "%")

        b2 = new_list_bot[l- k - 1]
        list_croisement.append((b1, b2,(k+1) * 2))
        #list_enfants = croisement(b1, b2, (k+1) * 2)
        #for enfant in list_enfants:
        #    list_bot.append(Bot(enfant))

    #pool = ThreadPool(4)
    #resultats = pool.map(croisement, list_croisement)
    with ThreadPoolExecutor(max_workers=12) as executor:
        resultats = executor.map(croisement, list_croisement)

    for lists in resultats:
        for model in lists:
            list_bot.append(Bot(model))

if draw_enable:
    root.mainloop()
