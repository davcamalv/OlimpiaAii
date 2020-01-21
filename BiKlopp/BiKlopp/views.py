from BiKlopp.populate import popular_jugadores_mercado, populate_noticias
from BiKlopp.models import Equipo, Jugador, Mercado, MiEquipo
from django.http import HttpResponse

def popularJugadoresMercado(request):
    popular_jugadores_mercado("dcamalv@gmail.com", "contraseña") 

def popular_noticias(request):
    return HttpResponse(populate_noticias())
