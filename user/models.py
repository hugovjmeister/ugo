from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser

# Create your models here.
# Modelos para Mantenedor de Usuario
class Estado(models.Model):
    idEstado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    created_at = models.DateTimeField(default=datetime.now())
    update_at = models.DateTimeField(null=True)

    def __str__ (self):
        return self.nombre

class Rol(models.Model):
    idRol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    created_at = models.DateTimeField(default=datetime.now())
    update_at = models.DateTimeField(null=True)

    def __str__ (self):
        return self.nombre

class Usuario(AbstractUser):
    rut = models.IntegerField(verbose_name="Rut", default="1")
    nombres = models.CharField(max_length=250, verbose_name="Nombres", default="")
    apellido_paterno = models.CharField(max_length=100, verbose_name="Apellido Paterno", default="")
    apellido_materno = models.CharField(max_length=100, verbose_name="Apellido Materno", default="")
    telefono = models.IntegerField(verbose_name="Telefono", default="1")
    CHOICES = [('M','Masculino'),('F','Femenino')]
    sexo=models.CharField(verbose_name='Sexo', max_length=1, choices=CHOICES, default="M")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento", default="1950-01-01")
    estado = models.ForeignKey(Estado, null=True, on_delete=models.SET_NULL, blank=True)
    roles = models.ManyToManyField(Rol)
    created_at = models.DateTimeField(default=datetime.now(), null=True, blank=True)
    update_at = models.DateTimeField(null=True, blank=True)
