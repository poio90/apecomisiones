from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from registro import views

urlpatterns = [

    path(route='login/',
         view=views.LoginUsuario.as_view(),
         name='login'),

    path(route='register/',
         view=views.RegistroUsuario.as_view(),
         name='register'),


    path(route='logout',
         view=login_required(views.LogoutUsuario.as_view()),
         name='logout'),

    path(route='password_reset',
         view=views.PasswordReset.as_view(),
         name='password_reset'),

    path(route='reset/<uidb64>/<token>/',
         view=views.PasswordResetConfirm.as_view(),
         name='password_reset_confirm'),

]
