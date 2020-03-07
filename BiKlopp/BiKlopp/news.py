from whoosh.index import open_dir
from whoosh.query import And, Term, Or

def filter_by_player_and_team(jugador, equipo):
    ix=open_dir("Index_news")
    with ix.searcher() as buscador_noticias:
        list_aux_jugador = []
        list_aux_equipo = []
        for nom_divididio in equipo.split():
            list_aux_equipo.append(Or([Term("titulo", str(nom_divididio).lower()), Term("desc", str(nom_divididio).lower())]))
        qe = And(list_aux_equipo)

        for nom_divididio in jugador.split():
            list_aux_jugador.append(Or([Term("titulo", str(nom_divididio).lower()), Term("desc", str(nom_divididio).lower())]))
        qj = And(list_aux_jugador)

        q = And([qe, qj])
        results_whoosh = buscador_noticias.search(q, limit=None)
        results = []
        for result_whoosh in results_whoosh:
            results.append(result_whoosh.fields())
        return results

def filter_by_team(equipo):
    ix=open_dir("Index_news")
    res = {}
    with ix.searcher() as buscador_noticias:
        list_aux = []
        for nom_divididio in equipo.split():
            list_aux.append(Or([Term("titulo", str(nom_divididio).lower()), Term("desc", str(nom_divididio).lower())]))
        q = And(list_aux)
        results_whoosh = buscador_noticias.search(q, limit=None)
        results = []
        for result_whoosh in results_whoosh:
            results.append(result_whoosh.fields())
        return results

def filter_by_player(jugador):
    ix=open_dir("Index_news")
    print(jugador)
    with ix.searcher() as buscador_noticias:
        list_aux = []
        for nom_divididio in jugador.split():
            list_aux.append(Or([Term("titulo", str(nom_divididio).lower()), Term("desc", str(nom_divididio).lower())]))
        q = And(list_aux)
        results_whoosh = buscador_noticias.search(q, limit=None)
        results = []
        for result_whoosh in results_whoosh:
            results.append(result_whoosh.fields())
        return results

