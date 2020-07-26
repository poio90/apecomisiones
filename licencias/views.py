from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, DeleteView, ListView, TemplateView
from .models import *
from .forms import FormLicencia

# Create your views here.


class LicenciaSolicitud(CreateView):
    model = Licencia
    form_class = FormLicencia
    context_object_name = 'licencia'
    template_name = 'licencias/licencia.html'
    success_url = reverse_lazy('licencias:licencias_historico')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super(LicenciaSolicitud, self).form_valid(form)


class HistoricoLicencias(ListView):
    model = Licencia
    context_object_name = 'licencias'
    template_name = 'licencias/historico_licencias.html'

    def get_queryset(self):
        return Licencia.objects.filter(user=self.request.user)


class EliminarLicencia(DeleteView):
    model = Licencia
    context_object_name = 'licencia'
    template_name = 'licencias/eliminar_licencia.html'
    success_url = reverse_lazy('licencias:licencias_historico')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'Licencia'
        context['list_url'] = reverse_lazy('licencias:licencias_historico')
        return context
