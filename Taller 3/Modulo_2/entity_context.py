from SPARQLWrapper import SPARQLWrapper, JSON



supported_entities = ['person', 'populated place','movie']


def dar_tipo_entidad(search_word):

    #First the entities
    ent = [ '"' + entity + '"@en' for entity in supported_entities]

    ent_string = " ".join(ent)


    #Convert to title
    search_word = search_word.title()

    query = '''
    select ?thing_name ?label
    where {

      ?thing foaf:name "'''

    query += search_word
    query+= '''"@en.
      ?thing foaf:name ?thing_name.

      ?thing a ?entity_type.

      ?entity_type rdfs:label ?label.
      VALUES ?label {'''
    query += ent_string


    query +=  '''}.
    }
    LIMIT 10
    '''

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    entity = None
    for result in results["results"]["bindings"]:
        return result["label"]["value"]


def get_entity_data(entity):
    #TODO
    #MOCK
    dic = ['name':'Tom Cruise', "Gender":'Male']
    return(dic)


while True:
    print('Write entity name')
    print(dar_tipo_entidad(input()))
