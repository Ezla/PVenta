from rest_framework import viewsets

from .serializers import InvoiceSerializer
from .models import ForeignInvoice


class InvoiceApiView(viewsets.ModelViewSet):
    queryset = ForeignInvoice.objects.all()
    serializer_class = InvoiceSerializer
