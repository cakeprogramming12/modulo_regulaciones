
from django.contrib import admin
from django.urls import path
from tasks import views 

urlpatterns = [
    path('', views.index, name='index'),  

    # Admin
    path('admin/', admin.site.urls),

    # Normativas
    path('nueva-normativa/', views.nueva_normativa, name='nueva_normativa'),      
    path('editar-normativa/<int:pk>/', views.editar_normativa, name='editar_normativa'),
    path('eliminar-normativa/<int:pk>/', views.eliminar_normativa, name='eliminar_normativa'),
    path('listar_normativas/', views.listar_normativas, name='listar_normativas'),

    # Reportes
    path('reportes/', views.reportes, name='reportes'),
    path('reporte_aprobados/', views.reporte_vehiculos_aprobados, name='reporte_aprobados'),
    path('reporte_rechazados/', views.reporte_vehiculos_rechazados, name='reporte_rechazados'),


    # Verificación vehicular
    path('verificacion/', views.verificacion_vehicular, name='verificacion_vehicular'),
]
