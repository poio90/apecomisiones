from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView, View
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from .forms import FormularioLogin

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
