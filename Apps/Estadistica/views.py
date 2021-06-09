from django.views.generic import ListView, DetailView, TemplateView
from Apps.Venta.views import LoginRequiredMixin
from Apps.Venta.models import SalesProduct, SalesAccount
from .models import ForeignInvoice


class VentaLista(LoginRequiredMixin, ListView):
    model = SalesAccount
    paginate_by = 50
    template_name = 'Estadistica/venta_list.html'

    def get_context_data(self, **kwargs):
        context = super(VentaLista, self).get_context_data(**kwargs)
        context['total_ventas'] = SalesAccount.objects.count()
        return context


class VentaConsultar(LoginRequiredMixin, DetailView):
    model = SalesAccount
    template_name = 'Estadistica/venta_detail.html'

    def get_context_data(self, **kwargs):
        context = super(VentaConsultar, self).get_context_data(**kwargs)
        context['Venta_producto'] = SalesProduct.objects.filter(
            sales_account=self.object)
        return context


class VentaDemo(ListView):
    template_name = 'Estadistica/compras_list.html'
    queryset = SalesAccount.objects.filter(
        created__range=('2015-10-01', '2015-11-01'))


class InvoiceList(TemplateView):
    template_name = 'Estadistica/invoice_app.html'

    def get_context_data(self, **kwargs):
        context = super(InvoiceList, self).get_context_data(**kwargs)
        context['count_invoices'] = ForeignInvoice.objects.count()
        return context
