import spacy
nlp = spacy.load('en_core_web_sm')
# Hay 3 modelos en ingles, la diferencia es el tamano con el que se entrena cada uno
# sm, md, lg

def dar_entidades(texto_pregunta):
    # Puede recibir el texto de la pregunta o el ID de esta
    # Pero debe devolver un arreglo con las entidades

    response = []

    doc = nlp(texto_pregunta)

    for ent in doc.ents:
        response.append(ent.text)

    return(response)
