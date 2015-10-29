from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView, View

import barcode
from StringIO import StringIO

from .models import Producto, Marca
from .forms import CrearProductoForm, CrearMarcaForm
from Apps.Venta.views import LoginRequiredMixin
from Apps.Venta.logica import crear_code39


class ProductoNuevo(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = CrearProductoForm
    success_url = '/Producto/Lista/1/'

    def form_valid(self, form):
        x = form.save()
        if x.code39:
            cod = str(x.id)
            while len(cod) < 10:
                cod = '0' + cod
            x.codigo = cod
            x.save()
        return super(ProductoNuevo, self).form_valid(form)


class ProductoLista(LoginRequiredMixin, ListView):
    model = Producto
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(ProductoLista, self).get_context_data(**kwargs)
        total = Producto.objects.count()
        context['total_productos'] = total
        buscar = self.request.GET.get('buscar_prod')
        marca = self.request.GET.get('marca_prod')
        if buscar:
            context['encontrado_productos'] = Producto.objects.filter(descripcion__icontains=buscar).count()
        elif marca:
            context['encontrado_productos'] = Producto.objects.filter(marca__marca=marca).count()
        else:
            context['encontrado_productos'] = total
        return context

    def get_queryset(self):
        buscar = self.request.GET.get('buscar_prod')
        marca = self.request.GET.get('marca_prod')
        if buscar:
            return Producto.objects.filter(descripcion__icontains=buscar)
        elif marca:
            return Producto.objects.filter(marca__marca=marca)
        else:
            return Producto.objects.all()


class ProductoActualizar(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = CrearProductoForm
    success_url = '/Producto/Lista/1/'

    def form_valid(self, form):
        x = form.save()
        if x.code39:
            cod = str(x.id)
            while len(cod) < 10:
                cod = '0' + cod
            x.codigo = cod
            x.save()
        return super(ProductoActualizar, self).form_valid(form)


class ProductoEliminar(LoginRequiredMixin, DeleteView):
    model = Producto
    success_url = '/Producto/Lista/1/'


class ProductoConsultar(LoginRequiredMixin, DetailView):
    model = Producto


class ProductoBuscar(LoginRequiredMixin, ListView):
    model = Producto
    paginate_by = 50


class MarcaNuevo(LoginRequiredMixin, CreateView):
    model = Marca
    form_class = CrearMarcaForm
    success_url = '/Marca/Lista/1/'
    template_name = 'Producto/marca_form.html'


class MarcaLista(LoginRequiredMixin, ListView):
    model = Marca
    paginate_by = 50
    template_name = 'Producto/marca_list.html'

    def get_context_data(self, **kwargs):
        context = super(MarcaLista, self).get_context_data(**kwargs)
        total = Marca.objects.count()
        context['total_marcas'] = total
        buscar = self.request.GET.get('buscar_marca')
        if buscar:
            context['encontrado_marcas'] = Marca.objects.filter(marca__icontains=buscar).count()
        else:
            context['encontrado_marcas'] = total
        return context

    def get_queryset(self):
        buscar = self.request.GET.get('buscar_marca')
        if buscar:
            return Marca.objects.filter(marca__icontains=buscar)
        else:
            return Marca.objects.all()


class MarcaActualizar(LoginRequiredMixin, UpdateView):
    model = Marca
    form_class = CrearMarcaForm
    success_url = '/Marca/Lista/1/'
    template_name = 'Producto/marca_form.html'


class MarcaEliminar(LoginRequiredMixin, DeleteView):
    model = Marca
    success_url = '/Marca/Lista/1/'
    template_name = 'Producto/marca_confirm_delete.html'


class MarcaNuevoAjax(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        marca = request.GET['marca']
        m = CrearMarcaForm(request.GET)
        if m.is_valid():
            e = False
            m.save()
            mensaje = 'Nueva marca %s agregada' % marca
        else:
            e = True
            mensaje = m.errors
        marcas = Marca.objects.all()
        dic_marcas = []
        for x in marcas:
            dic_marcas.append({'id': x.id, 'marca': x.marca})
        data = JsonResponse({'Errores': e, 'Marcas': dic_marcas, 'mensaje': mensaje})
        # data = serializers.serialize('json', marcas)
        return HttpResponse(data, content_type='application/json')


class CodeImagen(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        fp = StringIO()
        code39 = barcode.generate('Code39', '123456789012', writer=barcode.writer.ImageWriter(), output=fp)
        # filename = code39.save('img')
        response = HttpResponse(code39, content_type='application/png')
        response['Content-Disposition'] = 'filename="img.png"'
        return response
