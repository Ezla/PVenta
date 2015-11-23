from django.core.urlresolvers import reverse_lazy


def menu(request):
    menu = {
        'Venta':{'/Venta/'},
        'Producto':{

        },
        'Marca':{},
        'Estadisticas':{},
        'Usuario':{}
    }
    x = request.path.split('/')
    x.pop()
    x.pop(0)
    return {'breadcrumb': {
        'nombre': 'Venta',
        'url': reverse_lazy('Venta:url_venta'),
    }}
