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
    #print("gen_NN")
    inputs = Input(shape=(12,))
    #x = Flatten()(inputs)
    x = Dense(30, activation='relu')(inputs)
    x = Dense(30, activation='relu')(x)
    x = Dense(30, activation='relu')(x)
    predictions = Dense(11, activation='softmax')(x)
    #print("avant creation model")

    model = Model(inputs=inputs, outputs=predictions)
    #print("set_weights")
    if len(genes) > 0:
        model.set_weights(genes)
    model._make_predict_function()
    #print("fin ")
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
    #print("debut croisement")

    list_enfants = []
    list_p = []

    count = 0
    w1 = b1.genes
    w2 = b2.genes

    for i in range(0, nb_enfants):
        # nombre aleatoire compris entre - 0.5 et 1.5 utiliser pour faire le croisement
        p = random.uniform(-0.5, 1.5)

        # poids du nouvel enfant
        e = np.multiply(p, w1) + np.multiply(w2, (1-p))

        # mutation couche par couche
        #print(len(e))
        for k in range(0, len(e)):
            if len(e[k].shape) > 1: # on skip les couches qui qui n'ont pas de poids
                #print("avant", e[k])
                matrice_muta = np.random.randn(e[k].shape[0], e[k].shape[1])
                e[k] += np.multiply(matrice_muta - 0.5, 0.005)
                #print("apres", e[k])
                pass

        list_enfants.append(e)
    #print("fin croisement")
    return list_enfants
    # on parcourt les couches des parents en simultanne
    """
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
    """
    #print("finis: ", nb_enfants)
    #print("count: ", count)
    #print("weights: ", list_enfants[0][2])
