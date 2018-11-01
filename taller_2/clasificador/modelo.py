# Clase que se encarga de la clasificacion

import nltk
from nltk.corpus import stopwords # Import the stop word list
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SpanishStemmer, EnglishStemmer
import pandas as pd
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import itertools
import operator
from scipy.sparse import vstack
import collections

class Clasificador:

    def __init__(self, modelo, vectorizer):
        self.vectorizer = vectorizer
        self.modelo = modelo


    def predict(self, X_entrada):
        X_entrada = self.vectorizer.fit_transform(X_entrada)
        return(self.modelo.predict(X_entrada))



def balanced_split(X,y, test_size = 0.2):
    """
    Metodo que divide la muestra de forma balanceada
    """

    X_train, X_test, y_train, y_test = None, None, None, None

    labels = np.unique(y)
    y = np.array(y)

    for lab in labels:
        X_label = X[y == lab]
        y_label = y[y == lab]

        X_label_train, X_label_test, y_label_train, y_label_test = train_test_split(X_label, y_label, test_size=test_size)

        if(X_train is None):
            X_train, X_test, y_train, y_test = X_label_train, X_label_test, y_label_train, y_label_test
        else:
            X_train = vstack([X_train, X_label_train])
            X_test = vstack([X_test, X_label_test])
            #Numpy structures
            y_train = np.concatenate((y_train,y_label_train))
            y_test = np.concatenate((y_test,y_label_test))

    return(X_train, X_test, y_train, y_test)



def configurar_modelo(X, y, idioma = 'SPANISH', fitness = accuracy_score):
    """
    Metodo que encuentra la mejor maquina de soporte vectorial para el problema.


    Parameters
    ----------
    X : lista de String
        Lista con los textos de los tuits sobre los que se quiere entrenar

    y : lista de int
        Lista correspondiente con la clases de cada uno de los elementos de la muestra

    idioma : String
        SPANISH o ENGLISH dependiendo del idioma de la muestra

    fitness : funcion(y1,y2)
        Funcion para calcular la aptitud de los calsificadores. Recibe dos parametros,
        donde el primer parametro corresponde a las etiquetas de las clases reales y el segundo
        al encontrado. Debe devolver un valor numerico, donde numeros mayores corresponden a
        mejor aptitud
    """

    # Constante para
    round_num = 4

    #Prepara los datos

    #Tokenizador
    my_tokenizer = RegexpTokenizer("[\w']+")

    if(idioma == 'SPANISH'):
        stemmer = SpanishStemmer()
    elif(idioma == 'ENGLISH'):
        stemmer = EnglishStemmer()


    #Funcion stemmer
    def tokenizer_stemmer(document):
        return [stemmer.stem(token) for token in my_tokenizer.tokenize(document)]

    vectorizer = HashingVectorizer(analyzer = "word",
                                 tokenizer = tokenizer_stemmer,
                                 preprocessor = None,
                               #  stop_words = stopwords.words("spanish"),
                                 n_features = 10000,
                                 strip_accents='ascii',
                                 encoding = 'utf-8',
                                 ngram_range = (1,3))


    X = vectorizer.fit_transform(X)

    kernels = []
    kernels.append('linear')
    kernels.append('polynomial')
    kernels.append('rbf')
    kernels.append('sigmoid')

    #Parameters
    num_ite = 20
    C = [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000]
    coef = [-10,0,10]
    degrees = [2,3,4,5]
    gamma = [0.1,1,10]

    # parametros de prueba
    # Quitar comentarios para correr esquema mas pequenho
    #num_ite = 2
    #C = [10]
    #coef = [0]
    #degrees = [2]
    #gamma = [0.1]


    machines = {}
    final_scores = {}

    if('linear' in kernels):
        #Kernel Lineal
        configurations = list(itertools.product(C))
        scores = {}

        print('Linear Kernel')
        for i in range(num_ite):
            print('     Iteration ' + str(i+1) + ' of ' + str(num_ite))

            #Divide los datos
            X_train, X_test, y_train, y_test = balanced_split(X, y, test_size=0.2)

            for conf in configurations:

                clf = svm.SVC(C=conf[0], kernel = 'linear', gamma='scale', decision_function_shape='ovo')
                clf.fit(X_train, y_train)

                y_predicted = clf.predict(X_test)

                score = fitness(y_test, y_predicted)

                if(conf not in scores):
                    scores[conf] = 0

                scores[conf] = scores[conf] + score

                print('         Configuration: C = ' + str(conf[0]) + ' -- Score: ' + str(np.round(score,round_num)))

        scores = {k: v / num_ite for k, v in scores.items()}

        print(' ')

        conf = max(scores.items(), key=operator.itemgetter(1))[0]
        print(' Max Score: ' + str(scores[conf]))
        final_scores['linear'] = scores[conf]
        machines['linear'] = svm.SVC(C=conf[0], kernel = 'linear', gamma='scale', decision_function_shape='ovo')

        print(' ')

    if('polynomial' in kernels):
        #Kernel polynomial
        configurations = list(itertools.product(C,degrees, coef))
        scores = {}

        print('Polynomial Kernel')

        for i in range(num_ite):
            print('     Iteration ' + str(i+1) + ' of ' + str(num_ite))

            #Divide los datos
            X_train, X_test, y_train, y_test = balanced_split(X, y, test_size=0.2)

            for conf in configurations:

                clf = svm.SVC(C=conf[0], kernel = 'poly', gamma='scale', decision_function_shape='ovo', degree = conf[1], coef0 = conf[2])
                clf.fit(X_train, y_train)

                y_predicted = clf.predict(X_test)

                score = fitness(y_test, y_predicted)

                if(conf not in scores):
                    scores[conf] = 0

                scores[conf] = scores[conf] + score

                print('         Configuration: C = ' + str(conf[0]) + ', deg = ' + str(conf[1]) + ' coef = ' + str(conf[2])+ ' -- Score: ' + str(np.round(score,round_num)))

        scores = {k: v / num_ite for k, v in scores.items()}

        print(' ')

        conf = max(scores.items(), key=operator.itemgetter(1))[0]
        print(' Max Score: ' + str(scores[conf]))
        final_scores['polynomial'] = scores[conf]
        machines['polynomial'] = svm.SVC(C=conf[0], kernel = 'poly', gamma='scale', decision_function_shape='ovo', degree = conf[1], coef0 = conf[2])

        print(' ')



    if('rbf' in kernels):
        #Kernel polynomial
        configurations = list(itertools.product(C,gamma))
        scores = {}

        print('RBF Kernel')

        for i in range(num_ite):
            print('     Iteration ' + str(i+1) + ' of ' + str(num_ite))

            #Divide los datos
            X_train, X_test, y_train, y_test = balanced_split(X, y, test_size=0.2)

            for conf in configurations:

                clf = svm.SVC(C=conf[0], kernel = 'rbf', gamma=conf[1], decision_function_shape='ovo')
                clf.fit(X_train, y_train)

                y_predicted = clf.predict(X_test)

                score = fitness(y_test, y_predicted)

                if(conf not in scores):
                    scores[conf] = 0

                scores[conf] = scores[conf] + score

                print('         Configuration: C = ' + str(conf[0]) + ', gamma = ' + str(conf[1]) + ' -- Score: ' + str(np.round(score,round_num)))

        scores = {k: v / num_ite for k, v in scores.items()}

        print(' ')

        conf = max(scores.items(), key=operator.itemgetter(1))[0]
        print(' Max Score: ' + str(scores[conf]))
        final_scores['rbf'] = scores[conf]
        machines['rbf'] = svm.SVC(C=conf[0], kernel = 'rbf', gamma=conf[1], decision_function_shape='ovo')

        print(' ')


    if('sigmoid' in kernels):
        #Kernel polynomial
        configurations = list(itertools.product(C, coef))
        scores = {}

        print('Sigmoid Kernel')

        for i in range(num_ite):
            print('     Iteration ' + str(i+1) + ' of ' + str(num_ite))

            #Divide los datos
            X_train, X_test, y_train, y_test = balanced_split(X, y, test_size=0.2)

            for conf in configurations:

                clf = svm.SVC(C=conf[0], kernel = 'sigmoid', gamma='scale', decision_function_shape='ovo', coef0 = conf[1])
                clf.fit(X_train, y_train)

                y_predicted = clf.predict(X_test)

                score = fitness(y_test, y_predicted)

                if(conf not in scores):
                    scores[conf] = 0

                scores[conf] = scores[conf] + score

                print('         Configuration: C = ' + str(conf[0]) + ' coef = ' + str(conf[1])+ ' -- Score: ' + str(np.round(score,round_num)))

        scores = {k: v / num_ite for k, v in scores.items()}

        print(' ')

        conf = max(scores.items(), key=operator.itemgetter(1))[0]
        print(' Max Score: ' + str(scores[conf]))
        final_scores['sigmoid'] = scores[conf]
        machines['sigmoid'] = svm.SVC(C=conf[0], kernel = 'sigmoid', gamma='scale', decision_function_shape='ovo', coef0 = conf[1])

        print(' ')


    ker = max(final_scores.items(), key=operator.itemgetter(1))[0]

    final_machine = machines[ker]

    print('')
    print('Best Kernel: ' + str(ker))
    print('Score: ' + str(final_scores[ker]))

    final_machine.fit(X,y)


    clasificador = Clasificador(final_machine, vectorizer)
    return(clasificador)


data = pd.read_csv('data/dataset_otro.txt', sep='\t', encoding = "ISO-8859-1")
data = data.loc[data['rating.mode']!=4]

clf = configurar_modelo(data['content'].values.tolist(), data['rating.mode'].values.tolist(), idioma = "ENGLISH")

print(clf.predict(["I'm sick and tired of the decisions that the president is taking. No more!","cheers for the NYP and their amazing work!"]))
