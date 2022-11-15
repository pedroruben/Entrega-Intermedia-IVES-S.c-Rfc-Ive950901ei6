from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView

from .forms import AlumnoFormulario, Concepto_pagosFormulario, CuentasXcobrarFormulario
from .models import Alumno, Concepto_pagos, CuentasXcobrar

# Create your views here.
def Inicio(request):
    return render(request, "inicio.html")

def buscar_cuentas(request):
    lista = Alumno.objects.all()
    return render(request, "buscar_cuentas.html", {"lista_alumnos": lista})

def buscar(request):
    if request.POST["id_del_alumno"]:
        alumno_id = request.POST["id_del_alumno"]
        cuentas = CuentasXcobrar.objects.filter(alumno_id=alumno_id)
        lista = Alumno.objects.all()
        return render(request, "buscar_cuentas.html", {"cuentas":cuentas, "lista_alumnos": lista})

def AgregarAlumno (request):
    if request.method == "POST":
        formulario_alumnos = AlumnoFormulario(request.POST, request.FILES)
        print(formulario_alumnos)

        if formulario_alumnos.is_valid():
            informacionAlumno = formulario_alumnos.cleaned_data
            alumno = Alumno(nombre=informacionAlumno["nombre"], apellido_paterno=informacionAlumno["apellido_paterno"], apellido_materno=informacionAlumno["apellido_materno"], plan=informacionAlumno["plan"], fotografia=informacionAlumno["fotografia"])
            alumno.save()

            return HttpResponseRedirect('/')

    else:
        formulario_alumnos = AlumnoFormulario()
        return render(request, "agregar_alumno.html", {"formulario_alumnos":formulario_alumnos})

def AgregarConcepto (request):
    if request.method == "POST":
        formulario_concepto = Concepto_pagosFormulario(request.POST)
        print(formulario_concepto)

        if formulario_concepto.is_valid():
            informacionConcepto = formulario_concepto.cleaned_data
            concepto = Concepto_pagos(descripcion=informacionConcepto["descripcion"], cantidad=informacionConcepto["cantidad"])
            concepto.save()

            return HttpResponseRedirect('/')

    else:
        formulario_concepto = Concepto_pagosFormulario()
        return render(request, "agregar_conceptos.html", {"formulario_concepto":formulario_concepto})

def AgregarCuenta (request):
    if request.method == "POST":
        formulario_cuenta = CuentasXcobrarFormulario(request.POST)
        print(formulario_cuenta)

        if formulario_cuenta.is_valid():
            informacionCuenta = formulario_cuenta.cleaned_data
            cuenta = CuentasXcobrar(concepto_id=informacionCuenta["concepto_id"], alumno_id=informacionCuenta["alumno_id"], estado=informacionCuenta["estado"])
            cuenta.save()

            return HttpResponseRedirect('/')

    else:
        formulario_cuenta = CuentasXcobrarFormulario()
        return render(request, "agregar_cuentas.html", {"formulario_cuenta":formulario_cuenta})