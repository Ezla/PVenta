from django.conf.urls import url
from django.urls import path

from .api_views import ProductExistsView, ProductSearchSuggestionsView
from .views import ProductoNuevo, ProductoLista, ProductoActualizar, \
    ProductoEliminar, ProductoConsultar, MarcaNuevo, MarcaLista, \
    MarcaActualizar, MarcaEliminar, MarcaNuevoAjax, CodeImagen, \
    GetNotifications, DeleteNotifications, LookNotifications, StatusBar, \
    GenerateBarcodeView

app_name = 'Producto'
urlpatterns = [
    url(r'^Producto/Nuevo/$', ProductoNuevo.as_view(), name='url_nuevo'),
    url(r'^Producto/Lista/(?P<pk>\d+)/$', ProductoLista.as_view(),
        name='url_lista'),
    url(r'^Producto/Actualizar/(?P<pk>\d+)/$', ProductoActualizar.as_view(),
        name='url_actualizar'),
    url(r'^Producto/Eliminar/(?P<pk>\d+)/$', ProductoEliminar.as_view(),
        name='url_eliminar'),
    url(r'^Producto/Consultar/(?P<pk>\d+)/$', ProductoConsultar.as_view(),
        name='url_consultar'),
    url(r'^Marca/Nuevo/$', MarcaNuevo.as_view(), name='url_nueva_marca'),
    url(r'^Marca/Lista/(?P<pk>\d+)/$', MarcaLista.as_view(),
        name='url_lista_marca'),
    url(r'^Marca/Actualizar/(?P<pk>\d+)/$', MarcaActualizar.as_view(),
        name='url_actualizar_marca'),
    url(r'^Marca/Eliminar/(?P<pk>\d+)/$', MarcaEliminar.as_view(),
        name='url_eliminar_marca'),
    url(r'^Ajax/Marca/Nuevo/$', MarcaNuevoAjax.as_view(),
        name='url_marca_ajax'),
    url(r'^Codigo/PNG/$', CodeImagen.as_view(), name='url_codigo_png'),
    url(r'^Notification/get/$', GetNotifications.as_view(),
        name='url_get_notificaciones'),
    url(r'^Notification/delete/$', DeleteNotifications.as_view(),
        name='url_delete_notificaciones'),
    url(r'^Notification/look/$', LookNotifications.as_view(),
        name='url_look_notificaciones'),
    url(r'^Status/bar/$', StatusBar.as_view(), name='url_status_bar'),
    url(r'^api/search/product/(?P<code>[0-9]+)/$', ProductExistsView.as_view()),
    path('api/search/products/<str:word>/', ProductSearchSuggestionsView.as_view()),
    path('products/barcode/', GenerateBarcodeView.as_view(), name='url_generate_barcodes'),
]
