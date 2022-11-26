"""ProyectoCoder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView
from AppCoder.views import AgregarAlumno, Inicio, AgregarConcepto, AgregarCuenta, buscar_cuentas, buscar, loginView, register, codigo_barras, buscar_referencia, buscarRef, listar_ref_por_alumno, actRef, guardarActRef

urlpatterns = [
    path('admin/', admin.site.urls),
    path('agregar/',AgregarAlumno, name="Agregar"),
    path('agregar_conceptos/',AgregarConcepto, name="AgregarConceptos"),
    path('agregar_cuentas/',AgregarCuenta, name="AgregarCuentas"),
    path('buscar_cuentas/', buscar_cuentas, name="BuscarCuentas"),
    path('buscar/', buscar, name="Buscar"),
    path('buscarRef/', buscarRef, name="BuscarR"),
    path('listar_referencia/', listar_ref_por_alumno, name="ListarRef"),
    path('buscar_referencia/', buscar_referencia, name="BuscarRef"),
    path('actualizar_referencia/', actRef, name="ActRef"),
    path('guardar_referencia/', guardarActRef, name="GuardarActRef"),
    path('', Inicio, name="Inicio"),
    path('login/', loginView, name="Login"),
    path('registrar/', register, name="Registrar"),
    path('logout/', LogoutView.as_view(template_name="logout.html"), name="Logout"),
    path('barra/', codigo_barras, name="Codigo"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)