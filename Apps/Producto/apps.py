from django.apps import AppConfig


class ProductoAppConfig(AppConfig):
    name = 'Apps.Producto'

    def ready(self):
        import Apps.Producto.signals
