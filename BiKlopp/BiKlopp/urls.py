"""BiKlopp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from BiKlopp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('recomendar/', views.recomendar),
    path('popular-jugadores-mercado/', views.popularJugadoresMercado),
    path('popular-noticias/', views.popular_noticias),
    path('jugador/show/<int:player_id>/', views.mostrar_info_jugador),
    path('news/filter_by_player', views.news_filter_by_player),
    path('news/filter_by_team', views.news_filter_by_team),
    path('news/filter_by_player_and_team"', views.news_filter_by_player_and_team),
]
