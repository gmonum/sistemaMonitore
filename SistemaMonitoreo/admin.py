# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Empleado, TipoDocumento, Ubicacion, Aptitudes, Multimedia, Actividad, Insumo


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    save_on_top = True
    filter_horizontal=['empresa', 'aptitudes', 'documentos']
    fields=[('nombre','apellido1', 'apellido2'),
    	('domicilio', 'sexo', 'fecha_nacimiento'), 
    	('rfc', 'curp', 'fecha_ingreso'), 
    	('celular', 'telefono1', 'telefono2'),
    	'user',
    	'empresa', 
    	'aptitudes',
    	'documentos'
    ]
    
    
@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    save_on_top = True
    fields=['nombre_actividad',
        'insumo', 
        'cantidad_insumo'
    ]
    
    
#Registros
admin.site.register(TipoDocumento)
admin.site.register(Ubicacion)
admin.site.register(Aptitudes)
admin.site.register(Multimedia)
admin.site.register(Insumo)
