import numpy as np
import copy

from utils import rand_piece, rotate, game_over
from state import State


def eval_board(state, depth):
    pass


def compare_board():
    pass


def NN_eval_state(model, board):
    # evalue le score d'un board
    data = board.board.flatten()
    data = np.append(data, board.score)
    return model.predict(data)


def NN_search_eval_state(model, state, pieces, train=False, NN_play=True):
    """
    model: reseau de neurones qui va faire les predictions
    state: etat du jeu a evaluer
    pieces: suites de pieces a utiliser pour evaluer le state de base
    train: est-ce que l'on entraine le model
    NN_play: est-ce que l'on utilise la prediction du NN ou de l'algo
             pour faire l'evaluation
             si non c'est comme si c'etait l'algo qui jouait
             et le model ce fait juste entrainer
    """

    if len(pieces) == 1:
        score_NN = np.zeros(30)
        score_algo = np.zeros(30)
        piece = pieces[0]

        # on parcourt toutes les possibilites de jeux et on les evalue
        for r in range(0, 3):
            if r >= 1:
                rotate(piece)

            for c in range(0, 10):
                e_state = copy.deepcopy(state)
                e_state.pose(c, piece)

                # on stoque les scores
                score_NN[10*r + c] = NN_eval_state(model)
                if train:
                    score_algo[10*r + c] = eval_board(state, 2)
                    # TODO : model.fit + faire un fit stochiastic dans le NN

        # on retourne la valeur max
        if NN_play:
            return np.argmax(score_NN)
        else:
            return np.argmax(score_algo)
    else:
        score_NN = np.zeros(30)
        piece = pieces[0]
        pieces = pieces[1:]
        for r in range(0, 3):
            if r >= 1:
                rotate(piece)

            for c in range(0, 10):
                e_state = copy.deepcopy(state)
                e_state.pose(c, piece)
                score_NN[10*r + c] = NN_search_eval_state(model, state, pieces, train, NN_play)

        return np.argmax(score_NN)

    # boards = [board]
    # for i in range(0, len(pieces)):
    #     next_boards = []
    #     for j in range(0, len(boards)):
    #         # on parcourt toutes les colonnes possibles
    #         for c in range(0, 10):
    #             pass


def game_run(model, draw_enable=False, nb_move=100, piece_set=[]):
    """
    bot: le bot a faire jouer
    model: le model qui va faire les predictions
    draw_enable: affichage graphique de la partie joue
    nb_moves: nombre de coup autorise dans la partie
    piece_set: suite de pieces avec lequel jouer
    """

    global board_draw
    global canv
    global root

    if len(piece_set) == 0:
        for i in range(0, nb_move + 10):
            piece_set.append(rand_piece())

    move_played = 0
    finish = False
    piece = piece_set[0]

    score = 0
    lines_cleared = 0

    state = State()
    piece_number = 1

    while not finish:
        choice = prediction(model, piece)
        state.move(choice, piece)
        move_played += 1
        piece = piece_set[piece_number]
        piece_number += 1

        if game_over(state.board) or move_played >= nb_move:
            finish = True
            # score += calculate_board_score()

        # if draw_enable:
        #     board_plus_piece = get_board_plus_piece(board, piece)
        #     draw(board_plus_piece, clean_board_draw(root))
        #     canv.update()
        #     time.sleep(0.005)
