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
    inputs = Input(shape=(210,))
    #x = Flatten()(inputs)
    x = Dense(30, activation='relu')(inputs)
    x = Dense(30, activation='relu')(x)
    x = Dense(20, activation='relu')(x)
    predictions = Dense(11, activation='softmax')(x)
    #print("avant creation model")

    model = Model(inputs=inputs, outputs=predictions)
    #print("set_weights")
    if len(genes) > 0:
        model.set_weights(genes)
    model._make_predict_function()
    #print("fin ")
    return model

def croisement(w1, w2, nb_enfants):
    """
    b1.fitness > b2.fitness
    renvoie le croisement entre les poids des 2 parents
    c'est a dire 2 enfants avec des poids qui seront un mixte des parents
    """
    list_enfants = []
    list_p = []

    count = 0

    for i in range(0, nb_enfants):
        # nombre aleatoire compris entre - 0.5 et 1.5 utiliser pour faire le croisement
        p = random.uniform(-0.5, 1.5)

        # poids du nouvel enfant
        e = np.multiply(p, w1) + np.multiply(w2, (1-p))

        list_enfants.append(e)
    return list_enfants

def mutate(list_bot, nb, coeff): # proba: 1 bot sur nb sera mute
    list_proba = np.multiply(np.random.rand(len(list_bot)), nb)
    for i in range(0, len(list_bot)):
        if list_proba[i] <= 1:
            e = list_bot[i].genes
            for k in range(0, len(e)):
                if len(e[k].shape) > 1: # on skip les couches qui qui n'ont pas de poids
                    #print("avant", e[k])
                    matrice_muta = np.random.randn(e[k].shape[0], e[k].shape[1])
                    e[k] += np.multiply(matrice_muta - 0.5, coeff)


    return list_bot
