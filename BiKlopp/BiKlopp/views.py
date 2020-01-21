from BiKlopp.populate import popular_jugadores_mercado
from BiKlopp.models import Equipo, Jugador, Mercado
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404

def popularJugadoresMercado(request):
    popular_jugadores_mercado("dcamalv@gmail.com", "contraseña")
    return HttpResponseRedirect('/admin/')

def index(request):
    return render(request, "index.html")

def recomendar(request):
    correo = request.POST['correo']
    contrasenya = request.POST['contrasenya']
    #actualizar_info = request.POST['actualizar_info']
    #TODO popular_jugadores_mercado(correo, contrasenya, actualizar_info)
    #popular_jugadores_mercado(correo, contrasenya)
    #TODO popular_jugadores_mi_equipo(correo, contrasenya)
    #TODO algoritmo_recomendacion()
    jugadores = Jugador.objects.all() #Provisional: Se sustituyen por los jugadores recomendados
    #Todo solucionar lo de las URL
    return render(request, "recomendados.html", {"jugadores": jugadores})

def mostrar_info_jugador(request, player_id):
    jugador = get_object_or_404(Jugador, pk=player_id)
    return render(request, "mostrar_jugador.html", {"jugador": jugador})