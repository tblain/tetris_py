import numpy as np
import copy
from tqdm import tqdm

from utils import rand_piece, rotate, game_over
from state import State


def eval_board(state, depth):
    b = state.board
    board_score = 0
    board_max_heights = np.zeros(10)
    for i in range(0, 10):
        points = 10
        penal = 0
        max_height = 0
        for j in range(19, 0, -1):
            if b[i, j] == 1:
                board_score += points
                board_score -= penal
                penal = 0
                max_height = 19 - j
            else:
                points = max(1, points - 5)
                penal += 5

        board_max_heights[i] = max_height

    biggest_height = np.max(board_max_heights)
    for h in board_max_heights:
        board_score -= biggest_height - h

    return board_score + state.cleared_lines * 1000


def compare_board():
    pass


def NN_predic_eval_state(model, state, train=False, target=0):
    # evalue le score d'un board
    data = state.board.flatten()
    data = np.append(data, state.score)
    data = np.append(data, state.cleared_lines)
    # print(data.shape)
    predic = model.predict(data) * 1000
    if train:
        model.fit_on_one(data, target / 1000, 0.00005)
        # print(model.weights)
        for w in model.weights:
            # print(w)
            pass
        print(predic, " / ", target / 1000)

    return predic


def NN_search_eval_state(model, state, pieces, train=False, NN_play=True):
    # TODO: changer les param train, NN_play car c'est assez nul
    """
    model: reseau de neurones qui va faire les predictions
    state: etat du jeu a evaluer
    pieces: suites de pieces a utiliser pour evaluer le state de base
    train: est-ce que l'on entraine le model
    NN_play: est-ce que l'on utilise la prediction du NN ou de l'algo
             pour faire l'evaluation
             si non c'est comme si c'etait l'algo qui jouait
             et le model ce fait juste entrainer

    le principe: comme on connait la suite de piece sur laquelle on va joue
        il faut choisir le coup qui nous permet d'atteindre le meilleur state
        possible, on renvoie donc toujours le max
    """

    if len(pieces) == 1:
        score_NN = np.zeros(30)
        score_algo = np.zeros(30)
        # piece = copy.deepcopy(pieces[0])
        piece = pieces[0]

        # on parcourt toutes les possibilites de jeux et on les evalue
        for r in range(0, 3):
            if r >= 1:
                rotate(piece)

            for c in range(0, 10):
                e_piece = copy.deepcopy(piece)
                e_state = State(state.board[:], state.score, state.cleared_lines)
                e_state.pose(c, e_piece)

                # on stoque les scores
                if train:
                    score_algo[10 * r + c] = eval_board(e_state, 2)
                    # print(e_piece.pos)
                    # score_NN[10*r + c] = NN_predic_eval_state(model, e_state, train, score_algo[10*r + c])
                    # TODO : model.fit + faire un fit stochiastic dans le NN
                else:
                    score_NN[10 * r + c] = NN_predic_eval_state(model, e_state)

        # on retourne la valeur max
        if NN_play:
            return np.max(score_NN)
        else:
            return np.max(score_algo)
    else:
        score_NN = np.zeros(30)
        piece = copy.deepcopy(pieces[0])
        pieces = pieces[1:]
        for r in range(0, 3):
            if r >= 1:
                rotate(piece)

            for c in range(0, 10):
                e_piece = copy.deepcopy(piece)
                # e_state = copy.deepcopy(state)
                e_state = State(state.board[:], state.score, state.cleared_lines)
                e_state.pose(c, piece)
                score_NN[10 * r + c] = NN_search_eval_state(
                    model, e_state, pieces, train, NN_play
                )
        # print(score_NN)

        return np.max(score_NN)


def NN_choose_move(model, state, pieces, train=False, NN_play=True):
    score = np.zeros(30)
    piece = copy.deepcopy(pieces[0])

    # on parcourt toutes les possibilites de jeux et on les evalue
    for r in tqdm(range(0, 3)):
        if r >= 1:
            rotate(piece)

        for c in range(0, 10):
            e_piece = copy.deepcopy(piece)
            e_state = copy.deepcopy(state)
            e_state.pose(c, e_piece)

            # on stoque les scores
            score[10 * r + c] = NN_search_eval_state(
                model, e_state, pieces[1:], train, NN_play
            )

    choice = np.argmax(score)
    return choice // 10, choice % 10


def game_run(model, draw_enable=False, nb_move=1000, piece_set=[]):
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
    piece_number = 0
    finish = False

    state = State()

    while not finish:
        # TODO : modfier le nom et les arguments de game_run pour rendre ca plus adaptable
        # print(state.board)
        state.affichage()
        # e_state = copy.deepcopy(state)
        r, col = NN_choose_move(
            model, state, piece_set[piece_number : piece_number + 2], True, False
        )
        print("r: ", r, " / col: ", col)

        # print(piece_set[piece_number].rot_num)
        for _ in range(0, r):
            rotate(piece_set[piece_number])

        state.pose(col, piece_set[piece_number])
        move_played += 1
        piece_number += 1

        if game_over(state.board) or move_played >= nb_move:
            finish = True
            # score += calculate_board_score()

        # if draw_enable:
        #     board_plus_piece = get_board_plus_piece(board, piece)
        #     draw(board_plus_piece, clean_board_draw(root))
        #     canv.update()
        #     time.sleep(0.005)
