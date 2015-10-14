from django.shortcuts import render
from django.views.generic import ListView, DetailView

from Apps.Venta.views import LoginRequiredMixin
from Apps.Venta.models import Venta, Cuenta


class Venta_Lista(LoginRequiredMixin, ListView):
    model = Cuenta
    paginate_by = 50
    template_name = 'Estadistica/venta_list.html'

    def get_context_data(self, **kwargs):
        context = super(Venta_Lista, self).get_context_data(**kwargs)
        context['total_ventas'] = Cuenta.objects.count()
        return context


class Venta_Consultar(LoginRequiredMixin, DetailView):
    model = Cuenta
    template_name = 'Estadistica/venta_detail.html'

    def get_context_data(self, **kwargs):
        context = super(Venta_Consultar, self).get_context_data(**kwargs)
        context['Venta_producto'] = Venta.objects.filter(cuenta = self.object)
        return context