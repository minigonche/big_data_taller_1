# Modelo clasificador


#Clasificador polaridad
from classifier import *

# Librerias externas
import numpy as np
import pickle


# Clase que se encarga de la clasificacion

import nltk
from nltk.corpus import stopwords # Import the stop word list
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SpanishStemmer, EnglishStemmer
import pandas as pd
from sklearn.feature_extraction.text import HashingVectorizer, CountVectorizer
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import itertools
import operator
from scipy.sparse import vstack
import collections
import pprint
import sklearn
import pickle


class EncapsularClasificador:

    #Funcion stemmer
    def tokenizer_stemmer_global(document):
        stemmer = SpanishStemmer()
        my_tokenizer = RegexpTokenizer("[\w']+")
        return [stemmer.stem(token) for token in my_tokenizer.tokenize(document)]


    def __init__(self, modelo):


        self.vectorizer = CountVectorizer(analyzer = "word",
                                     tokenizer = EncapsularClasificador.tokenizer_stemmer_global,
                                     preprocessor = None,
                                     #stop_words = stopwords.words(idioma),
                                     strip_accents='ascii',
                                     encoding = 'utf-8',
                                     ngram_range = (1,3))
        self.modelo = modelo


    def predict(self, X_entrada):
        X_entrada = self.vectorizer.transform(X_entrada)
        return(self.modelo.predict(X_entrada))


    def fit(self, X_train, y_train):
        X_train = self.vectorizer.fit_transform(X_train)
        return(self.modelo.fit(X_train,y_train))

    def clone(clasificador):
        return(EncapsularClasificador(sklearn.base.clone(clasificador.modelo)))


class Clasificador:
    """
    Modelo clasificador de textos
    """

    def __init__(self, pickle_loc = "clasificadores_entrenados"):

        self.polaridad = SentimentClassifier()

        with open(pickle_loc + '/SEXISMO_machine.pkl', "rb") as input_file:
            self.sexismo = pickle.load(input_file)

        with open(pickle_loc + '/MATONEO_machine.pkl', "rb") as input_file:
            self.matoneo = pickle.load(input_file)


    def dar_polaridad(self, text):
        """
            Metodo que devuelve la polaridad de un texto dado
        """

        pred = self.polaridad.predict(text)*2 - 1
        return(int(np.round(pred)))


    def dar_sexismo(self, text):
        """
            Metodo que devuelve el sexismo de un texto dado
        """
        pred = self.sexismo.predict([text])
        return(int(np.round(pred[0])))


    def dar_matoneo(self, text):
        """
            Metodo que devuelve el matoneo de un tuit
        """
        # TODO: Por ahora esta con la libreria externa
        pred = self.matoneo.predict([text])
        return(int(np.round(pred[0])))
