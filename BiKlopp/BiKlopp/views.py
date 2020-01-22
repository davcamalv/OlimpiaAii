from BiKlopp.populate import popular_jugadores_mercado, populate_news, popular_jugadores_mi_equipo, login
from BiKlopp.models import Equipo, Jugador, Mercado
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from BiKlopp.news import filter_by_player_and_team, filter_by_team, filter_by_player
from datetime import date,timedelta
from scipy.stats.stats import pearsonr
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
    populate_news(jugador.nombre, jugador.id_equipo.nombre)
    noticias_player = filter_by_player(jugador.nombre)
    noticias_team = filter_by_team(jugador.id_equipo.nombre)
    noticias_player_and_team = filter_by_player_and_team(jugador.nombre, jugador.id_equipo.nombre)
    return render(request, "mostrar_jugador.html", {"jugador": jugador, "noticias_player":noticias_player, "noticias_team":noticias_team, "noticias_player_and_team":noticias_player_and_team})


def actualizar_recomendacion_plantilla():
    jugadores_alineacion = Jugador.objects.all().filter(alineacion=True)
    jugadores_mercado = Jugador.objects.all().filter(alineacion=False)
    print(jugadores_alineacion.count())
    print(jugadores_mercado.count())
    for jugador_mercado in jugadores_mercado:
        jugador = jugador_to_list(jugador_mercado)
        recomendados = []
        for jugador_alineacion in jugadores_alineacion:
            if jugador_alineacion.posicion == jugador_mercado.posicion:
                similitud = pearsonr(jugador, jugador_to_list(jugador_alineacion))[0]
                recomendados.append((jugador_alineacion.id_jugador, similitud))
        print(recomendados)
        mejor_similitud = max(recomendados, key= lambda pos: pos[1])
        jugador_mercado.jugador_similiar = get_object_or_404(Jugador, pk=mejor_similitud[0])
        jugador_mercado.porcentaje_similitud_jugador = mejor_similitud[1]
        jugador_mercado.save()
        print(jugador_mercado.juga)




def jugador_to_list(jugador_objeto):
    jugador = []
    puntos = []
    for puntito in jugador_objeto.ultimos_puntos.replace("[", "").replace("]", "").replace("'", "").split(","):
        try:
            puntos.append(int(puntito))
        except:
            puntos.append(0)
    jugador.extend(puntos)
    jugador.append(jugador_objeto.puntos_totales)
    jugador.append(jugador_objeto.valor_mercado)
    jugador.append(jugador_objeto.partidos_jugados)
    jugador.append(jugador_objeto.goles)
    jugador.append(jugador_objeto.media_puntos)
    return jugador