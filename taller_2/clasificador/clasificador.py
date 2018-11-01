# Modelo clasificador


#Clasificador preentrenado
from classifier import *


# Librerias externas
import numpy as np



class Clasificador:
    """
    Modelo clasificador de textos
    """

    def __init__(self):

        self.preentrenado = SentimentClassifier()

    def dar_polaridad(self, text):
        """
            Metodo que devuelve la polaridad de un texto dado
        """

        pred = self.preentrenado.predict(text)*2 - 1
        return(int(np.round(pred)))


    def dar_polaridad(self, text):
        """
            Metodo que devuelve la polaridad de un texto dado
        """

        pred = self.preentrenado.predict(text)*2 - 1
        return(int(np.round(pred)))


    def dar_sexismo(self, text):
        """
            Metodo que devuelve el sexismo de un texto dado
        """


        # TODO: Por ahora esta con la libreria externa

        pred = self.preentrenado.predict(text)*5 - 2
        return(int(np.round(pred)))
