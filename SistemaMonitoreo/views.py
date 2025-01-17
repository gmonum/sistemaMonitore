# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from SistemaMonitoreo.models import Bitacora, Ubicacion, Empleado, Actividad
from SistemaMonitoreo.forms import BitacoraForm
from django.utils import timezone
import logging
import os

from django.http.request import HttpRequest
from django.template.context_processors import request


 

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
         profile = request.user.is_staff
         logger.info('Usuario registrado: ' + User.objects.get(id=request.session['_auth_user_id']).__str__())
         logger.info('El Perfil del usuario es de staff: ' + profile.__str__()) 
         #logger.info()
         logger.info(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
         return TemplateResponse(request,'accounts/profile/index.html')

def duty_record(request):
     logger = logging.getLogger('SistemaMonitoreo')
     if not '_auth_user_id' in request.session:
         return HttpResponseRedirect('/login')
     else:
         empl_id = Empleado.objects.get(user_id=request.session['_auth_user_id']).id
         logger.info(empl_id)
         emp_ubicacion = Empleado.objects.get(user_id=request.session['_auth_user_id']).empresa
         return render(request, 'record/activities/index.html',
                                    {'actividades': Actividad.objects.all(),
                                     'ubicaciones': emp_ubicacion.all(),
                                     'inicia': True})
         #return TemplateResponse(request, 'record/activities/index.html', '')
         
def duty_record2(request):
     logger = logging.getLogger('SistemaMonitoreo')
     form = BitacoraForm(request.POST, request.FILES)
     if not '_auth_user_id' in request.session:
         return HttpResponseRedirect('/login')
     else:
         empl_id = Empleado.objects.get(user_id=request.session['_auth_user_id']).id
         logger.info(empl_id)
         emp_ubicacion = Empleado.objects.get(user_id=request.session['_auth_user_id']).empresa
         return render(request, 'record/activities/actividad.html',
                                    {
                                    'form':form,
                                    'actividades': Actividad.objects.all(),
                                    'nodes': Ubicacion.objects.all() })
         #return TemplateResponse(request, 'record/activities/index.html', '')

def duty_record_finalize(request, id):
     logger = logging.getLogger('SistemaMonitoreo')
     
     id_sent = id
     if not '_auth_user_id' in request.session:
         return HttpResponseRedirect('/login')
     else:
         logger.info('El id que quiere finalizar es: ' + id_sent.__str__())
         logger.info('El id_empleado del la bitacora es: ' + Bitacora.objects.get(id=id_sent).empleado_id.__str__())
         logger.info('El id_ubicacion de la bitacora es: ' + Bitacora.objects.get(id=id_sent).ubicacion_id.__str__())
     
         actividad_selecc = Bitacora.objects.get(id=id_sent).actividades
     return render(request, 'record/activities/index.html',
                                    {'bitacora': Bitacora.objects.filter(id=id_sent),
                                     'actividad': actividad_selecc.all(),
                                     'empleado': Empleado.objects.filter(id=Bitacora.objects.get(id=id_sent).empleado_id),
                                     'ubicacion': Ubicacion.objects.filter(id=Bitacora.objects.get(id=id_sent).ubicacion_id),
                                     'id': id_sent,
                                     'finaliza': True })


def save_update_activity(request, id):
     logger = logging.getLogger('SistemaMonitoreo')
     
     logger.info('El id ingresado es: ' + id.__str__())
     
     if int(id) > 0:
         request.session['id_actividad'] = id
         logger.info('lo agrego al session')
     else:
         if 'id_actividad' in request.session:
             del request.session['id_actividad']
             logger.info('lo borro de session')
     
     if  not 'id_actividad' in request.session and request.method == "POST":
         
         actividad_sel = request.POST["id_actividad"]
         ubicacion_sel = request.POST['id_ubicacion']
     
         request.session['ubicacion'] = Ubicacion.objects.get(id=ubicacion_sel)
         request.session['empleado'] = Empleado.objects.get(user_id=User.objects.get(id=request.session['_auth_user_id']))
         
         logger.info('Se realizara un inicio de actividad')
         hora_ini = request.POST["time_ini"]
         
         logger.info('La hora html: ' + hora_ini)
         logger.info('Hora actual: ' +  timezone.now().__str__())
         logger.info('La actividad seleccionada es: ' + actividad_sel)
         logger.info(u'La actividad sera: ' + Actividad.objects.get(id=actividad_sel).__str__().decode('utf-8'))
         logger.info('La ubicacion seleccionada es: ' + ubicacion_sel)
         logger.info('La ubicacion sera: ' + Ubicacion.objects.get(id=ubicacion_sel).__str__().decode('utf-8'))
         
         bitacora = Bitacora()
         bitacora.fecha_hora_inicio = timezone.now()
         bitacora.ubicacion = request.session.pop('ubicacion')
         logger.info('El empleado sera: ' + request.session['empleado'].__str__().decode('utf-8'))
         bitacora.empleado = request.session.pop('empleado')
         bitacora.save()
         logger.info('El id de la bitacora es: ' + bitacora.pk.__str__())
         logger.info('Elemento Bitacora guardado')
         
         bitacora.actividades.add(Actividad.objects.get(id=actividad_sel))
         bitacora.save()
         logger.info('Elemento Bitacora-Actividad guardado')
         return HttpResponseRedirect('/')
         #return TemplateResponse(request,'accounts/profile/index.html')
     else:
         logger.info('Se realizara un fin de actividad')
         Bitacora.objects.filter(id=request.session.pop('id_actividad')).update(fecha_hora_fin=timezone.now())
         logger.info('Elemento Bitacora id = ' + id.__str__() + ' actualizado a las ' + timezone.now().__str__())
         return HttpResponseRedirect('/')
         #return TemplateResponse(request,'accounts/profile/index.html')

def listado_user_actividades(request):
     logger = logging.getLogger('SistemaMonitoreo')
     if not '_auth_user_id' in request.session:
         return HttpResponseRedirect('/login')
     else:
         return render(request, 'record/activities/list/index.html',
                                    {'bitacora': Bitacora.objects.filter(empleado_id=Empleado.objects.get(user_id=User.objects.get(id=request.session['_auth_user_id']))).filter(fecha_hora_fin=None)})

def listado_todas_actividades(request):
     logger = logging.getLogger('SistemaMonitoreo')
     if not '_auth_user_id' in request.session:
         return HttpResponseRedirect('/login')
     else:
         return render(request, 'record/activities/list/index.html',
                                    {'bitacora': Bitacora.objects.all(),
                                     'consulta': True})
def duty_record_review(request, id):
     logger = logging.getLogger('SistemaMonitoreo')
     
     id_sent = id
     if not '_auth_user_id' in request.session:
         return HttpResponseRedirect('/login')
     else:
         logger.info('El id que quiere revisar es: ' + id_sent.__str__())
         logger.info('El id_empleado del la bitacora es: ' + Bitacora.objects.get(id=id_sent).empleado_id.__str__())
         logger.info('El id_ubicacion de la bitacora es: ' + Bitacora.objects.get(id=id_sent).ubicacion_id.__str__())
     
         actividad_selecc = Bitacora.objects.get(id=id_sent).actividades
     return render(request, 'record/activities/review/index.html',
                                    {'bitacora': Bitacora.objects.filter(id=id_sent),
                                     'actividad': actividad_selecc.all(),
                                     'empleado': Empleado.objects.filter(id=Bitacora.objects.get(id=id_sent).empleado_id),
                                     'ubicacion': Ubicacion.objects.filter(id=Bitacora.objects.get(id=id_sent).ubicacion_id),
                                     'id': id_sent,
                                     'visualiza': True })

def duty_record_fin(request, id):
     logger = logging.getLogger('SistemaMonitoreo')
     
     if not '_auth_user_id' in request.session:
         return HttpResponseRedirect('/login')
     else:
         logger.info('El id que mandaron es: ' + id)
         return HttpResponse('HELLO WORLD')


     
     
    