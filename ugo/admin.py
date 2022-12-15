from django.contrib import admin
from .models import *
from user.models import *
from historic_register.models import *

# Register your models here.
# Mantenedor de Usuario
admin.site.register(Estado)
admin.site.register(Rol)
admin.site.register(Usuario)

# Registro Histórico
admin.site.register(EscuelaProgramaDepartamento)
admin.site.register(RegistroHistorico)
admin.site.register(Sede)
