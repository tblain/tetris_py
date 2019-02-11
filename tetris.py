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
from utils import *
from genetic import *

import os
# desactivate un message dans le cli
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

"""
board 10:20
"""

# Pieces def



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

def game_run(bot, draw_enable=False, human=False, nb_move=100):
    score = 0
    move_played = 0
    finish = False
    board = np.zeros((10, 20))
    piece = rand_piece()

    bot.board = board
    bot.piece = piece
    bot.nb_run += 1

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

draw_enable = False

if draw_enable:
    root = Tk()
    canv = Canvas(root, highlightthickness=5)
    root.geometry('%sx%s+%s+%s' %(900, 1000, 100, 100))
    board_draw = clean_board_draw(root)



list_bot = []

#sess = tensorflow.Session()
#sess.run(tensorflow.global_variables_initializer())
#default_graph = tensorflow.get_default_graph()

# generation de la pop de depart
print("gen bots de depart")
for i in tqdm(range(0, 100)):
    list_bot.append(Bot())

print("gen finis")
for i in tqdm(range(1, 100000)):
    print("======================================================")
    print("Generation: ", i)
    print("game run, nb bots:", len(list_bot))
    #pool = ThreadPool(4)
    #resuls = pool.map(game_run, list_bot)
    #with concurrent.futures.ThreadPoolExecutor(2) as executor:
    #    results = [x for x in executor.map(game_run, list_bot)]
    #print("results")
    # calcul des fitness
    for bot in tqdm(list_bot):
        game_run(bot, nb_move=100)
        game_run(bot, nb_move=100)
        #print(i/len(list_bot) * 100, "%")

    # triage des bots par ordre de fintess
    list_bot.sort(key=lambda x: x.get_fitness(), reverse=True)
    new_list_bot = []

    list_fitness = []
    # selection des 10 meilleurs bots
    for j in range(0, 3):
        new_list_bot.append(list_bot[j])
        list_fitness.append(list_bot[j].get_fitness())

    print("weights")
    for layer in new_list_bot[0].model.get_weights():
        print(layer.shape)

    print("resultat des boss: ", list_fitness)
    if i > 1000000:
        print("test avec plus de move")
        root = Tk()
        canv = Canvas(root, highlightthickness=5)
        root.geometry('%sx%s+%s+%s' %(900, 1000, 100, 100))
        board_draw = clean_board_draw(root)
        game_run(new_list_bot[0], draw_enable=True, nb_move=150)

    list_bot = []

    print("croisement")
    l = len(new_list_bot)
    list_croisement = []
    b1 = new_list_bot[l-1]
    list_bot.append(b1)
    for k in tqdm(range(1, l)):
        #print(i/len(list_bot) * 100, "%")

        b2 = new_list_bot[l- k - 1]
        list_bot.append(b2)
        #list_croisement.append((b1, b2,(k+1) * 2))
        list_enfants = croisement(b1, b2, (k+1) * 2)
        for enfant in list_enfants:
            list_bot.append(Bot(enfant))

    #pool = ThreadPool(4)
    #resultats = pool.map(croisement, list_croisement)
    #with ThreadPoolExecutor(max_workers=12) as executor:
    #       resultats = executor.map(croisement, list_croisement)

    #for lists in resultats:
    #    for model in lists:
    #        list_bot.append(Bot(model))
    gc.collect()

if draw_enable:
    root.mainloop()
