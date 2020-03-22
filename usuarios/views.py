from django.db import transaction
from django.db.utils import IntegrityError
from django.shortcuts import render, redirect
from usuarios.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import View, FormView, UpdateView, CreateView, TemplateResponseMixin
from django.views.generic import DetailView
from django.contrib.auth import login, logout, authenticate, views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from .forms import FormLogin, FormRegistro, FormUpdateProfile


class Inicio(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class LoginUsuario(FormView):
    template_name = 'login.html'
    form_class = FormLogin
    success_url = reverse_lazy('usuarios:index')

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
            user = User.objects.create_user(username=username, num_afiliado=num_afil,dni=dni,password=passw)
        except IntegrityError:
            return render(request, 'registroUser.html', {'error': 'Ya existe un usuario con este nombre de usuario.'})

        user.save()

        return redirect('usuarios:login')

    return render(request, 'registroUser.html')


@login_required
def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('accounts/login/')


"""class PerfilUsuario(DetailView):
    template_name = 'profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = User.objects.all()"""


@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        afiliado_form = FormUpdateProfile(request.POST)
        if afiliado_form.is_valid():
            data = afiliado_form.cleaned_data
            user.last_name = data['last_name']
            user.first_name = data['first_name']
            user.email = data['email']
            user.dni = data['dni']
            user.num_tel = data['num_tel']
            user.save()
            redirect('usuarios:update_profile')
    else:
        afiliado_form = FormUpdateProfile()

    return render(request=request, template_name='profile.html', context={
        'user': request.user,
        'afiliado_form': afiliado_form
    })

@login_required
@transaction.atomic
def confeccionComision(request):
    return render(request, 'confeccion_comision.html')


@login_required
@transaction.atomic
def confeccionSolicitudComision(request):
    return render(request, 'confeccion_sol_comision.html')
"""

# ------------------------------Validaciones----------------------------------------#


def validar_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Ya existe un usuario con este nombre de usuario.'
    return JsonResponse(data)


def validar_afiliado(request):
    num_afiliado = request.GET.get('num_afiliado', None)
    data = {
        'is_taken': Afiliado.objects.filter(num_afiliado__iexact=num_afiliado).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Ya existe un usuario con este número de afiliado.'
    return JsonResponse(data)


def validar_dni(request):
    dni = request.GET.get('dni', None)
    data = {
        'is_taken': Afiliado.objects.filter(dni__iexact=dni).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Ya existe un usuario con este número de documento.'
    return JsonResponse(data)
#----------------------------------------------------------------------------------------#


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
            return redirect('usuarios:perfil_agente')
        else:
            messages.error(
                request, ('Por favor corrija el error a continuación.'))
    else:
        form = FormularioRegistro()
    return render(request, 'registroUser.html', {'form': form})


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        dni = request.POST.get('dni', None)
        data = {
            'is_taken': Afiliado.objects.filter(dni__iexact=dni).exists()
        }
        if data['is_taken']:
            data['error_message'] = 'Ya existe un usuario con este número de documento.'
        else:
            agente_form = AgenteForm(
                request.POST, instance=request.user.afiliado)
            if agente_form.is_valid():
                agente_form.save()
                data['success_message'] = 'Su perfil fue actualizado con éxito!'
        return JsonResponse(data)
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
    return render(request, 'confeccion_sol_comision.html')"""
