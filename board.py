import numpy as np


class Board():
    def __init__(self, board=np.zeros((10, 20), dtype=int), score=0, remove_full_lines=0):
        self.board = board
        self.score = score
        self.remove_full_lines = remove_full_lines

    def move(self, col, piece):
        # pose la piece dans la colonne indique
        for i in range(0, col):
            self.move_right(piece)
        self.direct_pose(piece)

    def move_right(self, piece):
        piece.pos += np.array([1, 0])

    def outside(self, dirvec, piece):
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

    def overlap(self, action=None, piece):
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

        if not self.outside(dirvec, piece):
            for i in range(0, len):
                for j in range(0, len):
                    if self.piece.tetro[i][j] == 1 and self.board[px + i][py + j] == 1:
                        return True
        return False

    def direct_pose(self, piece):
        # l = len(self.piece.tetro)
        # px = self.piece.pos[0]
        # py = self.piece.pos[1]

        if not self.overlap(piece=piece) and not self.outside([0, 0], piec):
            while not self.overlap("down", piece) and not self.outside([0, 1], piece):
                piece.pos[1] += 1
            self.push_on(piece)

    def push_on(self): 
        # met la piece definitivement dans le board
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

    def push_on(self, piec):
        # met la piece definitivement dans le board
        lenght = len(piece.tetro)
        px = self.piece.pos[0]
        py = self.piece.pos[1]

        for i in range(0, lenght):
            for j in range(0, lenght):
                if piece.tetro[i][j] == 1:
                    # print(self.board)
                    self.board[px + i][py + j] = 1
        self.remove_full_lines()

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
