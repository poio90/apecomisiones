from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import View, FormView, UpdateView, CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import FormularioLogin, UserForm, AgenteForm

class Inicio(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

class Login(FormView):
    template_name = 'login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('index')

    #medidas de seguridad
    @method_decorator(csrf_protect) #evita bulneravilidades comunes
    @method_decorator(never_cache) #no se almacena en cache la informacion correspondiente
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    #llega el formulario y antes de llamar al metodo POST pasa por form_valid y se valida lo que deseamos
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
        user_form = UserForm(request.POST, instance=request.user)
        agente_form = AgenteForm(request.POST, instance=request.user.agente)
        if user_form.is_valid() and agente_form.is_valid():
            user_form.save()
            agente_form.save()
            messages.success(request, ('Su perfil fue actualizado con éxito!'))
            return redirect('perfil_agente')
        else:
            messages.error(request, ('Por favor corrija el error a continuación.'))
    else:
        user_form = UserForm(instance=request.user)
        agente_form = AgenteForm(instance=request.user.agente)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'agente_form': agente_form
    })