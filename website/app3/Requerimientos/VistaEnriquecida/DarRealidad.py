

def dar_realidad(entidad):


    # TODO: Andrea

    if(entidad == 'Bradley Cooper'):

        html = '''
            <h4> Entity Reality </h4>

            <p> (Una descripcion lebe de lo que se esta diciendo de la entidad. El contenido es scrollable asi que tenemos todo el espacio que queramos)</p>

            <img class="d-block mx-auto mb-4" src="{% static "app3/img/bradley-cooper.jpg" %}" width="80%"  alt="" >

            <p> Comentario 1 de Twitter </p>
            <p> Comentario 2 de Twitter </p>
            <p> Comentario 3 de Twitter </p>

                  '''
    else:
        html = '''<h4> No Info Found </h4>

                    <p> No reality information was found for ENTIDAD </p>

                '''
        html = html.replace('ENTIDAD', entidad)

    return(html)
