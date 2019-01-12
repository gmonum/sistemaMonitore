# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Empleado, TipoDocumento, Ubicacion, Aptitudes, Multimedia, Actividad, Insumo
from django.utils.html import mark_safe

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    save_on_top = True
    change_template = 'admin/empleado_admin.html'
    filter_horizontal=['empresa', 'aptitudes', 'documentos']
    fields=[('nombre','apellido1', 'apellido2'),
    	('domicilio', 'sexo', 'fecha_nacimiento'), 
    	('rfc', 'curp', 'fecha_ingreso'), 
    	('celular', 'telefono1', 'telefono2'),
    	'user',
    	'empresa', 
    	'aptitudes',
    	'documentos',
    ]
    readonly_fields = ['documentos']

    def change_view(self, request, object_id, form_url = '', extra_context=None):
        
        response = super(EmpleadoAdmin, self).change_view(
            request,
            object_id, 
            form_url, 
            extra_context=extra_context,
        )

        response.context_data['documents_lst'] =  Multimedia.objects.all()
        
        return response
    
    #def lista_documentos(self, obj):
    #	listado = '<table>'
    #	for doc in obj.documentos.all():
    #		listado += '<tr>' + doc.name + '</tr>' 
    #	listado += '</table>'
    #	return mark_safe(listado)
    #lista_documentos.short_description = "Documentos"
    #readonly_fields["lista_documentos"]

    
    
@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    save_on_top = True
    filter_horizontal=['insumo']
    fields=['nombre_actividad',
        'insumo', 
        'cantidad_insumo'
    ]

@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    save_on_top = True
    fields=['nombre',
        'empresa', 
        'stock_maximo',
        'stock_minimo',
        'fecha_ultimo_abastecimiento',
        'stock_actual'
    ]

@admin.register(Multimedia)
class MultimediaAdmin(admin.ModelAdmin):
    save_on_top = True
    
    
    
    
#Registros
admin.site.register(TipoDocumento)
admin.site.register(Ubicacion)
admin.site.register(Aptitudes)
