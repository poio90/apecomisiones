from django.urls import path
from django.contrib.auth.decorators import login_required
from usuarios import views

urlpatterns = [
    path(route='accounts/register/',
         view=views.registroUsuario,
         name='register'),

    path(route='accounts/login/',
         view=views.Login.as_view(),
         name='login'),

    path(route='logout',
         view=login_required(views.logoutUsuario),
         name='logout'),

    path(route='perfil_agente',
         view=login_required(views.update_profile),
         name='perfil_agente'),

    path('', login_required(views.Inicio.as_view()), name='index'),

    path('confeccion_comisión', login_required(
        views.confeccionComision), name='confeccion_comisión'),
    path('confeccion_solicitud_comisión', login_required(
        views.confeccionSolicitudComision), name='confeccion_solicitud_comisión'),
    path('ajax/validate_username/', views.validar_username, name='validate_username'),
    path('ajax/validate_afiliado/', views.validar_afiliado, name='validate_afiliado'),
    path('ajax/validate_dni/', views.validar_dni, name='validate_dni'),
]
