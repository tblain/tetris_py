from tkinter import *
import numpy as np
import random
import copy

from piece import *


def get_value(piece, x, y):
    p = piece
    t = p.tetro
    l = len(t)
    px = p.pos[0]
    py = p.pos[1]

    # print("     px: %s | py: %s | x: %s | y:%s | l:%s" % (px, py, x, y, l))

    if px <= x <= px + l - 1 and py <= y <= py + l - 1:
        #        print(t[x-px][y-py])
        return t[x - px, y - py]
    else:
        return 0


def get_board_plus_piece(board, piece):
    board_plus_piece = np.zeros([10, 20])

    for i in range(0, 10):
        for j in range(0, 20):
            if board[i, j] == 1:
                board_plus_piece[i, j] = 1
            elif get_value(piece, i, j) == 1:
                board_plus_piece[i, j] = 2

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
            board_draw[i, j] = frame

    return board_draw


def rand_piece():
    n = random.randint(0, 6)
    # print("rand n: ", n)
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
        for j in range(0, 4):
            if board[i, j]:
                return True

    return False


def rotate(piece, n=1):
    # rotate the tetro matrice
    t = copy.copy(piece.tetro)
    l = len(t)
    for i in range(0, l // 2):
        for j in range(i, l - i - 1):
            temp = t[i][j]
            t[i, j] = t[l - 1 - j, i]
            t[l - 1 - j, i] = t[l - 1 - i, l - 1 - j]
            t[l - 1 - i, l - 1 - j] = t[j, l - 1 - i]
            t[j, l - 1 - i] = temp

    piece.rot_num += 1
    if piece.rot_num == 3:
        piece.rot_num = 0

    piece.tetro = t

    if n > 1:
        rotate(n - 1)
