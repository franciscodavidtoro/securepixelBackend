# Generated by Django 5.2.3 on 2025-07-16 23:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ensennanza', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='atencion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('vectorOjosCerados', models.JSONField(blank=True, default=None, null=True)),
                ('vectorAnguloCabeza', models.JSONField(blank=True, default=None, null=True)),
                ('tiempoLectura', models.FloatField(blank=True, default=None, null=True)),
                ('Usuario', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tema', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='ensennanza.tema')),
            ],
        ),
    ]
