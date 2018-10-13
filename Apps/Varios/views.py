from django.views.generic import TemplateView
from Apps.Venta.views import LoginRequiredMixin


class ListedView(LoginRequiredMixin, TemplateView):
    template_name = 'varios/listed.html'
