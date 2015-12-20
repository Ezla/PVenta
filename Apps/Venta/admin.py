from django.contrib import admin

from .models import Cuenta, Venta


class CuentaAdmin(admin.ModelAdmin):
    list_display = ('tiket', 'total', 'efectivo', 'cambio', 'creado', 'modificado')
    search_fields = ('tiket',)


class VentaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'descuento', 'precio', 'cantidad', 'subtotal', 'cuenta')


admin.site.register(Cuenta, CuentaAdmin)
admin.site.register(Venta, VentaAdmin)
