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
    template_name = 'licencia.html'
    success_url = reverse_lazy('comisiones:historico_anticipo')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super(LicenciaSolicitud, self).form_valid(form)

"""class HistoricoAnticipos(ListView):
    model = Anticipo
    context_object_name = 'anticipos'
    template_name = 'public/historico.html'

    def get_queryset(self):
        return Anticipo.objects.filter(integrantes_x_anticipo__user=self.request.user.id)"""