from django.db import models

# Create your models here.
class Plan (models.Model):
    DESCRIPCION = models.CharField(max_length=300)
    acuerdo = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.DESCRIPCION} {self.acuerdo}'

class Alumno (models.Model):
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE)
    fotografia = models.ImageField(upload_to="fotografias", null=True)
    certificado = models.ImageField(upload_to="certificados", null=True)
    comprobante = models.ImageField(upload_to="comprobantes", null=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido_paterno} {self.apellido_materno}'

class Concepto_pagos (models.Model):
    descripcion = models.CharField(max_length=300)
    cantidad = models.IntegerField()

    def __str__(self):
        return f'{self.descripcion} con valor de: ${self.cantidad}'

class CuentasXcobrar (models.Model):
    concepto_id = models.ForeignKey(Concepto_pagos, on_delete=models.CASCADE)
    alumno_id = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    estado = models.CharField(max_length=300)

class Referencias_pagos (models.Model):
    alumno_id = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    concepto_id = models.CharField(max_length=100)
    fecha_vencimiento = models.DateField()
    total_pagar = models.IntegerField()
    referencia = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.alumno_id} con valor de: ${self.total_pagar} y que vence el: {self.fecha_vencimiento}'