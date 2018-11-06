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


def balanced_split(X,y, test_size = 0.2):
    """
    Metodo que divide la muestra de forma balanceada
    """

    if(type(X) == type([1,2])):
        X = np.array(X)

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
            if(type(X_train) == type(np.array([1]))):
                X_train = np.concatenate((X_train, X_label_train))
                X_test = np.concatenate((X_test, X_label_test))
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

    hash_vectorizer = HashingVectorizer(analyzer = "word",
                                 tokenizer = tokenizer_stemmer,
                                 preprocessor = None,
                                 #stop_words = stopwords.words(idioma),
                                 n_features = 10000,
                                 strip_accents='ascii',
                                 encoding = 'utf-8',
                                 ngram_range = (1,3))

    count_vectorizer = CountVectorizer(analyzer = "word",
                                 tokenizer = tokenizer_stemmer,
                                 preprocessor = None,
                                 #stop_words = stopwords.words(idioma),
                                 strip_accents='ascii',
                                 encoding = 'utf-8',
                                 ngram_range = (1,3))


    hash_vectorizer = count_vectorizer

    X_svm = hash_vectorizer.fit_transform(X)
    X_mnb = count_vectorizer.fit_transform(X)



    prueba = False

    #Parameters
    if(not prueba):
        option_machines = []
        option_machines.append('linear')
        option_machines.append('polynomial')
        option_machines.append('rbf')
        option_machines.append('sigmoid')
        option_machines.append('bayes')
        num_ite = 5
        C = [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000]
        coef = [-10,0,10]
        degrees = [2,3,4,5]
        gamma = [0.1,1,10]
        alpha = [0,0.5,1,5,10]
    else:
        option_machines = []
        option_machines.append('linear')
        option_machines.append('bayes')
        num_ite = 2
        C = [10]
        coef = [0]
        degrees = [2]
        gamma = [0.1]
        alpha = [1]

    machines = {}
    final_scores = {}

    if('linear' in option_machines):
        #Kernel Lineal
        configurations = list(itertools.product(C))
        scores = {}

        print('Linear Kernel')
        for i in range(num_ite):
            print('     Iteration ' + str(i+1) + ' of ' + str(num_ite))

            #Divide los datos
            X_train, X_test, y_train, y_test = balanced_split(X_svm, y, test_size=0.2)

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

    if('polynomial' in option_machines):
        #Kernel polynomial
        configurations = list(itertools.product(C,degrees, coef))
        scores = {}

        print('Polynomial Kernel')

        for i in range(num_ite):
            print('     Iteration ' + str(i+1) + ' of ' + str(num_ite))

            #Divide los datos
            X_train, X_test, y_train, y_test = balanced_split(X_svm, y, test_size=0.2)

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



    if('rbf' in option_machines):
        #Kernel polynomial
        configurations = list(itertools.product(C,gamma))
        scores = {}

        print('RBF Kernel')

        for i in range(num_ite):
            print('     Iteration ' + str(i+1) + ' of ' + str(num_ite))

            #Divide los datos
            X_train, X_test, y_train, y_test = balanced_split(X_svm, y, test_size=0.2)

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


    if('sigmoid' in option_machines):
        #Kernel polynomial
        configurations = list(itertools.product(C, coef))
        scores = {}

        print('Sigmoid Kernel')

        for i in range(num_ite):
            print('     Iteration ' + str(i+1) + ' of ' + str(num_ite))

            #Divide los datos
            X_train, X_test, y_train, y_test = balanced_split(X_svm, y, test_size=0.2)

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


    if('bayes' in option_machines):

        #Bayes
        configurations = list(itertools.product(alpha))
        scores = {}

        print('Multinomial Bayes')

        for i in range(num_ite):
            print('     Iteration ' + str(i+1) + ' of ' + str(num_ite))

            #Divide los datos
            X_train, X_test, y_train, y_test = balanced_split(X_mnb, y, test_size=0.2)

            for conf in configurations:

                clf = MultinomialNB(alpha = conf[0])
                clf.fit(X_train, y_train)

                y_predicted = clf.predict(X_test)

                score = fitness(y_test, y_predicted)

                if(conf not in scores):
                    scores[conf] = 0

                scores[conf] = scores[conf] + score

                print('         Configuration: alpha = ' + str(conf[0]) + ' -- Score: ' + str(np.round(score,round_num)))

        scores = {k: v / num_ite for k, v in scores.items()}

        print(' ')

        conf = max(scores.items(), key=operator.itemgetter(1))[0]
        print(' Max Score: ' + str(scores[conf]))
        final_scores['bayes'] = scores[conf]
        machines['bayes'] = MultinomialNB(alpha = conf[0])

        print(' ')


    mac = max(final_scores.items(), key=operator.itemgetter(1))[0]

    final_machine = machines[mac]

    print('')
    print('Best Machine: ' + str(mac))
    print('Score: ' + str(final_scores[mac]))


    if(mac == 'bayes'):
        final_vectorizer = count_vectorizer
    else:
        final_vectorizer = hash_vectorizer

    clasificador = EncapsularClasificador(final_machine)

    class_results = {}
    class_results['accuracy'] = []

    unique_classes = np.unique(y).tolist()

    for cla in unique_classes:
        class_results[cla] = {}
        class_results[cla]['precision'] = []
        class_results[cla]['recall'] = []


    #Constructs final statistics
    print('')
    print('Constructing Final Statistics')
    print('')
    for i in range(num_ite):

        print('Iteration ' + str(i+1) + ' of ' + str(num_ite))
        maquina = EncapsularClasificador.clone(clasificador)
        X_train, X_test, y_train, y_test = balanced_split(X, y, test_size=0.2)

        maquina.fit(X_train,y_train)
        y_predicted = maquina.predict(X_test)

        class_results['accuracy'].append(accuracy_score(y_test, y_predicted))

        for cla in unique_classes:
            #precision
            sub_test = y_test[y_predicted == cla]
            precision = np.sum(sub_test == cla)/(max(len(sub_test),1))
            #print('Precision for class ' + str(cla) + ': '+ str(precision))
            class_results[cla]['precision'].append(precision)

            #recall
            sub_test = y_predicted[y_test == cla]
            recall = np.sum(sub_test == cla)/(max(len(sub_test),1))
            #print('Recall for class ' + str(cla) + ': '+ str(recall))
            class_results[cla]['recall'].append(recall)

    class_results_consolidated = {}
    class_results_consolidated['accuracy'] = np.round(100*np.mean(class_results['accuracy']),3)

    for cla in unique_classes:
        class_results_consolidated[cla] = {}

        precision = np.round(100*np.mean(class_results[cla]['precision']),3)
        recall = np.round(100*np.mean(class_results[cla]['recall']),3)

        class_results_consolidated[cla]['precision'] = precision
        class_results_consolidated[cla]['recall'] = recall


    pprint.pprint(class_results_consolidated, width=1)

    clasificador.fit(X,y)
    return(clasificador)


#data_otra = pd.read_csv('data/dataset_otro.txt', sep='\t', encoding = "ISO-8859-1")
#data_otra = data_otra.loc[data_otra['rating.mode']!=4]
#clf = configurar_modelo(data_otra['content'].values.tolist(), data_otra['rating.mode'].values.tolist(), idioma = "ENGLISH")
#print(clf.predict(["I'm sick and tired of the decisions that the president is taking. No more!","cheers for the NYP and their amazing work!"]))


categoria = 'MATONEO'


data_propia = pd.read_csv('data/datos_polaridad.csv', sep=',', encoding = "ISO-8859-1")
data_propia = data_propia[['TEXTO',categoria]]
data_propia.columns = ['TEXTO','CATEGORIA']
data_propia.dropna(inplace = True)


if(categoria == 'MATONEO'):
    data_propia.loc[data_propia.CATEGORIA == 'n', 'CATEGORIA'] = 0
    data_propia.loc[data_propia.CATEGORIA == 'm', 'CATEGORIA'] = 1
    data_propia.loc[data_propia.CATEGORIA == 'a', 'CATEGORIA'] = 2
    data_propia.loc[data_propia.CATEGORIA == 'c', 'CATEGORIA'] = 3

print('Total Datos: ' + str(data_propia.shape[0]))
print(data_propia.CATEGORIA.value_counts())

clf = configurar_modelo(data_propia['TEXTO'].values.tolist(), data_propia['CATEGORIA'].values.tolist(), idioma = "SPANISH")


with open('clasificadores_entrenados/' + categoria + '_machine.pkl', 'wb') as output:
    pickle.dump(clf, output)
