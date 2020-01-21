from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from usuarios import views

urlpatterns = [

    path(route='accounts/login/',
         view=views.LoginUsuario.as_view(),
         name='login'),

    path(route='accounts/register/',
         view=views.RegistroUsuario.as_view(),
         name='register'),

    path(route='logout',
         view=views.logoutUsuario,
         name='logout'),

    path(route='',
         view=views.Inicio.as_view(),
         name='index'),

    path(route='perfil_usuario/<str:username>/',
         view=views.PerfilUsuario.as_view(template_name='profile.html'),
         name='perfil_agente'),
]

"""path(route='accounts/register/',
         view=views.registroUsuario,
         name='register'),

    path(route='logout',
         view=login_required(views.logoutUsuario),
         name='logout'),

    path(route='perfil_agente',
         view=login_required(views.update_profile),
         name='perfil_agente'),

    
    path('confeccion_comisión', login_required(
        views.confeccionComision), name='confeccion_comisión'),
    path('confeccion_solicitud_comisión', login_required(
        views.confeccionSolicitudComision), name='confeccion_solicitud_comisión'),
    path('ajax/validate_username/', views.validar_username, name='validate_username'),
    path('ajax/validate_afiliado/', views.validar_afiliado, name='validate_afiliado'),
    path('ajax/validate_dni/', views.validar_dni, name='validate_dni'),"""
