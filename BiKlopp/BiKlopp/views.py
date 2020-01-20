from BiKlopp.populate import popular_jugadores_mercado
from BiKlopp.models import Equipo, Jugador, Mercado, MiEquipo

def popularJugadoresMercado(request):
    popular_jugadores_mercado("dcamalv@gmail.com", "contraseña") 
