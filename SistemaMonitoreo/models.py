# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from mptt.models import MPTTModel
from django.contrib import admin
from model_utils import Choices



# Create your models here.

class Ubicacion(MPTTModel):
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    es_empresa = models.BooleanField
    nombre = models.TextField(null=False, blank=True)
    direccion = models.TextField(null=False, blank=True)
    fecha_inicio_operaciones = models.DateTimeField
    def __unicode__(self):
        return self.description
    class Meta:
        verbose_name = 'una Ubicacion'
        verbose_name_plural = 'Ubicaciones'

class Insumo(models.Model):
    empresa = models.ForeignKey(Ubicacion,null=False)
    descripcion = models.CharField(max_length=30, null=False, blank=True)
    stock_maximo = models.FloatField(null=False,  default=0.0)
    stock_minimo = models.FloatField(null=False,  default=0.0)
    nombre = models.CharField(max_length=30, null=False, blank=True)
    fecha_ultimo_abastecimiento = models.DateTimeField(null=True)
    stock_actual = models.FloatField(null=False, default=0.0)

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = 'un Insumo'
        verbose_name_plural = 'Insumos'

class Actividad(models.Model):
    cantidad_insumo = models.IntegerField
    insumo = models.ManyToManyField(Insumo)


class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=30, null=False, blank=True)
    descripcion = models.CharField(max_length=30, null=True, blank=True)
    aplica_alerta = models.BooleanField(default=False)

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = 'Un tipo de documento'
        verbose_name_plural = 'Tipos de documentos'

class Multimedia(models.Model):
    fecha_captura = models.DateField
    fecha_fin_vigencia = models.DateField
    id_tipo_documento = models.ForeignKey(TipoDocumento, on_delete= models.CASCADE )

class Aptitudes(models.Model):
    titulo = models.CharField(max_length=30, null=False, blank=True)
    descripcion = models.TextField(null=False, blank=True)

class Empleado(models.Model):
    documentos = models.ManyToManyField(Multimedia)
    aptitudes = models.ManyToManyField(Aptitudes)
    empresa = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30, null=False, blank=True)
    apellido1 = models.CharField(max_length=30, null=False, blank=True)
    apellido2 = models.CharField(max_length=30, null=False, blank=True)
    SEXO = Choices('Elije' , 'Feminino', 'Masculino')
    sexo = models.CharField(choices=SEXO, max_length=30, null=True, default='Elije')
    domicilio = models.CharField(max_length=100, null=False, blank=True)
    rfc = models.CharField(max_length=30, null=False, blank=True)
    curp = models.CharField(max_length=30, null=False, blank=True)
    fecha_ingreso = models.DateField
    fecha_nacimiento = models.DateField
    celular = models.CharField(max_length=30, null=False, blank=True)
    telefono1 = models.CharField(max_length=30, null=False, blank=True)
    telefono2 = models.CharField(max_length=30, null=False, blank=True)

class Bitacora(models.Model):
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField()
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    actividades = models.ManyToManyField(Actividad)
    evidencias = models.ManyToManyField(Multimedia)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)


admin.site.register(TipoDocumento)
admin.site.register(Ubicacion)
admin.site.register(Empleado)