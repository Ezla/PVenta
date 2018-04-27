from django.contrib import admin
from .models import Provider, ForeignInvoice, Payment

admin.site.register(Provider)
admin.site.register(ForeignInvoice)
admin.site.register(Payment)
