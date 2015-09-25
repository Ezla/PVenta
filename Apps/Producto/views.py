from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView, View

import barcode
from StringIO import StringIO
from .models import Producto, Marca
from .forms import CrearProductoForm, CrearMarcaForm
from Apps.Venta.views import LoginRequiredMixin
from Apps.Venta.logica import crear_code39


class Producto_Nuevo(LoginRequiredMixin, CreateView):
	model = Producto
	form_class = CrearProductoForm
	success_url = '/Producto/Lista/1/'

	def form_valid(self, form):
		x = form.save()
		cod = str(x.id)
		while len(cod) < 10:
			cod = '0' + cod
		print cod
		x.codigo = cod
		x.save()
		return super(Producto_Nuevo, self).form_valid(form)


class Producto_Lista(LoginRequiredMixin, ListView):
	model = Producto
	paginate_by=50

	def get_context_data(self, **kwargs):
		context = super(Producto_Lista, self).get_context_data(**kwargs)
		context['total_productos'] = Producto.objects.count()
		return context


class Producto_Actualizar(LoginRequiredMixin, UpdateView):
	model = Producto
	form_class = CrearProductoForm
	success_url = '/Producto/Lista/1/'


class Producto_Eliminar(LoginRequiredMixin, DeleteView):
	model = Producto
	success_url = '/Producto/Lista/1/'


class Producto_Consultar(LoginRequiredMixin, DetailView):
	model = Producto


class Marca_Nuevo(LoginRequiredMixin, CreateView):
	model = Marca
	form_class = CrearMarcaForm
	success_url = '/Marca/Lista/1/'
	template_name = 'Producto/marca_form.html'


class Marca_Lista(LoginRequiredMixin, ListView):
	model = Marca
	paginate_by=50
	template_name = 'Producto/marca_list.html'

	def get_context_data(self, **kwargs):
		context = super(Marca_Lista, self).get_context_data(**kwargs)
		context['total_marcas'] = Marca.objects.count()
		return context


class Marca_Actualizar(LoginRequiredMixin, UpdateView):
	model = Marca
	form_class = CrearMarcaForm
	success_url = '/Marca/Lista/1/'
	template_name = 'Producto/marca_form.html'


class Marca_Eliminar(LoginRequiredMixin, DeleteView):
	model = Marca
	success_url = '/Marca/Lista/1/'
	template_name = 'Producto/marca_confirm_delete.html'


class Marca_Nuevo_Ajax(LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		marca = request.GET['marca']
		M = CrearMarcaForm(request.GET)
		if M.is_valid():
			e = False
			M.save()
			mensaje = 'Nueva marca %s agregada' % marca
		else:
			e = True
			mensaje = M.errors
		marcas = Marca.objects.all()
		dic_marcas =[]
		for x in marcas:
			dic_marcas.append({'id': x.id, 'marca': x.marca})
		data = JsonResponse({'Errores': e, 'Marcas': dic_marcas,'mensaje': mensaje})
		#data = serializers.serialize('json', marcas)
		return HttpResponse(data, content_type='application/json')


class Code_Imagen(LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		fp = StringIO()
		code39 = barcode.generate('Code39','123456789012', writer=barcode.writer.ImageWriter(), output=fp)
		#filename = code39.save('img')
		response = HttpResponse(code39, content_type='application/png')
		response['Content-Disposition'] = 'filename="img.png"'
		return response