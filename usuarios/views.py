from django.db import transaction
from django.db.utils import IntegrityError
from django.shortcuts import render, redirect
from .models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import View, FormView, UpdateView, CreateView, TemplateResponseMixin
from django.views.generic import DetailView, TemplateView
from django.contrib.auth import login, logout, authenticate, views as auth_views
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from .forms import FormLogin, FormRegistro, FormUpdateProfile, UserForm
from comisionManager import settings


class Inicio(TemplateView):
    template_name = 'inicio.html'


class Perfil(DetailView):
    model = User
    template_name = 'usuarios/profile.html'

    def get_context_data(self, **kwargs):
        context = super(Perfil, self).get_context_data(**kwargs)
        context['form'] = UserForm(instance=self.object)
        return context


class EditarPerfil(SuccessMessageMixin, UpdateView):
    model = User
    form_class = FormUpdateProfile
    context_object_name = 'usuario'
    template_name = 'usuarios/profile_edit.html'
    success_message = "Su perfil se ha actualizado exitosamente"

    def get_success_url(self):
        # if you are passing 'pk' from 'urls' to 'UpdateView' for user
        # capture that 'pk' as user_pk and pass it to 'reverse_lazy()' function
        user_pk = self.request.user.pk
        return reverse_lazy('usuarios:perfil', kwargs={'pk': user_pk})


"""https://ccbv.co.uk/projects/Django/3.0/django.views.generic.edit/DeletionMixin/"""
