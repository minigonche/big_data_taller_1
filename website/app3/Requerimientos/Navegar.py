# Clase que navega las distintas preguntas en la base de datos

from django.shortcuts import render
import pymongo
import numpy as np
import pandas as pd
import re
import re


def hacer_requerimiento(request, db):

    #Muestra una lista de preguntas

    colection = db.Questions
    list = colection.aggregate([{"$sample": {"size": 15}} ])

    question_list = []
    for q in list:
        q = clean_question(q)
        question_list.append(q)

    data = {}
    data['questions'] = question_list

    return render(request, 'app3/Navegar.html', data)


def clean_question(q):
    q['title'] = q['title'].replace('&#39;',"'")
    q['title'] = q['title'].replace('&quot;','"')
    body = q['body']
    body = re.sub("<a [^']+>", '', body)
    body = body.replace('</a>','')
    body = body.replace('<em>','')
    body = body.replace('</em>','')
    body = body.replace('<strong>','')
    body = body.replace('</strong>','')
    q['body'] = body

    return(q)
