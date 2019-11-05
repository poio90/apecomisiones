from django.contrib import admin
from .models import Agente, Ciudad, Transporte

# Register your models here.

admin.site.register(Agente)
admin.site.register(Ciudad)
admin.site.register(Transporte)
