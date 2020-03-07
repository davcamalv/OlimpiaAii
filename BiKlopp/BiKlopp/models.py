from django.db import models
from django.core.validators import MinValueValidator

class Equipo(models.Model):
    id_equipo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    foto = models.URLField()
    victorias = models.PositiveIntegerField()
    derrotas = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ('nombre',)

class MiEquipo(models.Model):
    id_mi_equipo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    ultima_fecha_actualizacion = models.DateTimeField(auto_now=True) #Se actualiza automaticamente cada save()

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ('nombre',)

class Mercado(models.Model):
    id_mercado = models.AutoField(primary_key=True)
    ultima_fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id_mercado)

    class Meta:
        ordering = ('id_mercado',)

class Jugador(models.Model):
    id_jugador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    foto = models.URLField()
    POSICIONES = (('PT', 'Portero'), ('DF', 'Defensa'), ('MC', 'Mediocentro'), ('DL', 'Delantero'))
    posicion = models.CharField(choices=POSICIONES, max_length=50)
    forma = models.CharField(max_length=50)
    ultimos_puntos = models.TextField(max_length=200)
    puntos_totales = models.IntegerField()
    valor_mercado = models.IntegerField(validators=[MinValueValidator(150000)])
    partidos_jugados = models.PositiveIntegerField()
    goles = models.PositiveIntegerField()
    tarjetas = models.PositiveIntegerField()
    media_puntos = models.FloatField()
    id_equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, blank=True, null=True)
    id_mi_equipo = models.ForeignKey(MiEquipo, on_delete=models.CASCADE, blank=True, null=True)
    id_mercado = models.ForeignKey(Mercado, on_delete=models.CASCADE, blank=True, null=True)
    porcentaje_similitud_ideal = models.FloatField(blank=True, null=True)
    porcentaje_similitud_jugador = models.FloatField(blank=True, null=True)
    jugador_similiar = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    alineacion = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ('nombre',)





