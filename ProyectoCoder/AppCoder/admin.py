from django.contrib import admin

from AppCoder.models import Concepto_pagos, CuentasXcobrar, Alumno

# Register your models here.

admin.site.register(Alumno)
admin.site.register(Concepto_pagos)
admin.site.register(CuentasXcobrar)