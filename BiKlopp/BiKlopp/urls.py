from django.contrib import admin
from django.urls import path
from BiKlopp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('recomendar/', views.recomendar),
    path('jugador/show/<int:player_id>/', views.mostrar_info_jugador),
]
