from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500
from comisionApp.views import Error404View, Error500View

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls',
                                   'jet-dashboard')),  # Django JET dashboard URLS
    path('admin/', admin.site.urls),
    path('', include(('usuarios.urls', 'usuarios'), namespace='usuarios')),
    path('', include(('comisionApp.urls', 'comisiones'), namespace='comisiones')),
    path('', include(('licencias.urls', 'licencias'), namespace='licencias')),
]

handler404 = Error404View.as_view()

handler500 = Error500View.as_error_view()