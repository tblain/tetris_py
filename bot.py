import numpy as np
import copy

# from piece import *
# from utils import *
# from genetic import *


class Bot:
    def __init__(self, genes=[]):
        self.genes = genes
        self.fitness = 0
        self.score = 0
        self.penalite = 0
        self.nb_run = 0
        self.lines_cleared = 0

    def play(self, model, next_pieces):  # joue un coup
        data = self.board
        data = data.reshape(1, 10, 20, 1)
        piece_input = np.array([self.piece.rot_num]).reshape((1, 1))
        piece_input = np.hstack((piece_input, self.piece.bin_forme.reshape(1, 7)))
        next_pieces_bin_formes = np.array([piece.bin_forme for piece in next_pieces])

        piece_input = np.hstack((piece_input, next_pieces_bin_formes.reshape(1, 7*2)))

        prediction = model.predict_on_batch([data, piece_input])

        choice = np.argmax(prediction)

        if choice == 0 and False:
            print("0000000000000000")

        if choice == 10:
            self.rotate(3)
            return False
        else:
            for i in range(0, choice):
                self.move("right")
            self.direct_pose()
            return True

    def move(self, dir):  # deplace la piece dans la direction indique
        if dir == "down":
            if self.outside([0, 1]) or self.overlap("down"):
                self.push_on_board()
            else:
                self.piece.pos += np.array([0, 1])
        elif dir == "right":
            if not self.overlap("right") and not self.outside([1, 0]):
                self.piece.pos += np.array([1, 0])
        elif dir == "left":
            if not self.overlap("left") and not self.outside([-1, 0]):
                self.piece.pos += np.array([-1, 0])

    def direct_pose(self):
        # l = len(self.piece.tetro)
        # px = self.piece.pos[0]
        # py = self.piece.pos[1]

        if not self.overlap() and not self.outside([0, 0]):
            while not self.overlap("down") and not self.outside([0, 1]):
                self.piece.pos[1] += 1
            self.push_on()

    def calculate_board_score(self):  # return the score for the current game
        b = self.board
        board_score = 0

        for i in range(0, 10):
            full_combo = 5
            for j in range(0, 20):
                if b[i, j] == 1:
                    board_score += full_combo + j
                    full_combo = min(20, full_combo + 5)
                else:
                    full_combo = 1

        return board_score / 10

    def rotate(self, n=1):
        # rotate the tetro matrice
        t = copy.copy(self.piece.tetro)
        l = len(t)
        for i in range(0, l // 2):
            for j in range(i, l - i - 1):
                temp = t[i][j]
                t[i, j] = t[l - 1 - j, i]
                t[l - 1 - j, i] = t[l - 1 - i, l - 1 - j]
                t[l - 1 - i, l - 1 - j] = t[j, l - 1 - i]
                t[j, l - 1 - i] = temp

        self.piece.rot_num += 1
        if self.piece.rot_num == 3:
            self.piece.rot_num = 0

        if self.overlap() or self.outside([0, 0]):
            self.piece.tetro = t

        if n > 1:
            self.rotate(n - 1)

    def push_on(self):  # met la piece definitivement dans le board
        # self.score += 10 - self.penalite
        lenght = len(self.piece.tetro)
        px = self.piece.pos[0]
        py = self.piece.pos[1]

        for i in range(0, lenght):
            for j in range(0, lenght):
                if self.piece.tetro[i][j] == 1:
                    # print("p: ", self.piece.tetro, " | px: ", px+l, "| py ", py+l)
                    # print(self.board)
                    self.board[px + i][py + j] = 1
        self.remove_full_lines()

    def outside(self, dirvec):
        # renvoie si la piece est en dehors du tableau ou non
        # apres avoir applique la direction en arg
        p = copy.copy(self.piece)
        lenght = len(p.tetro)
        px = p.pos[0] + dirvec[0]
        py = p.pos[1] + dirvec[1]

        for i in range(0, lenght):
            for j in range(0, lenght):
                if p.tetro[i, j] == 1 and (px + i >= 10 or px + i < 0 or py + j >=  20 or py + j < 0 ):
                    return True
        return False

    def overlap(self, action=None):
        len = len(self.piece.tetro)
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
            for i in range(0, len):
                for j in range(0, len):
                    if self.piece.tetro[i][j] == 1 and self.board[px + i][py + j] == 1:
                        return True
        return False

    def remove_full_lines(self):
        for j in range(0, 20):
            full = True
            for i in range(0, 10):
                if self.board[i, j] == 0:
                    full = False

            if full:
                self.lines_cleared += 1
                for y in range(j, 1, -1):
                    for x in range(0, 10 - 1):
                        self.board[x, y] = self.board[x, y - 1]

    def get_fitness(self):
        return self.score / self.nb_run

    def get_lines_cleared(self):
        return self.lines_cleared / self.nb_run
