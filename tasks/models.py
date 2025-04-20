from django.db import models


 # Tabla de normativas
class Normativa(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    tipo_combustible = models.CharField(max_length=20, choices=[
        ('Gasolina', 'Gasolina'),
        ('Diésel', 'Diésel'),
        ('Eléctrico', 'Eléctrico'),
        ('Híbrido', 'Híbrido'),
    ])
    limite_co = models.DecimalField(max_digits=5, decimal_places=2)
    limite_nox = models.DecimalField(max_digits=5, decimal_places=2)
    usa_obd = models.BooleanField()
    frecuencia_meses = models.PositiveIntegerField()
    vigente_desde = models.DateField()
    vigente_hasta = models.DateField(null=True, blank=True)
