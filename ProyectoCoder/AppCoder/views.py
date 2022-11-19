from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout, authenticate
from datetime import date

from .forms import AlumnoFormulario, Concepto_pagosFormulario, CuentasXcobrarFormulario
from .models import Alumno, Concepto_pagos, CuentasXcobrar

import barcode
from barcode.writer import ImageWriter

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
        return render(request, "buscar_cuentas.html", {"cuentas": cuentas, "lista_alumnos": lista})

@login_required
def AgregarAlumno(request):
    if request.method == "POST":
        formulario_alumnos = AlumnoFormulario(request.POST, request.FILES)

        if formulario_alumnos.is_valid():
            informacionAlumno = formulario_alumnos.cleaned_data
            alumno = Alumno(nombre=informacionAlumno["nombre"], apellido_paterno=informacionAlumno["apellido_paterno"],
                            apellido_materno=informacionAlumno["apellido_materno"], plan_id=informacionAlumno["plan_id"], fotografia=informacionAlumno["fotografia"], certificado=informacionAlumno["certificado"], comprobante=informacionAlumno["comprobante"])
            # alumno.save()
            nombre_c = informacionAlumno["nombre"]
            apellido_paterno_C = informacionAlumno["apellido_paterno"]
            apellido_materno_c = informacionAlumno["apellido_materno"]
            #Día actual
            today = date.today()
            nombre_usuario = nombre_c[0:2] + apellido_paterno_C[0:2] + apellido_materno_c[0:2] + str(today.year) + str(today.month) + str(today.day)
            # usuario = User(username=nombre_usuario, first_name=informacionAlumno["nombre"], last_name=informacionAlumno["apellido_paterno"]+" "+informacionAlumno["apellido_materno"])
            # usuario.set_password(nombre_usuario) #para colocar la contraseña hasheada en la BD
            # usuario.save()

            fecha = "10-12-2022"
            total = 1000
            referencia = "123456789"
            concepto_pagos = Concepto_pagos.objects.all()
            datos_referencia = {"nombre_usuario":nombre_usuario,"nombre":nombre_c, "apellido_paterno":apellido_paterno_C,
                            "apellido_materno":apellido_materno_c, "concepto_pagos":concepto_pagos, "referencia": referencia,
                            "total":total, "fecha":fecha}

            # return HttpResponseRedirect('/')
            return render(request, "confirmacion.html", context={"datos_referencia": datos_referencia})
    else:
        formulario_alumnos = AlumnoFormulario()
        return render(request, "agregar_alumno.html", {"formulario_alumnos": formulario_alumnos})


def AgregarConcepto(request):
    if request.method == "POST":
        formulario_concepto = Concepto_pagosFormulario(request.POST)
        print(formulario_concepto)

        if formulario_concepto.is_valid():
            informacionConcepto = formulario_concepto.cleaned_data
            concepto = Concepto_pagos(
                descripcion=informacionConcepto["descripcion"], cantidad=informacionConcepto["cantidad"])
            concepto.save()

            return HttpResponseRedirect('/')

    else:
        formulario_concepto = Concepto_pagosFormulario()
        return render(request, "agregar_conceptos.html", {"formulario_concepto": formulario_concepto})


def AgregarCuenta(request):
    if request.method == "POST":
        formulario_cuenta = CuentasXcobrarFormulario(request.POST)
        print(formulario_cuenta)

        if formulario_cuenta.is_valid():
            informacionCuenta = formulario_cuenta.cleaned_data
            cuenta = CuentasXcobrar(
                concepto_id=informacionCuenta["concepto_id"], alumno_id=informacionCuenta["alumno_id"], estado=informacionCuenta["estado"])
            cuenta.save()

            return HttpResponseRedirect('/')

    else:
        formulario_cuenta = CuentasXcobrarFormulario()
        return render(request, "agregar_cuentas.html", {"formulario_cuenta": formulario_cuenta})


def loginView(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            data = form.cleaned_data

            usuario = data['username']
            psw = data['password']

            user = authenticate(username=usuario, password=psw)

            if user:
                login(request, user)
                return render(request, "inicio.html", {'mensaje': f'Bienvenido {usuario}'})
            else:
                return render(request, "inicio.html", {'mensaje': f'Error, datos incorrectos'})

        return render(request, "inicio.html", {'mensaje': f'Error en el formulario'})

    else:
        form = AuthenticationForm()
        return render(request, "login.html", {"form": form})

@staff_member_required
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            form.save()
            return render(request, "inicio.html", {'mensaje': f'Usuario {username} creado con exito'})
        else:
            return render(request, "inicio.html", {'mensaje': f'Error al crear el usuario'})
    else:
        form = UserCreationForm()
        return render(request, "registro.html", {"form": form})

def codigo_barras(request):
    number = '049000042511'
    barcode_format = barcode.get_barcode_class('upc')
    my_barcode = barcode_format(number, writer=ImageWriter())
    my_barcode.save("media/generated_barcode")
    return render(request, "codigo_barra.html", {"my_barcode": my_barcode})