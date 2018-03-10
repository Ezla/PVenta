from django.conf.urls import url

from .views import VentaLista, VentaConsultar, VentaDemo

app_name = 'Estadistica'
urlpatterns = [
    url(r'^Ventas/Lista/(?P<pk>\d+)/$', VentaLista.as_view(),
        name='url_lista'),
    url(r'^Ventas/Consultar/(?P<pk>\d+)/$', VentaConsultar.as_view(),
        name='url_consultar'),
    url(r'^Demo/$', VentaDemo.as_view(), name='url_demo'),
]
