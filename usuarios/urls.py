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
         view=login_required(views.LogoutUsuario.as_view()),
         name='logout'),

    path(route='',
         view=login_required(views.Inicio.as_view()),
         name='index'),

    path(route='usuario/<pk>/perfil/editar',
         view=login_required(views.EditarPerfil.as_view()),
         name='editar_perfil'),

    path(route='usuario/<pk>/perfil/',
         view=login_required(views.Perfil.as_view()),
         name='perfil'),
]
