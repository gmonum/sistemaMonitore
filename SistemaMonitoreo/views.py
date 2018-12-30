# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, response
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from models import Bitacora, Ubicacion, Empleado
import logging
import os

from django.http.request import HttpRequest

 

def home(request):
     logger = logging.getLogger('SistemaMonitoreo')
     if not '_auth_user_id' in request.session:
         logger.info('No está logeado el dude')
         return HttpResponseRedirect('/login')
     else:
         return HttpResponseRedirect('/accounts/profile')
         #return TemplateResponse(request,'accounts/profile/index.html')
    
def user_profile(request):
     #request.session['logged_in'] = True
     logger = logging.getLogger('SistemaMonitoreo')
     if not '_auth_user_id' in request.session:
         logger.info('No está logeado el dude')
         return HttpResponseRedirect('/login')
     else:
         #request.session['logged_in'] = True
         logger.info("Usuario registrado: ") 
         logger.info(User.objects.get(id=request.session['_auth_user_id']))
         logger.info(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
         return TemplateResponse(request,'accounts/profile/index.html')

def duty_record(request):
     logger = logging.getLogger('SistemaMonitoreo')
     if not '_auth_user_id' in request.session:
         return HttpResponseRedirect('/login')
     else:
         
         return TemplateResponse(request, 'record/activities/index.html')
    
def save_activity(request, user):
    
     bitacora = Bitacora()
     bitacora.object_pk = 4
     bitacora.fecha_hora_inicio = '2018-12-28 01:30:18.280834-06'
     bitacora.fecha_hora_fin = '2018-12-28 03:30:18.280834-06'
     bitacora.ubicacion = Ubicacion.objects.get(id='1')
     bitacora.empleado = Empleado.objects.get(id='2')
     bitacora.save()
     logger.info(bitacora)
     logger.info('Elemento Bitacora guardado')
     
     
    