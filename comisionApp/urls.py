from django.urls import path
from . import views

urlpatterns = [
    path('alta_trasnporte/', views.altaTrasnporte, name='alta_trasnporte'),
    path('listar_ciudades/', views.listarCiudades, name='ciudades'),
    path('listar_transportes/', views.listarTransportes, name='transportes'),
    path('editar_transporte/<int:id>', views.editarTransporte, name='edit_transporte'),
    path('eliminar_transporte/<int:id>', views.eliminarTransporte, name='eliminar_transporte'),
]