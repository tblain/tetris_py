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
from operator import itemgetter, attrgetter, methodcaller
import matplotlib.pyplot as plt

from piece import *
from bot import *
from utils import *
from genetic import *

import os

# desactivate un message dans le cli
"""
board 10:20
"""


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


def game_run(bot, model, draw_enable=False, human=False, nb_move=100, piece_set=[]):
    """
    bot: le bot a faire jouer
    model: le model que le bot va utiliser, le model est fait a partir des genes du bot
           / obliger de fonctionner de cette maniere a cause de keras
    draw_enable: affichage graphique de la partie joue
    human: est ce un humain qui joue / ne fonctionne a priori
    nb_moves: nombre de coup autorise dans la partie
    piece_set: suite de pieces avec lequel jouer
    """
    global board_draw
    global canv
    global root

    if len(piece_set) == 0:
        for i in range(0, nb_move + 10):
            piece_set.append(rand_piece())

    score = 0
    move_played = 0
    finish = False
    board = np.zeros((10, 20), dtype=int)
    piece = piece_set[0]

    bot.board = board
    bot.piece = piece
    bot.nb_run += 1
    piece_number = 1

    while not finish:
        if human:
            with Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()
        else:
            need_piece = bot.play(model, piece_set[piece_number : piece_number + 2])
            move_played += 1
            if need_piece:
                bot.piece = piece_set[piece_number]
                piece_number += 1

        if game_over(board) or move_played >= nb_move:
            finish = True
            bot.score += bot.calculate_board_score()

        if draw_enable:
            board_plus_piece = get_board_plus_piece(board, piece)
            draw(board_plus_piece, clean_board_draw(root))
            canv.update()
            time.sleep(0.005)


def gen_algo():
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
    draw_enable = False
    if draw_enable:
        root = Tk()
        canv = Canvas(root, highlightthickness=5)
        root.geometry("%sx%s+%s+%s" % (900, 1000, 100, 100))
        board_draw = clean_board_draw(root)

    list_bot = []

    nb_run = 1  # nb de run par bot
    nb_move = 50  # nb de move par run
    nb_start_pop = 100  # nb de bot dans la pop de depart
    pieces_set = np.empty([nb_run, nb_move + 10], dtype=Piece)

    # generation de la pop de depart
    for i in range(0, nb_start_pop):
        list_bot.append(Bot())

    # generation des set de pieces avec lequels les bot vont jouer
    # chaque bot joue avec set a chaque generation
    for i in range(0, nb_run):
        for j in range(0, nb_move + 10):
            pieces_set[i][j] = rand_piece()

    # boucle de generation
    for i in range(1, 4000000):
        print(" ")
        print("======================================================")
        print("Generation: ", i)
        print("game run, nb bots:", len(list_bot))

        list_fitness_overall = []
        list_lignes_overall = []

        # on fait jouer chaque bot
        for bot in tqdm(list_bot):
            # creation
            model = gen_NN(bot.genes)
            bot.genes = model.get_weights()
            for piece_set in pieces_set:
                game_run(
                    bot, model, nb_move=nb_move, piece_set=copy.deepcopy(piece_set)
                )
            list_fitness_overall.append(bot.get_fitness())
            list_lignes_overall.append(bot.get_lines_cleared())
            keras.backend.clear_session()

        # trie des bots par ordre de fitness
        list_bot.sort(
            key=lambda x: (x.get_lines_cleared(), x.get_fitness()), reverse=True
        )
        new_list_bot = []

        list_fitness = []
        print("moyenne des fitness: ", np.mean(list_fitness_overall))
        print("moyenne des lignes: ", np.mean(list_lignes_overall))
        # selection des x meilleurs bots
        for j in range(0, 10):
            new_list_bot.append(list_bot[j])
            list_fitness.append(
                (list_bot[j].get_lines_cleared(), list_bot[j].get_fitness())
            )

        print("resultat des boss: ", list_fitness)
        # plt.plot([ [bot.get_lines_cleared(), bot.get_fitness() ] for bot in list_bot])
        # plt.show()
        if i > 1:
            model = gen_NN(new_list_bot[0].genes)
            game_run(
                new_list_bot[0],
                model,
                draw_enable=draw_enable,
                nb_move=100,
                piece_set=copy.copy(pieces_set[0]),
            )
            print(
                "resultat du meilleur: ",
                new_list_bot[0].get_lines_cleared(),
                " lignes cleared",
            )
            print(new_list_bot[0].genes[0][0])

        list_bot = []

        l = len(new_list_bot)

        list_enfants = []

        # croisement
        for k in range(1, l):

            b1 = new_list_bot[l - k]
            b2 = new_list_bot[l - k - 1]

            list_bot.append(b1)
            # list_bot.append(b2)

            list_croisement = croisement(b1.genes, b2.genes, 10)

            for enfant in mutate_list(list_croisement, 6, 2):
                list_bot.append(Bot(enfant))

        gc.collect()

    if draw_enable and False:
        root.mainloop()
