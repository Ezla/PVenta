from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.core import serializers
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView, View
import datetime
import barcode
from StringIO import StringIO

from .models import Producto, Marca
from .forms import CrearProductoForm, CrearMarcaForm
from Apps.Venta.views import LoginRequiredMixin
from Apps.Venta.logica import crear_code39, add_notif, status_bar


class ProductoNuevo(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = CrearProductoForm
    success_url = reverse_lazy('Producto:url_nuevo')
    template_name = 'Producto/producto_new.html'

    def form_valid(self, form):
        x = form.save()
        if x.code39:
            cod = str(x.id)
            while len(cod) < 10:
                cod = '0' + cod
            x.codigo = cod
            x.save()
        mensaje = 'Se ha agregado el producto: %s.' % x.descripcion
        add_notif(request=self.request, msg=mensaje, ico='fa fa-barcode text-green')
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
            context['encontrado_productos'] = Producto.objects.filter(
                Q(descripcion__icontains=buscar) | Q(codigo=buscar) |
                Q(marca__marca=buscar)).count()
        elif marca:
            context['encontrado_productos'] = Producto.objects.filter(
                marca__marca=marca).count()
        else:
            context['encontrado_productos'] = total
        return context

    def get_queryset(self):
        buscar = self.request.GET.get('buscar_prod')
        marca = self.request.GET.get('marca_prod')
        if buscar:
            return Producto.objects.filter(
                Q(descripcion__icontains=buscar) | Q(codigo=buscar) |
                Q(marca__marca=buscar))
        elif marca:
            return Producto.objects.filter(marca__marca=marca)
        else:
            return Producto.objects.all().order_by('-id')


class ProductoActualizar(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = CrearProductoForm
    success_url = reverse_lazy('Producto:url_lista', kwargs={'pk':1})
    template_name = 'Producto/producto_edit.html'

    def form_valid(self, form):
        x = form.save()
        if x.code39:
            cod = str(x.id)
            while len(cod) < 10:
                cod = '0' + cod
            x.codigo = cod
            x.save()
        mensaje = 'Se ha editado el producto: %s.' % x.descripcion
        add_notif(request=self.request, msg=mensaje, ico='fa fa-barcode text-yellow')
        return super(ProductoActualizar, self).form_valid(form)


class ProductoEliminar(LoginRequiredMixin, DeleteView):
    model = Producto
    success_url = reverse_lazy('Producto:url_lista', kwargs={'pk':1})
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        mensaje = 'Se ha eliminado el producto: %s.' % self.object.descripcion
        add_notif(request=self.request, msg=mensaje, ico='fa fa-barcode text-red')
        return super(ProductoEliminar, self).delete(request, *args, **kwargs)


class ProductoConsultar(LoginRequiredMixin, DetailView):
    model = Producto


class ProductoBuscar(LoginRequiredMixin, ListView):
    model = Producto
    paginate_by = 50


class MarcaNuevo(LoginRequiredMixin, CreateView):
    model = Marca
    form_class = CrearMarcaForm
    success_url = reverse_lazy('Producto:url_nueva_marca')
    template_name = 'Producto/marca_new.html'

    def form_valid(self, form):
        x = form.save(commit=False)
        mensaje = 'Se ha agregado la marca: %s.' % x.marca
        add_notif(request=self.request, msg=mensaje, ico='fa fa-tag text-green')
        return super(MarcaNuevo, self).form_valid(form)


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
    success_url = reverse_lazy('Producto:url_lista_marca', kwargs={'pk':1})
    template_name = 'Producto/marca_editar.html'

    def form_valid(self, form):
        x = form.save(commit=False)
        mensaje = 'Se ha editado la marca: %s.' % x.marca
        add_notif(request=self.request, msg=mensaje, ico='fa fa-tag text-yellow')
        return super(MarcaActualizar, self).form_valid(form)


class MarcaEliminar(LoginRequiredMixin, DeleteView):
    model = Marca
    success_url = reverse_lazy('Producto:url_lista_marca', kwargs={'pk':1})
    template_name = 'Producto/marca_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        mensaje = 'Se ha eliminado la marca: %s.' % self.object.marca
        add_notif(request=self.request, msg=mensaje, ico='fa fa-tag text-red')
        return super(MarcaEliminar, self).delete(request, *args, **kwargs)


class MarcaNuevoAjax(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        marca = request.GET['marca']
        m = CrearMarcaForm(request.GET)
        if m.is_valid():
            e = False
            m.save()
            mensaje = 'Se ha agregado la marca: %s.' % marca
            add_notif(request=self.request, msg=mensaje, ico='fa fa-tag text-green')
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


class GetNotifications(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        data = JsonResponse({
            'notificaciones': request.session['notificaciones'],
            'cantidad': request.session['cantidad'],
            'song': request.session['song'],
            'visto': request.session['visto'],
        })
        request.session['song'] = False
        request.session.save()
        return HttpResponse(data, content_type='application/json')


class DeleteNotifications(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        request.session['notificaciones'] = list()
        request.session['song'] = False
        request.session['visto'] = False
        request.session.save()
        data = JsonResponse({
            'notificaciones': request.session['notificaciones'],
            'cantidad': request.session['cantidad'],
            'song': request.session['song'],
            'visto': request.session['visto'],
        })
        return HttpResponse(data, content_type='application/json')


class LookNotifications(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        request.session['visto'] = False
        request.session['cantidad'] = 0
        data = JsonResponse({
            'cantidad': request.session['cantidad'],
            'visto': request.session['visto'],
        })
        return HttpResponse(data, content_type='application/json')


class StatusBar(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        status_bar(request)
        data = JsonResponse({'status_bar': request.session.get('status_bar')})
        return HttpResponse(data, content_type='application/json')
