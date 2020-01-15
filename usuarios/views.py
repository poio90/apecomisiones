from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import View, FormView, UpdateView, CreateView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from .forms import FormularioLogin, AgenteForm, FormularioRegistro


class Inicio(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

# Validaciones


def validar_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Ya existe un usuario con este nombre de usuario.'
    return JsonResponse(data)


def registroUsuario(request):
    if request.method == 'POST':
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.num_afiliado = form.cleaned_data.get('num_afiliado')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('perfil_agente')
        else:
            messages.error(
                request, ('Por favor corrija el error a continuación.'))
    else:
        form = FormularioRegistro()
    return render(request, 'registroUser.html', {'form': form})


class Login(FormView):
    template_name = 'login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('index')

    # medidas de seguridad
    @method_decorator(csrf_protect)  # evita bulneravilidades comunes
    # no se almacena en cache la informacion correspondiente
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    # llega el formulario y antes de llamar al metodo POST pasa por form_valid y se valida lo que deseamos
    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)


def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('accounts/login/')


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        agente_form = AgenteForm(request.POST, instance=request.user.afiliado)
        if agente_form.is_valid():
            agente_form.save()
            messages.success(request, ('Su perfil fue actualizado con éxito!'))
            return redirect('perfil_agente')
        else:
            messages.error(
                request, ('Por favor corrija el error a continuación.'))
    else:
        agente_form = AgenteForm(instance=request.user.afiliado)
    return render(request, 'profile.html', {
        'agente_form': agente_form
    })


@login_required
@transaction.atomic
def confeccionComision(request):
    return render(request, 'confeccion_comision.html')


@login_required
@transaction.atomic
def confeccionSolicitudComision(request):
    return render(request, 'confeccion_sol_comision.html')
