from whoosh.index import create_in,open_dir
from whoosh.reading import IndexReader
from whoosh.fields import Schema, TEXT, DATETIME
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh import query
from whoosh.query import And, Term, Or
import os


def filter_by_player_and_team():
    ix=open_dir("Index_news")
    jugador = "joaquín"
    equipo = "betis"
    with ix.searcher() as buscador_noticias:
        q = And([Or([Term("titulo", str(equipo)), Term("desc", str(equipo))]), Or([Term("titulo", str(jugador)), Term("desc", str(jugador))])])
        results = buscador_noticias.search(q, limit=None)
        return results

def filter_by_team():
    ix=open_dir("Index_news")
    equipo = "betis"
    with ix.searcher() as buscador_noticias:
        q = Or([Term("titulo", str(equipo)), Term("desc", str(equipo))])
        results = buscador_noticias.search(q, limit=None)
        return results

def filter_by_player_or_team():
    ix=open_dir("Index_news")
    jugador = "joaquín"
    equipo = "betis"
    with ix.searcher() as buscador_noticias:
        q = Or([Or([Term("titulo", str(equipo)), Term("desc", str(equipo))]), Or([Term("titulo", str(jugador)), Term("desc", str(jugador))])])
        results = buscador_noticias.search(q, limit=None)
        for res in results:
            print(res)
        return results

