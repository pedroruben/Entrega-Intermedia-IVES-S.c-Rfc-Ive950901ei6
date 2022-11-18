from django import forms
from django.forms import ModelForm
from .models import Alumno, Concepto_pagos, Plan

class AlumnoFormulario (forms.Form):
    nombre = forms.CharField(label='Nombre(s)',widget=forms.TextInput(attrs={'placeholder': 'Ingresa el nombre del alumno' , 'class':'form-control'}), max_length=100)
    apellido_paterno = forms.CharField(label='Apellido paterno',widget=forms.TextInput(attrs={'placeholder': 'Ingresa el apellido paterno del alumno' , 'class':'form-control'}), max_length=100)
    apellido_materno = forms.CharField(label='Apellido materno',widget=forms.TextInput(attrs={'placeholder': 'Ingresa el apellido materno del alumno' , 'class':'form-control'}), max_length=100)
    plan_id = forms.ModelChoiceField(queryset=Plan.objects.all())
    fotografia = forms.FileField(label='Fotografia',widget=forms.TextInput(attrs={'id': 'uploadImage1' , 'onchange':'previewImage(1)', 'type': 'file'}))
    certificado = forms.FileField(label='Certificado de bachillerato',widget=forms.TextInput(attrs={'id': 'uploadImage2' , 'onchange':'previewImage(2)', 'type': 'file'}))
    comprobante = forms.FileField(label='Comprobante de domicilio',widget=forms.TextInput(attrs={'id': 'uploadImage3' , 'onchange':'previewImage(3)', 'type': 'file'}))

class Concepto_pagosFormulario (forms.Form):
    descripcion = forms.CharField(label='Descripcion',widget=forms.TextInput(attrs={'placeholder': 'Ingresa la descripcion del concepto de pago' , 'class':'form-control'}), max_length=300)
    cantidad = forms.IntegerField(label='Cantidad a pagar',widget=forms.TextInput(attrs={'placeholder': 'Ingresa la cantidad a pagar de este concepto de pago' , 'class':'form-control'}))

class CuentasXcobrarFormulario (forms.Form):
    concepto_id = forms.ModelChoiceField(queryset=Concepto_pagos.objects.all().only("descripcion"))          
    alumno_id = forms.ModelChoiceField(queryset=Alumno.objects.all())
    estado = forms.CharField(label='Estado',widget=forms.TextInput(attrs={'placeholder': 'Ingresa el estado en el que se encuentra el pago' , 'class':'form-control'}), max_length=300)