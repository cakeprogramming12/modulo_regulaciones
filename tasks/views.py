from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Normativa,Vehiculo,Verificacion
from django.utils.dateparse import parse_date
from django.db.models import Q
from datetime import date
from tasks import models
from django.shortcuts import render
from .models import Vehiculo, Normativa, Verificacion
from datetime import date
from django.db.models import Q
from decimal import Decimal

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


#Verfificacion
def verificacion_vehicular(request):
    resultado = None

    if 'placa' in request.GET:
        placa = request.GET['placa'].upper().strip()
        try:
            vehiculo = Vehiculo.objects.get(placa=placa)
            normativa = Normativa.objects.filter(
                tipo_combustible=vehiculo.tipo_combustible,
                vigente_desde__lte=date.today()
            ).filter(
                Q(vigente_hasta__gte=date.today()) | Q(vigente_hasta__isnull=True)
            ).first()

            if normativa:
                # Convertir los valores de co_medido y nox_medido a Decimal
                try:
                    co_medido = Decimal(request.GET.get('co_medido'))
                    nox_medido = Decimal(request.GET.get('nox_medido'))
                    obd_funciona = request.GET.get('obd_funciona') == 'true'
                except (ValueError, TypeError) as e:
                    resultado = f"⚠️ Error al procesar los valores de las emisiones: {e}"
                    return render(request, 'verificacion_vehicular.html', {'resultado': resultado})

                # Guardar las emisiones en el vehículo
                vehiculo.co_medido = co_medido
                vehiculo.nox_medido = nox_medido
                vehiculo.save()

                # Guardar los datos en la tabla de Verificacion
                verificacion = Verificacion.objects.create(
                    vehiculo=vehiculo,
                    co_emitido=co_medido,
                    nox_emitido=nox_medido,
                    obd_funciona=obd_funciona,
                    normativa_aplicada=normativa,
                    aprobada=False  # Esto se determinará según la comparación
                )

                # Comparar los valores de emisión con la normativa
                cumple = (
                    co_medido <= normativa.limite_co and
                    nox_medido <= normativa.limite_nox and
                    obd_funciona == normativa.usa_obd
                )
                # Actualizar si es aprobado o no
                verificacion.aprobada = cumple
                verificacion.save()

                resultado = '✅ Aprobado' if cumple else '❌ Rechazado'
            else:
                resultado = '⚠️ No hay normativa aplicable al vehículo.'
        except Vehiculo.DoesNotExist:
            resultado = '🚫 Vehículo no encontrado.'

    return render(request, 'verificacion_vehicular.html', {'resultado': resultado})




#VISTAS PARA REPORTES
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, mm   # <-- INCLUYE mm AQUÍ
from datetime import datetime
from .models import Verificacion
from django.contrib.staticfiles import finders

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, mm
from datetime import datetime
from .models import Verificacion
from django.contrib.staticfiles import finders

def reporte_vehiculos_aprobados(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="vehiculos_aprobados.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Agregar logo
    logo_path = finders.find('imagenes/logo-reporte.png')  # Asegúrate de que el logo esté bien encontrado
    if logo_path:
        logo = Image(logo_path)
        logo_width = 2*inch  # Puedes cambiar este valor a lo que prefieras
        logo_height = (logo.imageHeight / logo.imageWidth) * logo_width  # Mantiene la proporción
        logo.drawHeight = logo_height
        logo.drawWidth = logo_width
        logo.hAlign = 'LEFT'
        elements.append(logo)


    # Título
    title = Paragraph("Reporte de Vehículos Aprobados", styles['Title'])
    elements.append(title)

    # Fecha de generación
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    fecha_paragraph = Paragraph(f"Fecha de generación: {fecha}", styles['Normal'])
    elements.append(fecha_paragraph)

    elements.append(Spacer(1, 20))

    # Obtener datos
    verificaciones_aprobadas = Verificacion.objects.filter(aprobada=True)

    if not verificaciones_aprobadas.exists():
        no_data = Paragraph("No hay vehículos aprobados registrados.", styles['Normal'])
        elements.append(no_data)
    else:
        data = [['Placa', 'Marca', 'Modelo', 'Año']]

        for verificacion in verificaciones_aprobadas:
            vehiculo = verificacion.vehiculo
            data.append([vehiculo.placa, vehiculo.marca, vehiculo.modelo, vehiculo.anio])

        table = Table(data, hAlign='CENTER')
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#004aad')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 11),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),
        ]))

        elements.append(table)

    # Agregar número de página
    def agregar_numero_pagina(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        page_number_text = f"Página {doc.page}"
        canvas.drawRightString(200 * mm, 15 * mm, page_number_text)
        canvas.restoreState()

    doc.build(elements, onFirstPage=agregar_numero_pagina, onLaterPages=agregar_numero_pagina)

    return response


def reporte_vehiculos_rechazados(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="vehiculos_rechazados.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Agregar logo
    logo_path = finders.find('imagenes/logo-reporte.png')  # Asegúrate de que el logo esté bien encontrado
    if logo_path:
        logo = Image(logo_path)
        logo_width = 2*inch  # Puedes cambiar este valor a lo que prefieras
        logo_height = (logo.imageHeight / logo.imageWidth) * logo_width  # Mantiene la proporción
        logo.drawHeight = logo_height
        logo.drawWidth = logo_width
        logo.hAlign = 'LEFT'
        elements.append(logo)

    # Título
    title = Paragraph("Reporte de Vehículos Rechazados", styles['Title'])
    elements.append(title)

    # Fecha de generación
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    fecha_paragraph = Paragraph(f"Fecha de generación: {fecha}", styles['Normal'])
    elements.append(fecha_paragraph)

    elements.append(Spacer(1, 20))

    # Obtener datos
    verificaciones_rechazadas = Verificacion.objects.filter(aprobada=False)

    if not verificaciones_rechazadas.exists():
        no_data = Paragraph("No hay vehículos rechazados registrados.", styles['Normal'])
        elements.append(no_data)
    else:
        data = [['Placa', 'Marca', 'Modelo', 'Año']]

        for verificacion in verificaciones_rechazadas:
            vehiculo = verificacion.vehiculo
            data.append([vehiculo.placa, vehiculo.marca, vehiculo.modelo, vehiculo.anio])

        table = Table(data, hAlign='CENTER')
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#004aad')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 11),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),
        ]))

        elements.append(table)

    # Agregar número de página
    def agregar_numero_pagina(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        page_number_text = f"Página {doc.page}"
        canvas.drawRightString(200 * mm, 15 * mm, page_number_text)
        canvas.restoreState()

    doc.build(elements, onFirstPage=agregar_numero_pagina, onLaterPages=agregar_numero_pagina)

    return response
