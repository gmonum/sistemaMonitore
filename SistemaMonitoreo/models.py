# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib import admin
from model_utils import Choices
from django.contrib.auth.models import User
from datetime import datetime




# Create your models here.

class Ubicacion(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    es_empresa = models.BooleanField
    nombre = models.TextField(null=False, blank=True)
    direccion = models.TextField(null=False, blank=True)
    fecha_inicio_operaciones = models.DateTimeField
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'una Ubicacion'
        verbose_name_plural = 'ubicaciones'

class Insumo(models.Model):
    empresa = models.ForeignKey(Ubicacion,null=False, on_delete=models.CASCADE)
    stock_maximo = models.FloatField(null=False,  default=0.0)
    stock_minimo = models.FloatField(null=False,  default=0.0)
    nombre = models.CharField(max_length=30, null=False, blank=True)
    fecha_ultimo_abastecimiento = models.DateTimeField(null=True)
    stock_actual = models.FloatField(null=False, default=0.0)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'un insumo'
        verbose_name_plural = 'insumos'

class Actividad(models.Model):
    nombre_actividad = models.CharField(max_length=50, null=False, blank=True)
    cantidad_insumo = models.IntegerField(null=True)
    insumo = models.ManyToManyField(Insumo)
    
    def __str__(self):
        return self.nombre_actividad

    class Meta:
        verbose_name = 'una actividad'
        verbose_name_plural = 'actividades'


class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=30, null=False, blank=True)
    descripcion = models.CharField(max_length=100, null=True, blank=True)
    aplica_alerta = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'un tipo de documento'
        verbose_name_plural = 'tipos de documentos'

class Multimedia(models.Model):
    fecha_captura = models.DateField
    fecha_fin_vigencia = models.DateField
    id_tipo_documento = models.ForeignKey(TipoDocumento, on_delete= models.CASCADE )
    documento = models.FileField(null=True,upload_to="documentos/")

    def file_link(self):
        if self.documento:
            return "<a href='%s'>descargar</a>" % (self.documento.url,)
        else:
            return "Sin documento adjunto"

    def __str__(self):
        return self.documento.name


    class Meta:
        verbose_name = 'un documento'
        verbose_name_plural = 'documentos'

class Aptitudes(models.Model):
    titulo = models.CharField(max_length=30, null=False, blank=True)
    descripcion = models.TextField(null=False, blank=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'una Aptitud'
        verbose_name_plural = 'Aptitudes'

class Empleado(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        limit_choices_to={'is_staff': False },
        verbose_name="usuario del sistema",
    )
    documentos = models.ManyToManyField(Multimedia)
    aptitudes = models.ManyToManyField(Aptitudes)
    empresa = models.ManyToManyField(Ubicacion)
    nombre = models.CharField(max_length=30, null=False, blank=True)
    apellido1 = models.CharField(max_length=30, null=False, blank=True)
    apellido2 = models.CharField(max_length=30, null=False, blank=True)
    SEXO = Choices('Elije una opción' , 'Feminino', 'Masculino')
    sexo = models.CharField(choices=SEXO, max_length=30, null=True, default='Elije una opción')
    domicilio = models.CharField(max_length=100, null=False, blank=True)
    rfc = models.CharField(max_length=13, null=False, blank=True)
    curp = models.CharField(max_length=18, null=False, blank=True)
    fecha_ingreso = models.DateField(default=datetime.now, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    celular = models.CharField(max_length=30, null=False, blank=True)
    telefono1 = models.CharField(max_length=30, null=False, blank=True)
    telefono2 = models.CharField(max_length=30, null=False, blank=True)

    def __str__(self):
        return self.nombre + " " + self.apellido1 + " " + self.apellido2
    

    class Meta:
        verbose_name = 'un empleado'
        verbose_name_plural = 'empleados'

class Bitacora(models.Model):
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField(null=True, blank=True)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    actividades = models.ManyToManyField(Actividad)
    evidencias = models.ManyToManyField(Multimedia)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)


