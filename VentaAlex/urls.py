from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers

from Apps.Producto.api_views import ProductoApiView, BrandApiView

router = routers.DefaultRouter()
router.register(r'product', ProductoApiView, base_name='api_product')
router.register(r'brand', BrandApiView, base_name='api_brand')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('Apps.Venta.urls', namespace='Venta')),
    url(r'^', include('Apps.Producto.urls', namespace='Producto')),
    url(r'^', include('Apps.Estadistica.urls', namespace='Estadistica')),
    url(r'^', include('Apps.Perfil.urls', namespace='PerfilUsuario')),
    url(r'^api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
