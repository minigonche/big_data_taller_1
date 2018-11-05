# Modelo clasificador


#Clasificador polaridad
from classifier import *

# Librerias externas
import numpy as np
import pickle


class Clasificador:
    """
    Modelo clasificador de textos
    """

    def __init__(self, pickle_loc = "clasificador.pkl"):

        self.polaridad = SentimentClassifier()
        #with open(pickle_loc, "rb") as input_file:
        #    self.clasificador = pickle.load()


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


        # TODO: Por ahora esta con la libreria externa

        pred = self.polaridad.predict(text)*5 - 2
        return(int(np.round(pred)))
