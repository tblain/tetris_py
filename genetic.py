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
from keras.layers import Dense, Input, Flatten
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
    inputs = Input(shape=(202,))
    #x = Flatten()(inputs)
    x = Dense(10, activation='relu')(inputs)
    x = Dense(10, activation='relu')(x)
    x = Dense(10, activation='relu')(x)
    predictions = Dense(4, activation='softmax')(x)

    model = Model(inputs=inputs, outputs=predictions)

    if len(genes) > 0:
        model.set_weights(genes)
    model._make_predict_function()

    return model

def croisement(b1, b2, nb_enfants):
    """
    b1.fitness > b2.fitness
    renvoie le croisement entre les poids des 2 parents
    c'est a dire 2 enfants avec des poids qui seront un mixte des parents
    """
    #b1 = args[0]
    #b2 = args[1]
    #nb_enfants = args[2]
    bw1 = b1.model.get_weights()
    bw2 = b2.model.get_weights()

    list_enfants = []
    list_p = []

    count = 0

    for i in range(0, nb_enfants):
        # poids des deux enfants qu'on initialise avec les poids des parents
        list_enfants.append(b1.model.get_weights())
        # nombre aleatoire compris entre - 0.5 et 1.5 utiliser pour faire le croisement
        list_p.append(random.uniform(-0.5, 1.5))

    # on parcourt les couches des parents en simultanne

    for k in range(0, len(bw1)):
        lbw1 = bw1[k]
        lbw2 = bw2[k]
        if len(lbw1.shape) > 1: # on skip les couches qui qui n'ont pas de poids
            nb_col = lbw1.shape[0]
            nb_row = lbw2.shape[1]

            # on update les poids de la couche
            for i in range(0, nb_col):
                for j in range(0, nb_row):
                    v1 = lbw1[i, j]
                    v2 = lbw2[i, j]
                    for e in range(0, len(list_enfants)):
                        count += 1
                        p = list_p[e]
                        list_enfants[e][k][i, j] = p * v1 + (1-p) * v2 + random.uniform(-0.5, 0.5)

    #print("finis: ", nb_enfants)
    #print("count: ", count)
    #print("weights: ", list_enfants[0][2])
    return list_enfants
