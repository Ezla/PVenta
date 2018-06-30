from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from datetime import datetime
from Apps.Venta.views import LoginRequiredMixin
from Apps.Venta.models import Venta, Cuenta
from .models import ForeignInvoice


class VentaLista(LoginRequiredMixin, ListView):
    model = Cuenta
    paginate_by = 50
    template_name = 'Estadistica/venta_list.html'

    def get_context_data(self, **kwargs):
        context = super(VentaLista, self).get_context_data(**kwargs)
        context['total_ventas'] = Cuenta.objects.count()
        return context


class VentaConsultar(LoginRequiredMixin, DetailView):
    model = Cuenta
    template_name = 'Estadistica/venta_detail.html'

    def get_context_data(self, **kwargs):
        context = super(VentaConsultar, self).get_context_data(**kwargs)
        context['Venta_producto'] = Venta.objects.filter(cuenta=self.object)
        return context


class VentaDemo(ListView):
    template_name = 'Estadistica/compras_list.html'
    queryset = Cuenta.objects.filter(creado__range=('2015-10-01','2015-11-01'))
    # queryset = Cuenta.objects.all()2015-11-09 05:04:47.821000


class InvoiceList(TemplateView):
    template_name = 'Estadistica/invoice_app.html'

    def get_context_data(self, **kwargs):
        context = super(InvoiceList, self).get_context_data(**kwargs)
        context['count_invoices'] = ForeignInvoice.objects.count()
        return context