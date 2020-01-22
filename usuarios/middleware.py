from django.shortcuts import redirect
from django.urls import reverse


class PerfilCompletoMiddlerware:
    def __init__(self, get_response):
        """Middlerware de inicializacion"""
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if not request.user.is_anonymous:
            user = request.user
            afiliado = request.user.afiliado
            if not user.last_name or not user.first_name or not afiliado.dni or not afiliado.num_tel:
                if request.path not in [reverse('usuarios:update_profile'), reverse('usuarios:logout')]:
                    return redirect('usuarios:update_profile')

        response = self.get_response(request)
        return response
