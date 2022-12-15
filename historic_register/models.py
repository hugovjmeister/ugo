from django.db import models
from datetime import datetime
from user.models import Usuario
from user.models import Rol
from user.models import Estado

# Create your models here.
class Sede(models.Model):
    codigo = models.CharField(max_length=5, verbose_name="Código")
    nombre = models.CharField(max_length=250, verbose_name="Nombre")
    created_at = models.DateTimeField(default=datetime.now())
    update_at = models.DateTimeField(null=True)

    def __str__ (self):
        return self.nombre        

class EscuelaProgramaDepartamento(models.Model):
    codigo = models.CharField(max_length=5, verbose_name="Código")
    nombre = models.CharField(max_length=50, verbose_name="Nombre")

    def __str__ (self):
        return self.nombre  

class RegistroHistorico(models.Model):
    cod_unico_historico = models.CharField(max_length=250, verbose_name="Código Único", null=True)
    anio = models.IntegerField(verbose_name="Año", default="1900")
    periodo = models.CharField(max_length=50, verbose_name="Periodo")
    mes_fin = models.CharField(max_length=50, verbose_name="Mes Fin")
    sigla = models.CharField(max_length=50, verbose_name="Sigla")
    seccion = models.CharField(max_length=100, verbose_name="Sección")
    accion_formativa = models.CharField(max_length=250, verbose_name="Acción Formativa")
    estrategia_formativa = models.CharField(max_length=250, verbose_name="Estatregia Formativa")
    duracion_horas = models.IntegerField(verbose_name="Duración Horas", default="0")
    modalidad = models.CharField(max_length=100, verbose_name="Modalidad")
    escuela_programa_departamento = models.ForeignKey(EscuelaProgramaDepartamento, null=True, on_delete=models.SET_NULL, blank=True)
    cargo = models.CharField(max_length=100, verbose_name="Cargo")
    sede = models.ForeignKey(Sede, null=True, on_delete=models.SET_NULL, blank=True)
    usuario = models.ForeignKey(Usuario, null=True, on_delete=models.SET_NULL, blank=True)
    estado = models.CharField(max_length=100, verbose_name="Estado")
    observacion = models.CharField(max_length=250, verbose_name="Observación")
    trayectoria = models.CharField(max_length=250, verbose_name="Trayectoria")
    ruta = models.CharField(max_length=250, verbose_name="Ruta")
    mencion = models.CharField(max_length=250, verbose_name="Mención")
    a_cargo = models.CharField(max_length=250, verbose_name="A Cargo")
    proveedor = models.CharField(max_length=250, verbose_name="Proveedor")
    created_at = models.DateTimeField(default=datetime.now())
    update_at = models.DateTimeField(null=True)