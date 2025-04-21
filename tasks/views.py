from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Normativa
from django.utils.dateparse import parse_date

#Paguina principal
def index(request):
    return render(request, 'principalRegulaciones.html')
    

#listar normativas
def listar_normativas(request):
    # Puedes agregar filtros aquí si quieres más adelante
    normativas = Normativa.objects.all().order_by('-vigente_desde')  # ordenadas por fecha de inicio
    return render(request, 'listar_normativas.html', {'normativas': normativas})

# Crear nueva normativa
def nueva_normativa(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        tipo_combustible = request.POST.get('tipo_combustible')
        limite_co = request.POST.get('limite_co')
        limite_nox = request.POST.get('limite_nox')
        usa_obd = request.POST.get('usa_obd') == '1'
        frecuencia_meses = request.POST.get('frecuencia_meses')
        vigente_desde = request.POST.get('vigente_desde')
        vigente_hasta = request.POST.get('vigente_hasta') or None

        # Crear la normativa
        Normativa.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            tipo_combustible=tipo_combustible,
            limite_co=limite_co,
            limite_nox=limite_nox,
            usa_obd=usa_obd,
            frecuencia_meses=frecuencia_meses,
            vigente_desde=parse_date(vigente_desde),
            vigente_hasta=parse_date(vigente_hasta) if vigente_hasta else None,
        )

        return redirect('listar_normativas')  # Redirige después de guardar

    return render(request, 'nueva-normativa.html')  # Renderiza el HTML que ya tienes


#editar normativa
def editar_normativa(request, pk):
    normativa = get_object_or_404(Normativa, pk=pk)

    if request.method == 'POST':
        normativa.nombre = request.POST.get('nombre')
        normativa.descripcion = request.POST.get('descripcion')
        normativa.tipo_combustible = request.POST.get('tipo_combustible')
        normativa.limite_co = request.POST.get('limite_co')
        normativa.limite_nox = request.POST.get('limite_nox')
        normativa.usa_obd = bool(int(request.POST.get('usa_obd')))
        normativa.frecuencia_meses = request.POST.get('frecuencia_meses')
        normativa.vigente_desde = request.POST.get('vigente_desde')
        normativa.vigente_hasta = request.POST.get('vigente_hasta') or None
        normativa.save()
        return redirect('listar_normativas')

    return render(request, 'editar_normativa.html', {'normativa': normativa})

#Eliminar norma
def eliminar_normativa(request, pk):
    normativa = get_object_or_404(Normativa, pk=pk)

    if request.method == 'POST':
        normativa.delete()
        return redirect('listar_normativas')

    return render(request, 'eliminar_normativa.html', {'normativa': normativa})


#reportes
def reportes(request):
    return render(request, 'reportes.html')