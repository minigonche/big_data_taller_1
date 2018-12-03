from django.shortcuts import render
from django.template import Template, Context
from django.http import HttpResponse
from app3.Requerimientos.VistaEnriquecida import DarContexto as DC
from app3.Requerimientos.VistaEnriquecida import DarRealidad as DR
from app3.Requerimientos.VistaEnriquecida import DetectorEntidades as DE
import re

id_contexto = 'context_ENTIDAD'
id_realidad = 'reality_ENTIDAD'


def hacer_requerimiento(request, db):

    # TODO

    #Extrae el template
    fp = open('app3/Templates/app3/VistaEnriquecida.html')
    t = fp.read()
    fp.close()

    # PREGUNTA

    #Extrae el id de la pregunta (ya sea porque le entra por parametro o lo
    # extrae del request)
    id = '12344' #MOCK

    #Extrae el texto de la pregunta
    question_text = dar_texto_pregunta(id)

    #Extrae las entidades
    entidades = DE.dar_entidades(question_text)

    #Rendeiza la pregunta
    question_text = renderizar_texto(question_text,entidades)

    t = t.replace('TEXTO_DE_LA_PREGUNTA', question_text)

    realidad_html = ''
    contexto_html = ''
    mostrar_js = ''
    #quitar_js = ''

    for entidad in entidades:

        realidad = DR.dar_realidad(entidad)
        realidad_html += encapsular_realidad( realidad , entidad ) +'\n'

        contexto = DC.dar_contexto(entidad)
        contexto_html += encapsular_contexto(contexto, entidad) + '\n'

        mostrar_js += dar_js_mostrar(entidad) + '\n'

        #quitar_js += dar_js_quitar(entidad) + '\n'


    #REALIDAD
    t = t.replace('REALIDAD_ENTIDADES', realidad_html)

    #CONTEXTO
    t = t.replace('CONTEXTO_ENTIDADES', contexto_html)

    #JS
    t = t.replace('MOSTRAR_ENTIDADES', mostrar_js)
    #t = t.replace('QUITAR_ENTIDADES', quitar_js)



    return HttpResponse(Template(t).render(Context({})))


def dar_texto_pregunta(id):

    #TODO
    #MOCK
    text = 'What is the meaning behind this scene in American Sniper where the nurses ignore Bradley Cooper and his crying baby in New York City?'
    #text = 'A question about Christian Bale in Batman. The premier will be in Houston'

    return(text)


def renderizar_texto(texto, entidades):

    template = '<span onmouseover="hover_in(\'ENTIDAD\')" onmouseout="hover_out(\'ENTIDAD\')" onclick="toggle(\'ENTIDAD\')"> <mark> ENTIDAD </mark> </span>'

    for ent in entidades:
        n_template = template.replace('ENTIDAD', ent)
        print(n_template)
        texto = texto.replace(ent, n_template)

    return(texto)

def dar_idenificador_entidad(entidad):
    """ Devueñve un identificador compatible con HTML"""


    regex = re.compile('[^a-zA-Z ]')
    clean = regex.sub('', entidad)

    if(clean == ''):
        return('unkown')

    clean = clean.lower()
    clean = clean.replace(' ','_')
    return(clean)

def encapsular_contexto(contexto, entidad):

    template =   '<div  id="' + id_contexto + '" class="small right" style="display: none;">'

    entidad_id = dar_idenificador_entidad(entidad)

    id_final = id_contexto.replace('ENTIDAD',entidad_id)

    template = template.replace(id_contexto, id_final)

    encapsulado = template + contexto + '</div>'

    return(encapsulado)


def encapsular_realidad(realidad, entidad):

    template =   '<div  id="' + id_realidad + '" class="small left" style="display: none;">'

    entidad_id = dar_idenificador_entidad(entidad)

    id_final = id_realidad.replace('ENTIDAD',entidad_id)

    template = template.replace(id_realidad, id_final)

    encapsulado = template + realidad + '</div>'

    return(encapsulado)

def dar_js_mostrar(entidad):

    #SEGUIR ACA

    template = '''

            if(entity == "ENTIDAD")
            {
              document.getElementById('REALITY_ID').style.display = 'block';
              document.getElementById('CONTEXT_ID').style.display = 'block';
            }

    '''
    entidad_id = dar_idenificador_entidad(entidad)


    reality_id = id_realidad.replace('ENTIDAD',entidad_id)
    context_id = id_contexto.replace('ENTIDAD',entidad_id)


    template = template.replace('ENTIDAD',entidad )
    template = template.replace('REALITY_ID',reality_id )
    template = template.replace('CONTEXT_ID',context_id )

    return(template)

def dar_js_quitar(entidad):

    #SEGUIR ACA

    template = '''

            if(entity == "ENTIDAD")
            {
              document.getElementById('REALITY_ID').style.display = 'none';
              document.getElementById('CONTEXT_ID').style.display = 'none';
            }

    '''
    entidad_id = dar_idenificador_entidad(entidad)


    reality_id = id_realidad.replace('ENTIDAD',entidad_id)
    context_id = id_contexto.replace('ENTIDAD',entidad_id)


    template = template.replace('ENTIDAD',entidad )
    template = template.replace('REALITY_ID',reality_id )
    template = template.replace('CONTEXT_ID',context_id )

    return(template)
