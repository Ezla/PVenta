from django.conf.urls import url
from django.urls import path

from .views import Login, Logout, Venta, VentaBuscarProducto, \
    VentaRemoverProd, VentaCancelarCuenta, VentaAumentarProd, \
    VentaPagarCuenta, VentaTiket, VentaTipoPrecio, VentaSetDescuento
from .api_views import AccountView, SalesProductChangeView, SearchProductView, SalesCartStatusView

app_name = 'Venta'
urlpatterns = [
    url(r'^$', Login.as_view(), name='url_index'),
    url(r'^Logout/$', Logout.as_view(), name='url_logout'),
    url(r'^Venta/$', Venta.as_view(), name='url_venta'),
    url(r'^Pagar/$', VentaPagarCuenta.as_view(), name='url_pagar'),
    url(r'^Tiket/(?P<pk>\d+)/$', VentaTiket.as_view(), name='url_tiket'),
    url(r'^Ajax/Buscar/$', VentaBuscarProducto.as_view(),
        name='url_buscar_ajax'),
    url(r'^Ajax/Remover/$', VentaRemoverProd.as_view(),
        name='url_remover_prod_ajax'),
    url(r'^Ajax/Aumentar/$', VentaAumentarProd.as_view(),
        name='url_aumentar_prod_ajax'),
    url(r'^Ajax/Precio/$', VentaTipoPrecio.as_view(),
        name='url_tipo_precio_ajax'),
    url(r'^Ajax/Cancelar/$', VentaCancelarCuenta.as_view(),
        name='url_cancelar_cuenta_ajax'),
    url(r'^Ajax/Descuento/$', VentaSetDescuento.as_view(),
        name='url_agregar_descuento_ajax'),
    path('api/sales/pay/', AccountView.as_view(), name='url_cart_pay'),
    path('api/sales/product/change/', SalesProductChangeView.as_view(), name='url_change_product'),
    path('api/sales/product/search/', SearchProductView.as_view(), name='url_search_product'),
    path('api/sales/cart/status/', SalesCartStatusView.as_view(), name='url_cart_status'),
]
