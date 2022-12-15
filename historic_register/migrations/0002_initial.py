# Generated by Django 4.0.6 on 2022-09-07 03:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
        ('historic_register', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrohistorico',
            name='estado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.estado'),
        ),
        migrations.AddField(
            model_name='registrohistorico',
            name='modalidad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='historic_register.modalidad'),
        ),
        migrations.AddField(
            model_name='registrohistorico',
            name='proveedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='historic_register.proveedor'),
        ),
        migrations.AddField(
            model_name='registrohistorico',
            name='rol',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.rol'),
        ),
        migrations.AddField(
            model_name='registrohistorico',
            name='sede',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='historic_register.sede'),
        ),
        migrations.AddField(
            model_name='registrohistorico',
            name='sigla',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='historic_register.sigla'),
        ),
        migrations.AddField(
            model_name='registrohistorico',
            name='tipo_disciplinar',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='historic_register.tipodisciplinar'),
        ),
        migrations.AddField(
            model_name='registrohistorico',
            name='tipo_habilitacion_trayectoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='historic_register.tipohabilitaciontrayectoria'),
        ),
        migrations.AddField(
            model_name='registrohistorico',
            name='unidad_solicitante',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='historic_register.unidadsolicitante'),
        ),
        migrations.AddField(
            model_name='registrohistorico',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
