from django.db import models


 # Tabla de vehiculo
class Vehiculo(models.Model):
    placa = models.CharField(max_length=10)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.PositiveIntegerField()
    tipo_combustible = models.CharField(max_length=20, choices=[
        ('Gasolina', 'Gasolina'),
        ('Diésel', 'Diésel'),
        ('Eléctrico', 'Eléctrico'),
        ('Híbrido', 'Híbrido'),
    ])
    usa_obd = models.BooleanField()  # Si el vehículo tiene OBD
    co_medido = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Emisiones de CO
    nox_medido = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Emisiones de NOx

    def __str__(self):
        return self.placa

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


class Verificacion(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    co_emitido = models.DecimalField(max_digits=5, decimal_places=2)
    nox_emitido = models.DecimalField(max_digits=5, decimal_places=2)
    obd_funciona = models.BooleanField()
    normativa_aplicada = models.ForeignKey(Normativa, on_delete=models.PROTECT)
    aprobada = models.BooleanField()

    