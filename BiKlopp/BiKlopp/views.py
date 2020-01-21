from BiKlopp.populate import popular_jugadores_mercado, populate_news
from BiKlopp.models import Equipo, Jugador, Mercado, MiEquipo
from django.http import HttpResponse
from BiKlopp.news import filter_by_player_and_team, filter_by_team, filter_by_player_or_team

def popularJugadoresMercado(request):
    popular_jugadores_mercado("dcamalv@gmail.com", "contraseña") 

def popular_noticias(request):
    populate_news()

