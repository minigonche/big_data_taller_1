

def dar_contexto(entidad):


    # TODO: Felipe

    if(entidad == 'Bradley Cooper'):

        html = '''
          <h4> Entity Context </h4>

          <p>  (Contexto de la persona o lugar) </p>

          <p> <strong> Edad: </strong>  38 </p>
          <p> <strong> Sexo: </strong>  Masculino </p>
          <p> <strong> Profesion: </strong>  Actor </p>

          <img class="d-block mx-auto mb-4" src="{% static "app3/img/bradley-cooper-pro.jpg" %}" width="80%" alt="" >

                  '''
    else:
        html = '''<h4> No Info Found </h4>

                    <p> No context information was found for ENTIDAD </p>

                '''
        html = html.replace('ENTIDAD', entidad)

    return(html)
