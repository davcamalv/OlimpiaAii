from BiKlopp.populate import popular_jugadores_mercado, populate_news, popular_jugadores_mi_equipo, login
from BiKlopp.models import Equipo, Jugador, Mercado
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from BiKlopp.news import filter_by_player_and_team, filter_by_team, filter_by_player
from datetime import datetime, date, time, timedelta
import calendar
import pytz

def index(request):
    return render(request, "index.html")

def recomendar(request):
    correo = request.POST['correo']
    contrasenya = request.POST['contrasenya']
    actualizar_info = request.POST.get('actualizar_info', False)
    if actualizar_info:
        try:
            driver = login(correo, contrasenya)
        except:
            return render(request, "index.html", {"error": "El usuario o la contraseña no son correctos"})
        popular_jugadores_mercado(driver)
        popular_jugadores_mi_equipo(driver)

    elif len(Mercado.objects.all()) == 0:
        try:
            driver = login(correo, contrasenya)
        except:
            return render(request, "index.html", {"error": "El usuario o la contraseña no son correctos"})
        popular_jugadores_mercado(driver)
    else:

        mercado = Mercado.objects.all()[0]
        utc=pytz.UTC
        if mercado.ultima_fecha_actualizacion < utc.localize((datetime.now() - timedelta(days=1))):
            try:
                driver = login(correo, contrasenya)
            except:
                return render(request, "index.html", {"error": "El usuario o la contraseña no son correctos"})
            popular_jugadores_mercado(driver)
        

    #TODO algoritmo_recomendacion()
    jugadores = Jugador.objects.all() #Provisional: Se sustituyen por los jugadores recomendados
    #Todo solucionar lo de las URL
    return render(request, "recomendados.html", {"jugadores": jugadores})

def mostrar_info_jugador(request, player_id):
    jugador = get_object_or_404(Jugador, pk=player_id)
    populate_news()
    noticias = filter_by_team()
    for n in noticias:
        print(n)
    return render(request, "mostrar_jugador.html", {"jugador": jugador, "noticias":noticias})

def news_filter_by_team(request, player_id):
    jugador = get_object_or_404(Jugador, pk=player_id)
    noticias = filter_by_team()
    return render(request, "mostrar_jugador.html", {"jugador": jugador, "noticias": noticias})

def news_filter_by_player(request, player_id):
    jugador = get_object_or_404(Jugador, pk=player_id)
    noticias = filter_by_player()
    return render(request, "mostrar_jugador.html", {"jugador": jugador, "noticias": noticias})

def news_filter_by_player_and_team(request, player_id):
    jugador = get_object_or_404(Jugador, pk=player_id)
    noticias = filter_by_player_and_team()
    return render(request, "mostrar_jugador.html", {"jugador": jugador, "noticias": noticias})