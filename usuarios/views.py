from django.db import transaction
from django.db.utils import IntegrityError
from django.shortcuts import render, redirect
from usuarios.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import View, FormView, UpdateView, CreateView, TemplateResponseMixin
from django.views.generic import DetailView, TemplateView
from django.contrib.auth import login, logout, authenticate, views as auth_views
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from .forms import FormLogin, FormRegistro, FormUpdateProfile


class Inicio(TemplateView):
    template_name = 'index.html'


class Perfil(DetailView):
    model = User
    template_name = 'profile.html'


class EditarPerfil(UpdateView):
    model = User
    form_class = FormUpdateProfile
    context_object_name = 'usuario'
    template_name = 'profile_edit.html'

    def get_success_url(self):
        # if you are passing 'pk' from 'urls' to 'UpdateView' for user
        # capture that 'pk' as user_pk and pass it to 'reverse_lazy()' function
        user_pk = self.request.user.pk
        return reverse_lazy('usuarios:perfil', kwargs={'pk': user_pk})


class LoginUsuario(FormView):
    template_name = 'login.html'
    form_class = FormLogin

    # medidas de seguridad
    @method_decorator(csrf_protect)  # evita bulneravilidades comunes
    # no se almacena en cache la informacion correspondiente
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(LoginUsuario, self).dispatch(request, *args, **kwargs)

    # llega el formulario y antes de llamar al metodo POST pasa por form_valid y se valida lo que deseamos
    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginUsuario, self).form_valid(form)

    def get_success_url(self):
        # if you are passing 'pk' from 'urls' to 'UpdateView' for user
        # capture that 'pk' as user_pk and pass it to 'reverse_lazy()' function
        user_pk = self.request.user.pk
        return reverse_lazy('usuarios:perfil', kwargs={'pk': user_pk})


def registroUsuario(request):
    if request.method == 'POST':
        dni = request.POST['dni']
        username = request.POST['username']
        passw = request.POST['password']
        passw_confirmation = request.POST['password_confirmation']
        num_afil = request.POST['num_afiliado']

        num_afiliado_taken = User.objects.filter(
            num_afiliado=num_afil).exists()
        if num_afiliado_taken:
            return render(request, 'registroUser.html', {'error': 'Ya existe un usuario con este número de afiliado.'})

        dni_taken = User.objects.filter(
            dni=dni).exists()
        if dni_taken:
            return render(request, 'registroUser.html', {'error': 'Ya existe un usuario con este número de documento.'})

        if passw != passw_confirmation:
            return render(request, 'registroUser.html', {'error': 'No coincide la contraseña'})

        try:
            user = User.objects.create_user(
                username=username, num_afiliado=num_afil, dni=dni, password=passw)
        except IntegrityError:
            return render(request, 'registroUser.html', {'error': 'Ya existe un usuario con este nombre de usuario.'})

        user.save()

        return redirect('usuarios:login')

    return render(request, 'registroUser.html')


class LogoutUsuario(LogoutView):
    next_page = 'accounts/login/'
