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
from datetime import datetime, timedelta

from .forms import AlumnoFormulario, Concepto_pagosFormulario, CuentasXcobrarFormulario
from .models import Alumno, Concepto_pagos, CuentasXcobrar, Referencias_pagos
from .send_mail_with_python import enviarCorreo

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
                            apellido_materno=informacionAlumno["apellido_materno"], correo_electronico=informacionAlumno["correo_electronico"], 
                            plan_id=informacionAlumno["plan_id"], fotografia=informacionAlumno["fotografia"], certificado=informacionAlumno["certificado"], 
                            comprobante=informacionAlumno["comprobante"])
            # alumno.save()
            nombre_c = informacionAlumno["nombre"]
            apellido_paterno_C = informacionAlumno["apellido_paterno"]
            apellido_materno_c = informacionAlumno["apellido_materno"]
            #Día actual
            today = datetime.today()
            nombre_usuario = nombre_c[0:2] + apellido_paterno_C[0:2] + apellido_materno_c[0:2] + str(today.month) + str(today.day) + str(today.hour) + str(today.minute)
            # usuario = User(username=nombre_usuario, first_name=informacionAlumno["nombre"], last_name=informacionAlumno["apellido_paterno"]+" "+informacionAlumno["apellido_materno"])
            # usuario.set_password(nombre_usuario) #para colocar la contraseña hasheada en la BD
            # usuario.save()
            #:::::::::::::::::::::::::::::::::::::::::
            #fecha de vigencia
            td = timedelta(7)
            vigencia = today + td
            vigencia = vigencia.strftime("%d de %b del %Y") # vigencia = dia de mes del año
            #:::::::::::::::::::::::::::::::::::::::::
            concepto_pagos = Concepto_pagos.objects.all()
            #calculo del total a pagar
            total = 0
            for pago in concepto_pagos:
                total = total + pago.cantidad
            total_a_mostrar = format(total, '0,.2f')
            #:::::::::::::::::::::::::::::::::::::::::
            #se debe hacer una tabla para registrar las referencias, fecha de pago, total, al alumno que pertenecen y sus conceptos de pago
            #la referencia debe tener un total de 27 caracteres
            #la primera parte son 19 caracteres
            referencia = "000000" + str(today.year) + str(today.month) + str(today.day) + str(today.hour) + str(today.minute) + "0" #hasta aqui son 19 caracteres
            fecha_condensada = (int(datetime.strptime(vigencia, "%d de %b del %Y").year) - 2009)*372;
            fecha_condensada = fecha_condensada + ((int(datetime.strptime(vigencia, "%d de %b del %Y").month) - 1)*31);
            fecha_condensada = fecha_condensada + (int(datetime.strptime(vigencia, "%d de %b del %Y").day)-1);
            referencia += str(fecha_condensada)

            importeCon = 0
            digitos = total * 100
            digitos = str(digitos)
            limite = len(digitos)
            i=0
            while i<limite:
                if i==0 or i==3 or i==6:
                    multi=7
                elif i==1 or i==4 or i==7: 
                    multi=3
                elif i==2 or i==5 or i==8: 
                    multi=1
                pos = (i+1) * -1
                val = digitos[pos]
                importeCon = importeCon + int((int(val) * int(multi)))
                i = i+1
            residuo = int(importeCon) % 10
            referencia += str(residuo) + "2"
            limiteRef = len(referencia)
            digitosV = 0
            i = 0
            while i < limiteRef:
                if i==0 or i==5 or i==10 or i==15 or i==20: 
                    multi=11 
                if i==1 or i==6 or i==11 or i==16 or i==21: 
                    multi=13 
                if i==2 or i==7 or i==12 or i==17 or i==22: 
                    multi=17 
                if i==3 or i==8 or i==13 or i==18 or i==23: 
                    multi=19 
                if i==4 or i==9 or i==14 or i==19 or i==24: 
                    multi=23 
                pos = (i+1) * -1
                val = referencia[pos]
                digitosV = digitosV + (int(val) * int(multi))
                i = i+1
            
            residuoV = digitosV % 97
            dV = residuoV + 1
            if dV < 10:
                referencia = referencia + '0' + str(dV)
            else:
                referencia = referencia + str(dV)
            #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            #Registro en base de datos
            alumno_obj = Alumno.objects.filter(nombre=informacionAlumno["nombre"], apellido_paterno=apellido_paterno_C, apellido_materno=apellido_materno_c)#.values()
            id_alumno = [a.id for a in alumno_obj][0]
            # print(int(id_alumno))
            registro_ref = Referencias_pagos(alumno_id_id=int(id_alumno), concepto_id=[c.id for c in concepto_pagos], fecha_vencimiento=datetime.strptime(vigencia, "%d de %b del %Y"), total_pagar=total, referencia=referencia)
            # registro_ref.save()
            print(registro_ref)
            #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            #CODIGO DE BARRAS
            barcode_format = barcode.get_barcode_class('GS1_128')
            my_barcode = barcode_format(referencia, writer=ImageWriter())
            my_barcode.save("media/generated_barcode", {"font_size": 8, "module_height": 5, "text_distance": 3})
            #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            #Envio de correo
            correo_electronico = informacionAlumno["correo_electronico"]
            asunto = "Inscripcion completada - Universidad IVES"
            nombre_completo = informacionAlumno["apellido_paterno"]+ " " + informacionAlumno["apellido_materno"]+ " " + informacionAlumno["nombre"]
            enviarCorreo(correo_electronico, asunto, nombre_completo, nombre_usuario)
            #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            #Envio de datos a la template
            datos_referencia = {"nombre_usuario":nombre_usuario,"nombre":nombre_c, "apellido_paterno":apellido_paterno_C,
                            "apellido_materno":apellido_materno_c, "concepto_pagos":concepto_pagos, "referencia": referencia,
                            "total":total_a_mostrar, "vigencia":vigencia}
            return render(request, "confirmacion.html", context={"datos_referencia": datos_referencia})
    else:
        formulario_alumnos = AlumnoFormulario()
        return render(request, "agregar_alumno.html", {"formulario_alumnos": formulario_alumnos})

def buscarRef(request):
        inner_qs = Referencias_pagos.objects.all().values('alumno_id_id').distinct()
        lista = Alumno.objects.filter(id__in=inner_qs) #De esta forma se buscan los id_Alumno's distintos de Referencias de pagos en Alumnos para sacar sus datos pero sin que se repitan y que solo aparezcan los que tengan referencia de pago
        # lista = Referencias_pagos.objects.all().values('alumno_id_id').distinct()
        return render(request, "buscar_referencias.html", {"lista_alumnos": lista})

def listar_ref_por_alumno(request):
    referencias_lista = []
    if request.POST["id_del_alumno"]:
        alumno_id = request.POST["id_del_alumno"]
        referencias = Referencias_pagos.objects.filter(alumno_id_id=alumno_id)
        #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        #Datos del alumno
        # alumno_query = Alumno.objects.filter(id=alumno_id)
        # nombre = [a.nombre for a in alumno_query][0]
        # apellido_paterno = [a.apellido_paterno for a in alumno_query][0]
        # apellido_materno = [a.apellido_materno for a in alumno_query][0]
        #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        #Conceptos de pago
        datos_referencias = {}
        for referencia in referencias:
            conceptos = referencia.concepto_id
            conceptos = conceptos.replace('[', '')
            conceptos = conceptos.replace(']', '')
            conceptos = list(conceptos.split(","))
            concepto_pagos = []
            for concepto in conceptos:
                descripcion_query = Concepto_pagos.objects.filter(id=int(concepto))
                descripcion = [c.descripcion for c in descripcion_query][0]
                print(f'El valor de descripcion es {descripcion}')
                concepto_pagos.append(descripcion)
            datos_referencias = {"alumno_id":alumno_id,"id_referencia":referencia.id,"concepto_pagos":concepto_pagos,"fecha_vencimiento":referencia.fecha_vencimiento, "total_pagar":referencia.total_pagar,"referencia":referencia.referencia}
            referencias_lista.append(datos_referencias)
        #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        #Datos del alumno
        alumno_query = Alumno.objects.filter(id=alumno_id)
        nombre = [a.nombre for a in alumno_query][0]
        apellido_paterno = [a.apellido_paterno for a in alumno_query][0]
        apellido_materno = [a.apellido_materno for a in alumno_query][0]
        inner_qs = Referencias_pagos.objects.all().values('alumno_id_id').distinct()
        lista = Alumno.objects.filter(id__in=inner_qs) #De esta forma se buscan los id_Alumno's distintos de Referencias de pagos en Alumnos para sacar sus datos pero sin que se repitan y que solo aparezcan los que tengan referencia de pago
        return render(request, "buscar_referencias.html", {"referencias": referencias_lista, "lista_alumnos": lista})

def buscar_referencia(request):
    if request.POST["id_referencia"]:
        id_ref = request.POST["id_referencia"]
        alumno_id = request.POST["id_alumno"]
        referencia_query = Referencias_pagos.objects.filter(id=id_ref)
        #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        #Datos del alumno
        alumno_query = Alumno.objects.filter(id=alumno_id)
        nombre = [a.nombre for a in alumno_query][0]
        apellido_paterno = [a.apellido_paterno for a in alumno_query][0]
        apellido_materno = [a.apellido_materno for a in alumno_query][0]
        #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        #concepto de pagos, para sacar su descripcion y cantidad a pagar
        conceptos = [r.concepto_id for r in referencia_query][0]
        conceptos = conceptos.replace('[', '')
        conceptos = conceptos.replace(']', '')
        conceptos = list(conceptos.split(","))
        concepto_pagos = []
        for concepto in conceptos:
            descripcion_query = Concepto_pagos.objects.filter(id=int(concepto))
            descripcion = [c.descripcion for c in descripcion_query][0]
            cantidad = [c.cantidad for c in descripcion_query][0]
            print(f'El valor de descripcion es {descripcion}')
            concepto_pagos_str = descripcion + " con un costo de: $"+str(cantidad) +"mxn"
            concepto_pagos.append(concepto_pagos_str)
        #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        # Formato para la vigencia            
        vigencia = [r.fecha_vencimiento for r in referencia_query][0]
        vigencia = vigencia.strftime("%d de %b del %Y") # vigencia = dia de mes del año
        #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        #Formato para el total
        total = format([r.total_pagar for r in referencia_query][0], '0,.2f')
        #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        #CODIGO DE BARRAS
        barcode_format = barcode.get_barcode_class('GS1_128')
        my_barcode = barcode_format([r.referencia for r in referencia_query][0], writer=ImageWriter())
        my_barcode.save("media/generated_barcode", {"font_size": 8, "module_height": 5, "text_distance": 3})
        #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        #Envio de datos a la template
        datos_referencia = {"nombre":nombre, "apellido_paterno":apellido_paterno,"apellido_materno":apellido_materno, 
                            "concepto_pagos":concepto_pagos, "referencia": [r.referencia for r in referencia_query][0],
                            "total":total, "vigencia":vigencia}
        lista = Alumno.objects.all()
        return render(request, "buscar_referencias.html", {"datos_referencia": datos_referencia, "lista_alumnos": lista})
    else:
        lista = Alumno.objects.all()
        return render(request, "buscar_referencias.html", {"lista_alumnos": lista})

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