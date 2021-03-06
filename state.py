import numpy as np
import copy


class State():
    def __init__(self, board=np.zeros((10, 20), dtype=float), score=0, cleared_lines=0):
        self.board = np.zeros((10, 20))
        self.board[:] = board
        self.score = score
        self.cleared_lines = cleared_lines

    def pose(self, col, piece):
        # pose la piece dans la colonne indique
        for i in range(0, col):
            self.move_right(piece)
        self.direct_pose(piece)

    def move_right(self, piece):
        if not self.overlap(piece, "right") and not self.outside([1, 0], piece):
            piece.pos += np.array([1, 0])

    def outside(self, dirvec, piece):
        # renvoie si la piece est en dehors du tableau ou non
        # apres avoir applique la direction en arg
        # p = copy.copy(piece)
        p = piece
        lenght = len(p.tetro)
        px = p.pos[0] + dirvec[0]
        py = p.pos[1] + dirvec[1]

        for i in range(0, lenght):
            for j in range(0, lenght):
                if p.tetro[i, j] == 1 and (px + i >= 10 or px + i < 0 or py + j >= 20 or py + j < 0):
                    return True
        return False

    def overlap(self, piece, action=None):
        lenght = len(piece.tetro)
        dirvec = [0, 0]
        px = piece.pos[0]
        py = piece.pos[1]

        if action == "down":
            py += 1
            dirvec = [0, 1]

        if action == "right":
            px += 1
            dirvec = [1, 0]

        if action == "left":
            px -= 1
            dirvec = [-1, 0]

        if not self.outside(dirvec, piece):
            for i in range(0, lenght):
                for j in range(0, lenght):
                    if piece.tetro[i][j] == 1 and self.board[px + i][py + j] == 1:
                        return True
        return False

    def direct_pose(self, piece):
        # l = len(piece.tetro)
        # px = piece.pos[0]
        # py = piece.pos[1]
        # piece = copy.deepcopy(piece)

        if not self.overlap(piece=piece) and not self.outside([0, 0], piece):
            while not self.overlap(piece, "down") and not self.outside([0, 1], piece):
                piece.pos[1] += 1
            self.push_on(piece)

    def push_on(self, piece):
        # met la piece definitivement dans le board
        # piece = copy.deepcopy(piece)
        lenght = len(piece.tetro)
        px = piece.pos[0]
        py = piece.pos[1]

        for i in range(0, lenght):
            for j in range(0, lenght):
                if piece.tetro[i][j] == 1:
                    self.board[px + i][py + j] = 1

        # print("test")
        self.score += 10
        self.remove_full_lines()

    def remove_full_lines(self):
        for j in range(0, 20):
            full = True
            for i in range(0, 10):
                if self.board[i, j] == 0:
                    full = False

            if full:
                # print("remove_full_lines")
                self.cleared_lines += 1
                for y in range(j, 1, -1):
                    for x in range(0, 10 - 1):
                        self.board[x, y] = self.board[x, y - 1]

    def affichage(self):
        for i in range(0, 20):
            print("|", end='')
            for j in range(0, 10):
                if self.board[j, i] == 1:
                    print('O', end='')
                else:
                    print(' ', end='')
            print("|")
