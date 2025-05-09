# Generated by Django 5.2 on 2025-04-21 03:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_normativa_delete_cita_delete_vehiculo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placa', models.CharField(max_length=10)),
                ('marca', models.CharField(max_length=50)),
                ('modelo', models.CharField(max_length=50)),
                ('anio', models.PositiveIntegerField()),
                ('tipo_combustible', models.CharField(choices=[('Gasolina', 'Gasolina'), ('Diésel', 'Diésel'), ('Eléctrico', 'Eléctrico'), ('Híbrido', 'Híbrido')], max_length=20)),
                ('usa_obd', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Verificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('co_emitido', models.DecimalField(decimal_places=2, max_digits=5)),
                ('nox_emitido', models.DecimalField(decimal_places=2, max_digits=5)),
                ('obd_funciona', models.BooleanField()),
                ('aprobada', models.BooleanField()),
                ('normativa_aplicada', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tasks.normativa')),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.vehiculo')),
            ],
        ),
    ]
