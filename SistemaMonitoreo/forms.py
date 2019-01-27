from models import Bitacora
from django import forms
from django.db import models
from mptt.forms import TreeNodeChoiceField
from django.db.models import Q
from django.contrib.auth.models import User
class BitacoraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BitacoraForm, self).__init__(*args, **kwargs)
        #if self.instance:
        # self.fields['lugarCategory'] = TreeNodeChoiceField(queryset=LugarC.tree.all(),level_indicator=u'+--')
    class Meta:
        model = Bitacora
        fields = ('fecha_hora_inicio','fecha_hora_fin', 'actividades','evidencias', 'empleado', 'ubicacion')
        widgets = {
            'fecha_hora_inicio':  forms.DateTimeInput(attrs={'class':'combo'}, format='%d/%m/%Y %H:%M'),
            'fecha_hora_fin': forms.DateTimeInput(attrs={'class':'combo'}, format='%d/%m/%Y %H:%M'),
            'actividades': forms.Select(attrs={'class':'combo','size':'80', 'cols':'80'}),
            'evidencias': forms.TextInput(attrs={'required':True}),
            'empleado': forms.Select(attrs={'size':'80', 'cols':'80', 'required':True}),
        }