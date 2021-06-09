from django.contrib import admin
from .models import Provider, ForeignInvoice, Payment


class ForeignInvoiceAdmin(admin.ModelAdmin):
    list_display = (
    'folio', 'provider', 'amount', 'discount', 'discount_applied',
    'status', 'invoice_date', 'settlement_date')


admin.site.register(Provider)
admin.site.register(ForeignInvoice, ForeignInvoiceAdmin)
admin.site.register(Payment)
