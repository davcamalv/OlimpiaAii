from BiKlopp.populate import popular_jugadores_mercado, populate_news, popular_jugadores_mi_equipo
from BiKlopp.models import Jugador, Mercado
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from BiKlopp.news import filter_by_player_and_team, filter_by_team, filter_by_player
from datetime import datetime,timedelta
import pytz

def index(request):
    return render(request, "index.html")

def recomendar(request):
    correo = request.POST['correo']
    contrasenya = request.POST['contrasenya']
    actualizar_info = request.POST.get('actualizar_info', False)
    if actualizar_info:

        popular_jugadores_mercado(correo, contrasenya)
        popular_jugadores_mi_equipo(correo, contrasenya)

    elif len(Mercado.objects.all()) == 0:

        popular_jugadores_mercado(correo, contrasenya)
    else:

        mercado = Mercado.objects.all()[0]
        utc=pytz.UTC
        if mercado.ultima_fecha_actualizacion < utc.localize((datetime.now() - timedelta(days=1))):
            popular_jugadores_mercado(correo, contrasenya)
        

    #TODO algoritmo_recomendacion()
    jugadores = Jugador.objects.all() #Provisional: Se sustituyen por los jugadores recomendados
    #Todo solucionar lo de las URL
    return render(request, "recomendados.html", {"jugadores": jugadores})

def mostrar_info_jugador(request, player_id):
    jugador = get_object_or_404(Jugador, pk=player_id)
    populate_news(jugador.nombre, jugador.id_equipo.nombre)
    noticias_player = filter_by_player(jugador.nombre)
    noticias_team = filter_by_team(jugador.id_equipo.nombre)
    noticias_player_and_team = filter_by_player_and_team(jugador.nombre, jugador.id_equipo.nombre)
    return render(request, "mostrar_jugador.html", {"jugador": jugador, "noticias_player":noticias_player, "noticias_team":noticias_team, "noticias_player_and_team":noticias_player_and_team})
