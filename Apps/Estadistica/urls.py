from django.conf.urls import patterns, url

from .views import Venta_Lista, Venta_Consultar


urlpatterns = patterns('',
        url(r'^Ventas/Lista/(?P<pk>\d+)/$', Venta_Lista.as_view(), name="url_lista"),
        url(r'^Ventas/Consultar/(?P<pk>\d+)/$', Venta_Consultar.as_view(), name='url_consultar'),
)
