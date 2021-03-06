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
from keras.layers import Dense, Input, Flatten, Conv2D, MaxPooling2D
import keras.backend as K
import tensorflow
from pynput.keyboard import Key, Controller, Listener
import copy
from multiprocessing.dummy import Pool as ThreadPool
from concurrent.futures import ThreadPoolExecutor
from tensorflow.python.client import device_lib

from piece import *
from bot import *
from utils import *

import os


def gen_NN(genes=[]):
    # Inputs
    pieces_input = Input(shape=(3 * 7 + 1,))
    board_input = Input(shape=(10, 20, 1))

    # First convolution extracts 16 filters that are 3x3
    # Convolution is followed by max-pooling layer with a 2x2 window
    conv_l = Conv2D(32, 2, activation="relu")(board_input)
    conv_l = MaxPooling2D(2)(conv_l)

    # Second convolution extracts 32 filters that are 3x3
    # Convolution is followed by max-pooling layer with a 2x2 window
    conv_l = Conv2D(64, 2, activation="relu")(conv_l)
    conv_l = MaxPooling2D(2)(conv_l)

    # Third convolution extracts 64 filters that are 3x3
    # Convolution is followed by max-pooling layer with a 2x2 window

    conv_l = Flatten()(conv_l)

    x = keras.layers.concatenate([conv_l, pieces_input])

    x = Dense(60, activation="relu")(x)
    x = Dense(40, activation="relu")(x)
    predictions = Dense(11, activation="softmax")(x)

    model = Model(inputs=[board_input, pieces_input], outputs=predictions)
    # print(model.summary())

    if len(genes) > 0:
        model.set_weights(genes)
    model._make_predict_function()

    return model


def croisement(w1, w2, nb_enfants):
    """
    b1.fitness > b2.fitness
    renvoie le croisement entre les poids des 2 parents
    c'est a dire 2 enfants avec des poids qui seront un mixte des parents
    """
    list_enfants = []

    for i in range(0, nb_enfants):
        # nombre aleatoire compris entre - 0.5 et 1.5 utiliser pour faire le croisement
        p = random.uniform(-0.5, 1.5)

        # poids du nouvel enfant
        e = np.multiply(p, w1) + np.multiply(w2, (1 - p))

        list_enfants.append(e)
    return list_enfants


def mutate(genes, nb, coeff):
    for k in range(0, len(genes)):
        if len(genes[k].shape) > 1 and random.randint(
            0, nb == 0
        ):  # on skip les couches qui qui n'ont pas de poids
            matrice_muta = np.random.random(genes[k].shape)
            genes[k] += np.multiply(matrice_muta - 0.5, coeff)


def mutate_list(list_bot, nb, coeff):
    l = len(list_bot)
    for i in range(0, l):
        mutate(list_bot[i], max(0, nb - (l - i)), coeff)

    return list_bot
