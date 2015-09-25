from django.conf.urls import patterns, url

from .views import Producto_Nuevo, Producto_Lista, Producto_Actualizar, Producto_Eliminar, Producto_Consultar, Marca_Nuevo, Marca_Lista, Marca_Actualizar, Marca_Eliminar, Marca_Nuevo_Ajax, Code_Imagen


urlpatterns = patterns('',
    url(r'^Producto/Nuevo/$', Producto_Nuevo.as_view(), name="url_nuevo"),
    url(r'^Producto/Lista/(?P<pk>\d+)/$', Producto_Lista.as_view(), name="url_lista"),
    url(r'^Producto/Actualizar/(?P<pk>\d+)/$', Producto_Actualizar.as_view(), name='url_actualizar'),
    url(r'^Producto/Eliminar/(?P<pk>\d+)/$', Producto_Eliminar.as_view(), name='url_eliminar'),
    url(r'^Producto/Consultar/(?P<pk>\d+)/$', Producto_Consultar.as_view(), name='url_consultar'),
    url(r'^Marca/Nuevo/$', Marca_Nuevo.as_view(), name='url_nueva_marca'),
    url(r'^Marca/Lista/(?P<pk>\d+)/$', Marca_Lista.as_view(), name='url_lista_marca'),
    url(r'^Marca/Actualizar/(?P<pk>\d+)/$', Marca_Actualizar.as_view(), name='url_actualizar_marca'),
    url(r'^Marca/Eliminar/(?P<pk>\d+)/$', Marca_Eliminar.as_view(), name='url_eliminar_marca'),
    url(r'^Ajax/Marca/Nuevo/$', Marca_Nuevo_Ajax.as_view(), name="url_marca_ajax"),
    url(r'^Codigo/PNG/$', Code_Imagen.as_view(), name="url_codigo_png"),
)
