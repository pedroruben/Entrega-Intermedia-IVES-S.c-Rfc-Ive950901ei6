from django.contrib import admin

from AppCoder.models import Concepto_pagos, CuentasXcobrar, Alumno, Referencias_pagos, Estatus_doc

# Register your models here.

admin.site.register(Alumno)
admin.site.register(Concepto_pagos)
admin.site.register(CuentasXcobrar)
admin.site.register(Referencias_pagos)
admin.site.register(Estatus_doc)