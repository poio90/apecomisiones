from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.decorators import login_required
from usuarios.views import Inicio, Login, logoutUsuario, update_profile


urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path('admin/', admin.site.urls),
    path('', login_required(Inicio.as_view()), name='index'),
    path('accounts/login/', Login.as_view(), name='login'),
    path('logout',login_required(logoutUsuario), name='logout'),
    path('perfil_agente',login_required(update_profile), name='perfil_agente'),
]
