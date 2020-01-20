import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import re
import os
from django.core.exceptions import ObjectDoesNotExist
from BiKlopp.models import Equipo, Jugador, Mercado
from django.conf import settings
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

def popular_jugadores_mercado(usuario, contrasena):
    path = os.getcwd()
    url = os.path.join(path, "BiKlopp/resources/chromedriver.exe").replace("\\","/")
   
    driver = webdriver.Chrome(url, options=options)

    driver.get('https://biwenger.as.com/login')
    driver.find_element_by_class_name('btn.squared.block.success').click()

    username = driver.find_element_by_name('email')
    username.send_keys(usuario)
    
    password = driver.find_element_by_name('password')
    password.send_keys(contrasena)

    driver.find_element_by_class_name('btn.squared.success').click()

    #Espera para completar el logeo y poder acceder al mercado
    time.sleep(2)

    driver.get('https://biwenger.as.com/market')

    #Espera para cargar el mercado y poder acceder a los jugadores
    time.sleep(2)
   
    mercado = Mercado.objects.create()
    i = 0
    jugadores = driver.find_elements_by_tag_name("player-card")
    urls = []
    for jugador in jugadores:
        urls.append(str(jugador.find_element_by_class_name("content").find_element_by_class_name("main").find_element_by_tag_name("h3").find_element_by_tag_name("a").get_attribute("href")))

    while i < 1:

        url = urls[i]

        driver.get(url)

        #Espera para cargar el jugador y poder extraer los datos
        time.sleep(2)

        page = BeautifulSoup(driver.page_source, "html5lib")
        
        nombre = page.find("h1",{"itemprop": "name"}).getText()
        foto = page.find("img",{"itemprop": "image"})["src"]
        forma_fisica = page.find('player-status')["title"]
        posicion = page.find('player-position').getText()
        puntos = []
        for punto in page.find("player-fitness").findAll(re.compile("^player-")):
            try:
                puntos.append(punto["title"])
            except:
                puntos.append(punto.getText())
        url_equipo = page.find('team-link').find("a")
        nombre_equipo = url_equipo["title"]
        foto_equipo = url_equipo.find("img")["src"]
        url_completa_equipo = "https://biwenger.as.com" + str(url_equipo["href"])
        driver.get(url_completa_equipo)
        #Espera para cargar el equipo y poder extraer los datos
        time.sleep(2)
        estadisticas = page.find("div",{"class": "stats"}).findAll("div", {"class": "row"})
        victorias_equipo = estadisticas[1].findAll("span")[0].getText()
        derrotas_equipo = estadisticas[1].findAll("span")[1].getText()

        try:
            equipo_bd = Equipo.objects.get(nombre=nombre)
            equipo_bd.update(nombre=nombre,foto=foto, posicion= posicion, forma=forma_fisica, ultimos_puntos=puntos, puntos_totales=puntos_totales, valor_mercado=valor, partidos_jugados=partidos_jugados, goles=goles, tarjetas=tarjetas, media_puntos=media_puntos, id_equipo=id_equipo, id_mi_equipo=id_mi_equipo, id_mercado=id_mercado)
            equipo_bd.save()
            equipo = equipo_bd
        except ObjectDoesNotExist:
            nuevo_Equipo = Equipo(nombre=nombre_equipo,foto=foto_equipo, victorias=victorias_equipo, derrotas=derrotas_equipo)
            nuevo_Equipo.save()
            equipo = nuevo_Equipo

        driver.get(url)

        #Espera para cargar el jugador y poder extraer los datos
        time.sleep(2) 
        estadisticas = page.find("div",{"class": "stats"}).findAll("div", {"class": "row"})
        puntos_totales = estadisticas[0].find("div", {"class": "stat main"}).find("span").getText()
        valor = estadisticas[2].find("div", {"class": "stat main"}).find("span", {"itemprop": "netWorth"}).getText()
        partidos_jugados =  estadisticas[4].find("div", {"class": "stat main"}).find("span").getText()
        goles = estadisticas[5].findAll("span")[0].getText()
        tarjetas = estadisticas[5].findAll("span")[1].getText()
        media_puntos =  estadisticas[6].find("div", {"class": "stat main"}).find("span").getText()
        

        try:
            jugador_bd = Jugador.objects.get(nombre=nombre)
            jugador_bd.update(nombre=nombre,foto=foto, posicion= posicion, forma=forma_fisica, ultimos_puntos=puntos, puntos_totales=puntos_totales, valor_mercado=valor, partidos_jugados=partidos_jugados, goles=goles, tarjetas=tarjetas, media_puntos=media_puntos, id_equipo=equipo, id_mercado=mercado)
            jugador_bd.save()
        except ObjectDoesNotExist:
            nuevo_jugador = Jugador(nombre=nombre,foto=foto, posicion= posicion, forma=forma_fisica, ultimos_puntos=puntos, puntos_totales=puntos_totales, valor_mercado=valor, partidos_jugados=partidos_jugados, goles=goles, tarjetas=tarjetas, media_puntos=media_puntos, id_equipo=equipo, id_mercado=mercado)
            nuevo_jugador.save()
           
        i = i + 1

    driver.quit()

