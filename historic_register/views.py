from django.shortcuts import render
from .models import *
from django.views.generic.list import ListView
from django.views.generic import View
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
import pandas as pd

# Create your views here.
class ListRegistroHistorico(ListView):
    model = RegistroHistorico
    template_name = 'registro_historico/index.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super(ListRegistroHistorico, self).dispatch(request, *args, **kwargs)
        return redirect('login')

def upload_historico(request):
    if request.method == 'POST':
        df = pd.read_excel(request.FILES['xlsHistorico'])
        data = pd.DataFrame(df, columns= ['Reg_Valido', 'AÑO', 'PERIODO', 'Mes Fin', 'SIGLA', 'Sección', 'ACCIÓN FORMATIVA', 'ESTRATEGIA_FORMATIVA',
            'Duración Horas', 'Modalidad', 'Escuela/Programa (docente)', 'Cargo', 'Sede (docente)', 'Usuario', 'Rut', 'Apellidos', 'Nombre', 'Correo',
            'Estado', 'OBSE', 'Trayectoria', 'RUTA', 'MENCIÓN', 'A CARGO DE', 'PROVEEDOR'])

        data['Duración Horas'] = data['Duración Horas'].fillna(0)

        RegistroHistorico.objects.all().delete()

        for historico in range(len(data)):
            if data.iloc[historico, 0] != 'NO':
                anio = data.iloc[historico, 1]
                if pd.isna(data.iloc[historico, 2]):
                    periodo = ''
                else:
                    periodo = data.iloc[historico, 2]
                
                if pd.isna(data.iloc[historico, 3]):
                    mes_fin = ''
                else:
                    mes_fin = data.iloc[historico, 3]
                
                if pd.isna(data.iloc[historico, 4]):
                    sigla = ''
                else:
                    sigla = data.iloc[historico, 4]
                
                if pd.isna(data.iloc[historico, 5]):
                    seccion = ''
                else:
                    seccion = data.iloc[historico, 5]
                
                if pd.isna(data.iloc[historico, 6]):
                    accion_formativa = ''
                else:
                    accion_formativa = data.iloc[historico, 6]
                
                if pd.isna(data.iloc[historico, 7]):
                    estrategia_formativa = ''
                else:
                    estrategia_formativa = data.iloc[historico, 7]
                
                if pd.isna(data.iloc[historico, 8]):
                    duracion_horas = 0
                else:
                    duracion_horas = data.iloc[historico, 8]
                modalidad = data.iloc[historico, 9]

                try:
                    escuela_programa_departamento = EscuelaProgramaDepartamento.objects.get(codigo = data.iloc[historico, 10])
                except EscuelaProgramaDepartamento.DoesNotExist:
                    messages.error(request, "Columna 'Escuela/Programa (docente)' no existe en Fila: " + str(historico+2))
                    return render(request, 'registro_historico/index.html')

                if pd.isna(data.iloc[historico, 11]):
                    cargo = ''
                else:
                    cargo = data.iloc[historico, 11]
                
                try:
                    sede = Sede.objects.get(codigo = data.iloc[historico, 12])
                except Sede.DoesNotExist:
                    messages.error(request, "Columna 'Sede (docente)' no existe en Fila: " + str(historico+2))
                    return render(request, 'registro_historico/index.html')

                rut_usuario = str(data.iloc[historico, 14])
                rut_usuario = rut_usuario[:-1]
                rut_usuario = int('0' + rut_usuario)
                usuario = Usuario.objects.filter(rut=rut_usuario).first()
                if not usuario:
                    estado_usuario = Estado.objects.get(idEstado = 1)
                    value_user = Usuario(
                        is_superuser = 1,
                        username = data.iloc[historico, 13],
                        first_name = "",
                        last_name = "",
                        is_staff = 1,
                        is_active = 1,
                        date_joined = datetime.now(),
                        rut = rut_usuario,
                        nombres = data.iloc[historico, 16],
                        apellido_paterno = data.iloc[historico, 15],
                        apellido_materno = ' ',
                        email = data.iloc[historico, 17],
                        telefono = 0,
                        sexo = 'M',
                        fecha_nacimiento = '1950-01-01',
                        created_at = datetime.now(),
                        update_at = datetime.now(),
                        estado = estado_usuario
                    )
                    value_user.save()

                usuario = Usuario.objects.filter(rut=rut_usuario).first()
                if pd.isna(data.iloc[historico, 18]):
                    estado = ''
                else:
                    estado = data.iloc[historico, 18]
                
                if pd.isna(data.iloc[historico, 19]):
                    observacion = ''
                else:
                    observacion = data.iloc[historico, 19]
                
                if pd.isna(data.iloc[historico, 20]):
                    trayectoria = ''
                else:
                    trayectoria = data.iloc[historico, 20]
                
                if pd.isna(data.iloc[historico, 21]):
                    ruta = ''
                else:
                    ruta = data.iloc[historico, 21]
                
                if pd.isna(data.iloc[historico, 22]):
                    mencion = ''
                else:
                    mencion = data.iloc[historico, 22]
                
                if pd.isna(data.iloc[historico, 23]):
                    a_cargo = ''
                else:
                    a_cargo = data.iloc[historico, 23]
                
                if pd.isna(data.iloc[historico, 24]):
                    proveedor = ''
                else:
                    proveedor = data.iloc[historico, 24]
                

                value = RegistroHistorico(
                    anio = anio,
                    periodo = periodo,
                    mes_fin = mes_fin,
                    sigla = sigla,
                    seccion = seccion,
                    accion_formativa = accion_formativa,
                    estrategia_formativa = estrategia_formativa,
                    duracion_horas = duracion_horas,
                    modalidad = modalidad,
                    escuela_programa_departamento = escuela_programa_departamento,
                    cargo = cargo,
                    sede = sede,
                    usuario = usuario,
                    estado = estado,
                    observacion = observacion,
                    trayectoria = trayectoria,
                    ruta = ruta,
                    mencion = mencion,
                    a_cargo = a_cargo,
                    proveedor = proveedor,
                    created_at = datetime.now(),
                    update_at = datetime.now()
                )
                value.save()
  
        return redirect('historico')  

def delete_historico(request, id):
    registro_historico = RegistroHistorico.objects.get(id = id)
    registro_historico.delete()
    return redirect('historico')