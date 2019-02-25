import numpy as np

class Piece:
    def __init__(self):
        pass

class PieceI(Piece):

    def __init__(self):
        self.forme = 0
        self.bin_forme = np.array([1, 0, 0, 0, 0, 0, 0])
        self.name = "I"
        self.rot_num = 0
        self.pos = np.array([0, 0])
        self.tetro = np.array([[0, 0, 0, 0, 0],
                               [0, 0, 1, 0, 0],
                               [0, 0, 1, 0, 0],
                               [0, 0, 1, 0, 0],
                               [0, 0, 1, 0, 0]])

    def __repr__(self):
        return  "I"

class PieceJ(Piece):

    def __init__(self):
        self.forme = 1
        self.bin_forme = np.array([1, 0, 0, 0, 0, 0, 0])
        self.name = "J"
        self.rot_num = 0
        self.pos = np.array([0, 0])
        self.tetro = np.array([[1, 1, 0],
                               [0, 1, 0],
                               [0, 1, 0]])

    def __repr__(self):
        return  "J"


class PieceL(Piece):

    def __init__(self):
        self.forme = 2
        self.bin_forme = np.array([1, 0, 0, 0, 0, 0, 0])
        self.name = "L"
        self.rot_num = 0
        self.pos = np.array([0, 0])
        self.tetro = np.array([[0, 1, 0],
                               [0, 1, 0],
                               [0, 1, 1]])

    def __repr__(self):
        return  "L"

class PieceO(Piece):

    def __init__(self):
        self.forme = 3
        self.bin_forme = np.array([1, 0, 0, 0, 0, 0, 0])
        self.name = "O"
        self.rot_num = 0
        self.pos = np.array([0, 0])
        self.tetro = np.array([[1, 1],
                               [1, 1]])

    def __repr__(self):
        return  "O"

class PieceS(Piece):

    def __init__(self):
        self.forme = 4
        self.bin_forme = np.array([1, 0, 0, 0, 0, 0, 0])
        self.name = "S"
        self.rot_num = 0
        self.pos = np.array([0, 0])
        self.tetro = np.array([[0, 1, 0],
                               [1, 1, 0],
                               [1, 0, 0]])

    def __repr__(self):
        return  "S"

class PieceT(Piece):

    def __init__(self):
        self.forme = 5
        self.bin_forme = np.array([1, 0, 0, 0, 0, 0, 0])
        self.name = "T"
        self.rot_num = 0
        self.pos = np.array([0, 0])
        self.tetro = np.array([[0, 1, 0],
                               [1, 1, 0],
                               [0, 1, 0]])

    def __repr__(self):
        return  "T"

class PieceZ(Piece):

    def __init__(self):
        self.forme = 6
        self.bin_forme = np.array([1, 0, 0, 0, 0, 0, 0])
        self.name = "Z"
        self.rot_num = 0
        self.pos = np.array([0, 0])
        self.tetro = np.array([[1, 0, 0],
                               [1, 1, 0],
                               [0, 1, 0]])

    def __repr__(self):
        return  "W"
