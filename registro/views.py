from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, logout, authenticate, views as auth_views
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.views import (
    LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView )
from django.contrib.auth.decorators import login_required
from .forms import FormLogin, FormRegistro
from usuarios.models import User
from django.contrib.messages.views import SuccessMessageMixin


class LoginUsuario(FormView):
    template_name = 'registro/login.html'
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
        return reverse_lazy('usuarios:index')


class RegistroUsuario(SuccessMessageMixin, CreateView):
    model = User
    form_class = FormRegistro
    template_name = 'registro/registroUser.html'
    success_message = "Su registro se ha completado con éxito, inicie sesión para continuar"
    success_url = reverse_lazy('registro:login')


class LogoutUsuario(LogoutView):
    next_page = 'login/'


class PasswordReset(PasswordResetView):
    """
    Metodo sobreescrito para que aplique los estilos
    """
    template_name = 'registration/password_reset_form.html'
    html_email_template_name = 'registration/html_password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    #email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(PasswordReset, self).get_form(form_class)
        form.fields['email'].widget.attrs['class'] = 'form-control'
        form.fields['email'].widget.attrs['placeholder'] = 'Email'
        return form


class PasswordResetConfirm(PasswordResetConfirmView):
    """
    Metodo sobreescrito para que aplique los estilos
    """

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(PasswordResetConfirm, self).get_form(form_class)
        form.fields['new_password1'].widget.attrs['class'] = 'form-control'
        form.fields['new_password2'].widget.attrs['class'] = 'form-control'
        form.fields['new_password1'].widget.attrs['placeholder'] = 'Contraseña'
        form.fields['new_password2'].widget.attrs['placeholder'] = 'Confirmar contraseña'
        return form
