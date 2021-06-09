from django.contrib import admin

from .models import SalesAccount, SalesProduct, Discount


class SalesAccountAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'subtotal', 'cash', 'change_due',
                    'created', 'modified')
    search_fields = ('ticket',)


class SalesProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'with_discount', 'price',
                    'quantity', 'sales_account')


admin.site.register(SalesAccount, SalesAccountAdmin)
admin.site.register(SalesProduct, SalesProductAdmin)
admin.site.register(Discount)
