# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-09 02:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Aptitudes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(blank=True, max_length=30)),
                ('descripcion', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'una Aptitud',
                'verbose_name_plural': 'Aptitudes',
            },
        ),
        migrations.CreateModel(
            name='Bitacora',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora_inicio', models.DateTimeField()),
                ('fecha_hora_fin', models.DateTimeField()),
                ('actividades', models.ManyToManyField(to='SistemaMonitoreo.Actividad')),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=30)),
                ('apellido1', models.CharField(blank=True, max_length=30)),
                ('apellido2', models.CharField(blank=True, max_length=30)),
                ('sexo', models.CharField(choices=[('Elije una opci\xf3n', 'Elije una opci\xf3n'), ('Feminino', 'Feminino'), ('Masculino', 'Masculino')], default='Elije una opci\xf3n', max_length=30, null=True)),
                ('domicilio', models.CharField(blank=True, max_length=100)),
                ('rfc', models.CharField(blank=True, max_length=30)),
                ('curp', models.CharField(blank=True, max_length=30)),
                ('celular', models.CharField(blank=True, max_length=30)),
                ('telefono1', models.CharField(blank=True, max_length=30)),
                ('telefono2', models.CharField(blank=True, max_length=30)),
                ('aptitudes', models.ManyToManyField(to='SistemaMonitoreo.Aptitudes')),
            ],
            options={
                'verbose_name': 'un empleado',
                'verbose_name_plural': 'empleados',
            },
        ),
        migrations.CreateModel(
            name='Insumo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(blank=True, max_length=30)),
                ('stock_maximo', models.FloatField(default=0.0)),
                ('stock_minimo', models.FloatField(default=0.0)),
                ('nombre', models.CharField(blank=True, max_length=30)),
                ('fecha_ultimo_abastecimiento', models.DateTimeField(null=True)),
                ('stock_actual', models.FloatField(default=0.0)),
            ],
            options={
                'verbose_name': 'un insumo',
                'verbose_name_plural': 'insumos',
            },
        ),
        migrations.CreateModel(
            name='Multimedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documento', models.FileField(null=True, upload_to=b'')),
            ],
            options={
                'verbose_name': 'un documento',
                'verbose_name_plural': 'documentos',
            },
        ),
        migrations.CreateModel(
            name='TipoDocumento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=30)),
                ('descripcion', models.CharField(blank=True, max_length=100, null=True)),
                ('aplica_alerta', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'un tipo de documento',
                'verbose_name_plural': 'tipos de documentos',
            },
        ),
        migrations.CreateModel(
            name='Ubicacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(blank=True)),
                ('direccion', models.TextField(blank=True)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='SistemaMonitoreo.Ubicacion')),
            ],
            options={
                'verbose_name': 'una Ubicacion',
                'verbose_name_plural': 'ubicaciones',
            },
        ),
        migrations.AddField(
            model_name='multimedia',
            name='id_tipo_documento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SistemaMonitoreo.TipoDocumento'),
        ),
        migrations.AddField(
            model_name='insumo',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SistemaMonitoreo.Ubicacion'),
        ),
        migrations.AddField(
            model_name='empleado',
            name='documentos',
            field=models.ManyToManyField(to='SistemaMonitoreo.Multimedia'),
        ),
        migrations.AddField(
            model_name='empleado',
            name='empresa',
            field=models.ManyToManyField(to='SistemaMonitoreo.Ubicacion'),
        ),
        migrations.AddField(
            model_name='empleado',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bitacora',
            name='empleado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SistemaMonitoreo.Empleado'),
        ),
        migrations.AddField(
            model_name='bitacora',
            name='evidencias',
            field=models.ManyToManyField(to='SistemaMonitoreo.Multimedia'),
        ),
        migrations.AddField(
            model_name='bitacora',
            name='ubicacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SistemaMonitoreo.Ubicacion'),
        ),
        migrations.AddField(
            model_name='actividad',
            name='insumo',
            field=models.ManyToManyField(to='SistemaMonitoreo.Insumo'),
        ),
    ]
