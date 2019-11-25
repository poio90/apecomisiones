from django.urls import path
from .views import home,listarComisiones

urlpatterns = [
    path('', home, name='index'),
    path('', listarComisiones, name='listarComisiones'),
]