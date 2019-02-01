import numpy as np

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