from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView, FormView, View
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import login, logout
from django.db import transaction

from .forms import AuthenticationFormCustom
from Apps.Producto.models import Producto
from .logica import calcul_p, calcul_sql
from .models import Cuenta, Venta as Ventas
from decimal import Decimal
import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.pagesizes import letter, A6
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table
from reportlab.lib import colors
from io import BytesIO

class Login(FormView):
    template_name = 'index.html'
    form_class = AuthenticationFormCustom
    success_url =  reverse_lazy('Venta:url_venta')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        self.request.session['cuenta'] = []
        return super(Login, self).form_valid(form)


class Logout(RedirectView):
    url = reverse_lazy('Venta:url_index')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(Logout, self).get(request, *args, **kwargs)


class LoginRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy('Venta:url_index'))
        else:
            return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class Venta(LoginRequiredMixin, TemplateView):
    template_name = 'Venta/index.html'

    def dispatch(self, request, *args, **kwargs):
        return super(Venta, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Venta, self).get_context_data(**kwargs)
        context['data'] = self.request.session['cuenta']
        precio = calcul_p(self.request)
        context['precio'] = precio
        return context


class Venta_Buscar_Producto(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        codigo = request.GET['cod']
            # Agregar - Listado de la compra
        cont = False
        try:
            prod = Producto.objects.get(codigo=codigo)
             # Validamos si esta vacio
            if request.session['cuenta']:
                for x in request.session['cuenta']:
                    # Validamos que no este en la lista
                    if x['codigo'] == prod.codigo:
                        # Si se encuentra, aumentamos solamente la cantidad
                        x['cantidad'] = str(int(x['cantidad']) + 1)
                        # Removemos y colocamos el item al inicio de la lista
                        y = x
                        request.session['cuenta'].remove(x)
                        request.session['cuenta'].insert(0, y)
                        # Bandera para comprobar si estaba en la lista
                        cont = True
                        break
                # Si la Bandera no se valido agregamos el item a la inicio de la lista
                if cont == False:
                    request.session['cuenta'].insert(0, {'codigo': prod.codigo, 'descripcion': prod.descripcion, 'punitario':str(prod.punitario), 'pmayoreo':str(prod.pmayoreo), 'tprecio':False, 'cantidad':str(1)})
            else:
                request.session['cuenta'].append({'codigo': prod.codigo, 'descripcion': prod.descripcion, 'punitario':str(prod.punitario), 'pmayoreo':str(prod.pmayoreo), 'tprecio':False, 'cantidad':str(1)})
            # Calculamos precio total de la cuenta
            precio = calcul_p(request)
            data = JsonResponse({'cuenta': request.session['cuenta'],'precio': precio,'buscado':prod.id})
        except Exception:
            precio = calcul_p(request)
            data = JsonResponse({'cuenta': request.session['cuenta'],'precio': precio})


        request.session.save()
        return HttpResponse(data, content_type='application/json')


class Venta_Remover_Prod(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        codigo = request.GET['cod']
        if request.session['cuenta']:
            for x in request.session['cuenta']:
                if x['codigo'] == codigo:
                    x['cantidad'] = str(int(x['cantidad']) - 1)
                    if int(x['cantidad']) <= 0:
                        request.session['cuenta'].remove(x)
                    break
        request.session.save()
        precio = calcul_p(request)
        data = JsonResponse({'cuenta': request.session['cuenta'],'precio': precio})
        return HttpResponse(data, content_type='application/json')


class Venta_Aumentar_Prod(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        codigo = request.GET['cod']
        if request.session['cuenta']:
            for x in request.session['cuenta']:
                if x['codigo'] == codigo:
                    x['cantidad'] = str(int(x['cantidad']) + 1)
                    break
        request.session.save()
        precio = calcul_p(request)
        data = JsonResponse({'cuenta': request.session['cuenta'],'precio': precio})
        return HttpResponse(data, 'application/json')


class Venta_Tipo_Precio(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        codigo = request.GET['cod']
        if request.session['cuenta']:
            for x in request.session['cuenta']:
                if x['codigo'] == codigo:
                    if x['tprecio'] == False:
                        x['tprecio'] = True
                    else:
                        x['tprecio'] = False
                    break
        request.session.save()
        precio = calcul_p(request)
        data = JsonResponse({'cuenta': request.session['cuenta'],'precio': precio})
        return HttpResponse(data, 'application/json')


class Venta_Cancelar_Cuenta(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        request.session['cuenta'] = []
        request.session.save()
        data = JsonResponse({'listo': 'Se a cancelado la cuenta.'})
        return HttpResponse(data, content_type='application/json')


class Venta_Pagar_Cuenta(LoginRequiredMixin, View):

    #@transaction.atomic
    def get(self, request, *args, **kwargs):
        total = calcul_p(request)
        # Validamos si encontramos productos en la compra
        if total == 0:
            data = JsonResponse({'mensaje': 'No hay productos agrregados, la cuenta es de $%s.' % str(total), 'tipo': False})
            return HttpResponse(data, content_type='application/json')
        # Prevenir posibles problemas al trabajar con la cantidad enviada
        try:
            efectivo = Decimal(request.GET['efectivo'])
        except:
            data = JsonResponse({'mensaje': 'Debes enviar una cantidad en forma numerica.'})
            return HttpResponse(data, content_type='application/json')
        # Validamos que el efectivo no sea negativo y sea mayor a lo que se paga
        if efectivo <= 0 or efectivo < total:
            data = JsonResponse({'mensaje': 'Has ingresado $%s. Debes ingresar una cantidad que cubra el total de la cuenta. $%s' % (str(efectivo),str(total)), 'tipo': False})
        elif efectivo >= total:
            # Creamos la cuenta con un numero de tiket generico
            cambio = efectivo - total
            C = Cuenta.objects.create(tiket='0000', total=total, efectivo=efectivo, cambio = cambio)
            # Creamos un Tiket para la cuenta en base al id de la cuenta y la fecha de creacion
            x = ''
            val = len(str(C.id))
            while (val < 10):
                x += '0'
                val = val + 1
            x += str(C.id)
            today = datetime.date.today()
            x = str(today).replace('-','') + x
            # Actualizamos el Nuevo tiket de al cuenta
            Cuenta.objects.filter(id=C.id).update(tiket=x)
            # Vinculamos los productos que se compraron a la cuenta
            for item in request.session['cuenta']:
                # Validamos si se cobra por precio a mayoreo o no
                if item.get('tprecio') == False:
                    precio = float(item.get('punitario'))
                else:
                    precio = float(item.get('pmayoreo'))
                cantidad = int(item.get('cantidad'))
                sub = precio * cantidad
                Ventas.objects.create(codigo=item.get('codigo'), nombre=item.get('descripcion'),
                descuento=False, precio=precio,cantidad=cantidad,subtotal=sub,cuenta=C)
            request.session['cuenta'] = []
            #{'codigo': prod.codigo, 'descripcion': prod.descripcion, 'punitario':str(prod.punitario), 'pmayoreo':str(prod.pmayoreo), 'cantidad':str(1)}
            data = JsonResponse({'mensaje': 'El pago ha sido realizado correctamente.', 'tipo': True})
        # Posible error no detectado ???
        else:
            data = JsonResponse({'mensaje': 'Ha ocurrido un error, intenta nuevamente.', 'tipo': False})
        return HttpResponse(data, content_type='application/json')


class Venta_Tiket(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        sql = Ventas.objects.filter(cuenta=11)
        total = calcul_sql(sql)
        response = HttpResponse(content_type='application/pdf')
        pdf_name = "tiket.pdf"
        buff = BytesIO()
        doc = SimpleDocTemplate(buff,
                            pagesize=A6,
                            rightMargin=0,
                            leftMargin=0,
                            topMargin=0,
                            bottomMargin=0,
                            )
        clientes = []
        styles = getSampleStyleSheet()

        header = Paragraph("Comprobante de Ventas", styles['Heading1'])

        clientes.append(header)
        headings = ('Nombre', 'Precio', 'Cantidad', 'Subtotal')
        allclientes = [(p.nombre, p.precio, p.cantidad, p.subtotal) for p in sql]
        allclientes.append(('','','TOTAL:', total))
        t = Table([headings] + allclientes)
        t.setStyle(TableStyle(
            [
                #('GRID', (0, 0), (3, -1), 1, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                ('LINEABOVE', (0, -1), (-1,-1), 1, colors.black),
                #('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
                ('FONTSIZE',(0,0),(3,len(allclientes)),7)
            ]
        ))
        clientes.append(t)
        doc.build(clientes)
        response.write(buff.getvalue())
        buff.close()
        return response

class Venta_Demo(TemplateView):
    template_name = 'Demo.html'


