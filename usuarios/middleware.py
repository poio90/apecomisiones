from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages


class PerfilCompletoMiddlerware:
    
    def __init__(self, get_response):
        """Middlerware de inicializacion"""
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if not request.user.is_anonymous:
            if not request.user.is_staff:
                user = request.user
                if not user.last_name or not user.first_name or not user.dni or not user.num_tel:
                    if request.path not in [reverse('usuarios:editar_perfil'), reverse('usuarios:logout')]:
                        messages.success(request,('Por favor complete su datos personales'))
                        return redirect('usuarios:editar_perfil')

        response = self.get_response(request)
        return response
