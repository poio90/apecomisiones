from django.shortcuts import render
from django.views.generic import View, CreateView, DeleteView, ListView, TemplateView
from .models import *

# Create your views here.
class LicenciaSolicitud(TemplateView):
    template_name = 'licencia.html'

class EliminarAnticipo(DeleteView):
    model = Anticipo
    context_object_name = 'anticipo'
    template_name = 'eliminar_anticipo.html'
    success_url = reverse_lazy('comisiones:historico_anticipo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'Anticipo'
        context['list_url'] = reverse_lazy('comisiones:historico_anticipo')
        return context


class HistoricoAnticipos(ListView):
    model = Anticipo
    context_object_name = 'anticipos'
    template_name = 'public/historico.html'

    def get_queryset(self):
        return Anticipo.objects.filter(integrantes_x_anticipo__user=self.request.user.id)