from tkinter import *
import time
import numpy as np

from piece import *
from bot import *
from utils import *


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
        print("exit")
        return False


def game_run(bot, model, draw_enable=False, human=False, nb_move=100, piece_set=[]):
    """
    bot: le bot a faire jouer
    model: le model que le bot va utiliser,
           le model est fait a partir des genes du bot
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
        for i in range(0, nb_move+10):
            piece_set.append(rand_piece())

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
            with Listener(
                on_press=on_press,
                on_release=on_release) as listener: listener.join()
        else:
            need_piece = bot.play(model, piece_set[piece_number:piece_number+2])
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