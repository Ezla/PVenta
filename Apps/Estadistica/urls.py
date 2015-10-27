from django.conf.urls import patterns, url

from .views import VentaLista, VentaConsultar

urlpatterns = patterns('',
                       url(r'^Ventas/Lista/(?P<pk>\d+)/$', VentaLista.as_view(), name="url_lista"),
                       url(r'^Ventas/Consultar/(?P<pk>\d+)/$', VentaConsultar.as_view(), name='url_consultar'),
                       )
