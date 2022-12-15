from django.shortcuts import render
from .models import *
from historic_register.models import *
from django.views.generic import View
from django.urls import reverse_lazy
from django.shortcuts import redirect
import pandas as pd
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count
from io import BytesIO
import xlsxwriter
from django.http import HttpResponse

# Create your views here.
class ReportRatings(View):
    def get(self, request, *args, **kwargs):
        Periodos = RegistroHistorico.objects.raw('select distinct 1 as id, anio, periodo from historic_register_registrohistorico')
        cmbPeriodo = []
        for item in Periodos:
            periodo_info = {}
            periodo_info['periodo'] = str(item.anio) + "-" + item.periodo
            cmbPeriodo.append(periodo_info)

        Sedes = Sede.objects.all()
        Escuelas = EscuelaProgramaDepartamento.objects.all()
        return render(request, 'reports/report_ratings.html', {"Periodo": cmbPeriodo, "Sede": Sedes, "Escuela": Escuelas})

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super(ReportRatings, self).dispatch(request, *args, **kwargs)
        return redirect('login')   

def get_data_ratings(request, *args, **kwargs):
    cmbPeriodo = request.GET.get("cmbPeriodo", None)
    cmbSede = request.GET.get("cmbSede", None)
    cmbEscuelaPrograma = request.GET.get("cmbEscuelaPrograma", None)
    anio = cmbPeriodo.split("-")[0]
    periodo = cmbPeriodo.split("-")[1]

    idSede = 0
    if cmbSede != "0":
        objSede = Sede.objects.get(codigo = cmbSede)
        idSede = objSede.id

    idEscuela = 0
    if cmbEscuelaPrograma != "0":
        objEscuela = EscuelaProgramaDepartamento.objects.get(codigo = cmbEscuelaPrograma)
        idEscuela = objEscuela.id

    registro_historico = RegistroHistorico.objects.raw('''SELECT s.id, s.nombre, (select count(*) from historic_register_registrohistorico where Sede_id = s.id and Anio = %s and Periodo = %s and Estado like '%%APROBADO%%' and (0=%s or escuela_programa_departamento_id = %s)) as aprobado, (select count(*) from historic_register_registrohistorico where Sede_id = s.id and Anio = %s and Periodo = %s and Estado like '%%REPROBADO%%' and (0=%s or escuela_programa_departamento_id = %s)) as reprobado from historic_register_sede s where (0=%s or s.id = %s)  group by s.id, s.nombre''', [anio, periodo, idEscuela, idEscuela, anio, periodo, idEscuela, idEscuela, idSede, idSede])
    registro_pie = RegistroHistorico.objects.raw('''select distinct 1 id, round((((select count(*) from historic_register_registrohistorico where estado like '%%APROBADO%%' and anio = %s and periodo = %s and (0=%s or sede_id=%s) and (0=%s or escuela_programa_departamento_id = %s))*100)/(select count(*) from historic_register_registrohistorico where (estado like '%%APROBADO%%' or estado like '%%REPROBADO%%') and anio = %s and periodo = %s and (0=%s or sede_id=%s) and (0=%s or escuela_programa_departamento_id = %s) )),0) aprobado, round((((select count(*) from historic_register_registrohistorico where estado like '%%REPROBADO%%' and anio = %s and periodo = %s and (0=%s or sede_id=%s) and (0=%s or escuela_programa_departamento_id = %s) )*100)/(select count(*) from historic_register_registrohistorico where (estado like '%%APROBADO%%' or estado like '%%REPROBADO%%') and anio = %s and periodo = %s and (0=%s or sede_id=%s) and (0=%s or escuela_programa_departamento_id = %s) )),0) reprobado from historic_register_registrohistorico''', [anio, periodo, idSede, idSede, idEscuela, idEscuela, anio, periodo, idSede, idSede, idEscuela, idEscuela, anio, periodo, idSede, idSede, idEscuela, idEscuela, anio, periodo, idSede, idSede, idEscuela, idEscuela])
    sedes = []
    datosA = []
    datosR = []
    datosPie = []
    
    for item in registro_historico:
        sedes.append(item.nombre)
        datosA.append(item.aprobado)
        datosR.append(item.reprobado)

    for item in registro_pie:
        datosPie.append(item.aprobado)
        datosPie.append(item.reprobado)

    #Totalizadores
    participaciones = RegistroHistorico.objects.raw('''select 1 id, count(*) participaciones from historic_register_registrohistorico where anio = %s and periodo = %s and (0=%s or sede_id=%s) and (0=%s or escuela_programa_departamento_id = %s)''', [anio, periodo, idSede, idSede, idEscuela, idEscuela])
    for item in participaciones:
        participaciones = item.participaciones

    docentes = RegistroHistorico.objects.raw('''select 1 id, count(*) docentes from historic_register_registrohistorico where cargo like '%%Docente%%' and anio = %s and periodo = %s and (0=%s or sede_id=%s) and (0=%s or escuela_programa_departamento_id = %s)''', [anio, periodo, idSede, idSede, idEscuela, idEscuela])
    for item in docentes:
        docentes = item.docentes

    horas = RegistroHistorico.objects.raw('''select 1 id, sum(duracion_horas) horas from historic_register_registrohistorico where anio = %s and periodo = %s and (0=%s or sede_id=%s) and (0=%s or escuela_programa_departamento_id = %s)''', [anio, periodo, idSede, idSede, idEscuela, idEscuela])
    for item in horas:
        horas = item.horas

    data = {
        "labels": sedes,
        "datosA": datosA,
        "datosR": datosR,
        "datosPie": datosPie,
        "participaciones": participaciones,
        "docentes": docentes,
        "horas": horas
    }
    return JsonResponse(data)

def export_data(request, periodo, sede, escuela):
    output = BytesIO()
    # Feed a buffer to workbook
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet("data")

    # Get Data
    cmbPeriodo = periodo
    cmbSede = sede
    cmbEscuelaPrograma = escuela
    anio = cmbPeriodo.split("-")[0]
    periodo = cmbPeriodo.split("-")[1]

    idSede = 0
    if cmbSede != 0:
        objSede = Sede.objects.get(codigo = cmbSede)
        idSede = objSede.id

    idEscuela = 0
    if cmbEscuelaPrograma != 0:
        objEscuela = EscuelaProgramaDepartamento.objects.get(codigo = cmbEscuelaPrograma)
        idEscuela = objEscuela.id

    data = RegistroHistorico.objects.raw('''select r.id, e.codigo, s.codigo, r.anio, r.periodo, r.mes_fin, r.sigla, r.seccion, r.accion_formativa, r.estrategia_formativa, r.duracion_horas, r.modalidad, r.cargo, u.username, u.rut, u.apellido_paterno, u.nombres, u.email, r.estado, r.observacion, r.trayectoria, r.ruta, r.mencion, r.a_cargo, r.proveedor
        from historic_register_registrohistorico r 
        inner join historic_register_escuelaprogramadepartamento e on r.escuela_programa_departamento_id = e.id 
        inner join historic_register_sede s on r.sede_id = s.id
        inner join user_usuario u on r.usuario_id = u.id
        where r.anio = %s and r.periodo = %s and (0=%s or r.sede_id=%s) and (0=%s or r.escuela_programa_departamento_id=%s)''', [anio, periodo, idSede, idSede, idEscuela, idEscuela])
    # End Get Data

    columns = ["AÑO", "PERIODO", "Mes Fin", "SIGLA", "Sección", "ACCIÓN FORMATIVA", "ESTRATEGIA_FORMATIVA", "Duración Horas", "Modalidad", "Escuela/Programa (docente)"
    , "Cargo", "Sede (docente)", "Usuario", "Rut", "Apellidos", "Nombre", "Correo", "Estado", "OBSE", "Trayectoria", "RUTA", "MENCIÓN", "A CARGO DE", "PROVEEDOR"]
    # Fill first row with columns
    row = 0
    for i,elem in enumerate(columns):
        worksheet.write(row, i, elem)
    row += 1
    # Now fill other rows with columns
    for item in data:
        worksheet.write(row, 0, item.anio)
        worksheet.write(row, 1, item.periodo)
        worksheet.write(row, 2, item.mes_fin)
        worksheet.write(row, 3, item.sigla)
        worksheet.write(row, 4, item.seccion)
        worksheet.write(row, 5, item.accion_formativa)
        worksheet.write(row, 6, item.estrategia_formativa)
        worksheet.write(row, 7, item.duracion_horas)
        worksheet.write(row, 8, item.modalidad)
        worksheet.write(row, 9, item.codigo)
        worksheet.write(row, 10, item.cargo)
        worksheet.write(row, 11, item.codigo)
        worksheet.write(row, 12, item.username)
        worksheet.write(row, 13, item.rut)
        worksheet.write(row, 14, item.apellido_paterno)
        worksheet.write(row, 15, item.nombres)
        worksheet.write(row, 16, item.email)
        worksheet.write(row, 17, item.estado)
        worksheet.write(row, 18, item.observacion)
        worksheet.write(row, 19, item.trayectoria)
        worksheet.write(row, 20, item.ruta)
        worksheet.write(row, 21, item.mencion)
        worksheet.write(row, 22, item.a_cargo)
        worksheet.write(row, 23, item.proveedor)
        row += 1
    # Close workbook for building file
    workbook.close()
    output.seek(0)
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    return response