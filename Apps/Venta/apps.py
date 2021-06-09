from django.apps import AppConfig


class SaleAppConfig(AppConfig):
    name = 'Apps.Venta'

    def ready(self):
        import Apps.Venta.signals
