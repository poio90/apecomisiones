from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls',
                                   'jet-dashboard')),  # Django JET dashboard URLS
    path('admin/', admin.site.urls),
    path('',include(('usuarios.urls','usuarios'), namespace='usuarios')),
    path('',include(('comisionApp.urls','comisiones'), namespace='comisiones')),
    path('',include(('licencias.urls','licencias'), namespace='licencias')),
]