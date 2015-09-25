from django.conf.urls import patterns, url


from .views import Venta_Demo, Login, Logout, Venta, Venta_Buscar_Producto, Venta_Remover_Prod, Venta_Cancelar_Cuenta, Venta_Aumentar_Prod,  Venta_Pagar_Cuenta, Venta_Tiket, Venta_Tipo_Precio

urlpatterns = patterns('',
    url(r'^$', Login.as_view(), name='url_index'),
    url(r'^Logout/$', Logout.as_view(), name='url_logout'),
    url(r'^Venta/$', Venta.as_view(), name='url_venta'),
    url(r'^Pagar/$', Venta_Pagar_Cuenta.as_view(), name='url_pagar'),
    url(r'^Tiket/$', Venta_Tiket.as_view(), name='url_tiket'),
    url(r'^Ajax/Buscar/$', Venta_Buscar_Producto.as_view(), name="url_buscar_ajax"),
    url(r'^Ajax/Remover/$', Venta_Remover_Prod.as_view(), name='url_remover_prod_ajax'),
    url(r'^Ajax/Aumentar/$', Venta_Aumentar_Prod.as_view(), name='url_aumentar_prod_ajax'),
    url(r'^Ajax/Precio/$', Venta_Tipo_Precio.as_view(), name='url_tipo_precio_ajax'),
    url(r'^Ajax/Cancelar/$', Venta_Cancelar_Cuenta.as_view(), name='url_cancelar_cuenta_ajax'),
    url(r'^Demo/$', Venta_Demo),
)
