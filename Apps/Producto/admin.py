from django.contrib import admin

from .models import Producto, Marca


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion', 'marca', 'punitario', 'pmayoreo', 'inventario', 'cantidad', 'minimo')


admin.site.register(Producto, ProductoAdmin)
admin.site.register(Marca)
