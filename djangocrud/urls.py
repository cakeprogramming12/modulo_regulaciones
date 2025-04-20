
from django.contrib import admin
from django.urls import path
from tasks import views 

urlpatterns = [
    path('', views.index, name='index'),  
    path('admin/', admin.site.urls),
    #(paguina,funcion leer)
    path('nueva-normativa/', views.nueva_normativa, name='nueva_normativa'),      
    path('editar-normativa/<int:pk>/', views.editar_normativa, name='editar_normativa'),
    path('eliminar-normativa/<int:pk>/', views.eliminar_normativa, name='eliminar_normativa'),
    path('listar_normativas/', views.listar_normativas, name='listar_normativas'),
]


