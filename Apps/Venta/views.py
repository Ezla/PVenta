# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView, FormView, View, ListView
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import login, logout
from django.db import transaction

from .forms import AuthenticationFormCustom
from Apps.Producto.models import Producto
from .logica import calcul_p, calcul_sql
from .models import Cuenta, Venta as Ventas

from decimal import Decimal
from io import BytesIO
import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle,Spacer, Table, Image
from reportlab.lib.pagesizes import A6
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
from reportlab.graphics.barcode import code128



class Login(FormView):
    template_name = 'Venta/login.html'
    form_class = AuthenticationFormCustom
    success_url = reverse_lazy('Venta:url_venta')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        # self.request.session['cuenta'] = []
        return super(Login, self).form_valid(form)


class Logout(RedirectView):
    url = reverse_lazy('Venta:url_index')
    permanent = False

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
    template_name = 'Venta/VentaTemplate/index.html'

    def dispatch(self, request, *args, **kwargs):
        return super(Venta, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Venta, self).get_context_data(**kwargs)
        context['data'] = self.request.session['cuenta']
        precio = calcul_p(self.request)
        context['precio'] = precio
        return context


class VentaBuscarProducto(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        codigo = request.GET.get('cod')
        nombre = request.GET.get('nombre')
        # Agregar - Listado de la compra
        cont = False
        try:
            if codigo:
                prod = Producto.objects.get(codigo=codigo)
            else:
                prod = Producto.objects.get(descripcion=nombre)
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
                if not cont:
                    request.session['cuenta'].insert(0, {'codigo': prod.codigo, 'descripcion': prod.descripcion,
                                                         'punitario': str(prod.punitario),
                                                         'pmayoreo': str(prod.pmayoreo), 'tprecio': False,
                                                         'cantidad': str(1)})
            else:
                request.session['cuenta'].append(
                    {'codigo': prod.codigo, 'descripcion': prod.descripcion, 'punitario': str(prod.punitario),
                     'pmayoreo': str(prod.pmayoreo), 'tprecio': False, 'cantidad': str(1)})
            # Calculamos precio total de la cuenta
            precio = calcul_p(request)
            data = JsonResponse({'cuenta': request.session['cuenta'], 'precio': precio, 'buscado': prod.id})
        except Exception:
            precio = calcul_p(request)
            data = JsonResponse({'cuenta': request.session['cuenta'], 'precio': precio})

        request.session.save()
        return HttpResponse(data, content_type='application/json')


class VentaRemoverProd(LoginRequiredMixin, View):

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
        data = JsonResponse({'cuenta': request.session['cuenta'], 'precio': precio})
        return HttpResponse(data, content_type='application/json')


class VentaAumentarProd(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        codigo = request.GET['cod']
        if request.session['cuenta']:
            for x in request.session['cuenta']:
                if x['codigo'] == codigo:
                    x['cantidad'] = str(int(x['cantidad']) + 1)
                    break
        request.session.save()
        precio = calcul_p(request)
        data = JsonResponse({'cuenta': request.session['cuenta'], 'precio': precio})
        return HttpResponse(data, 'application/json')


class VentaTipoPrecio(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        codigo = request.GET['cod']
        if request.session['cuenta']:
            for x in request.session['cuenta']:
                if x['codigo'] == codigo:
                    if not x['tprecio']:
                        x['tprecio'] = True
                    else:
                        x['tprecio'] = False
                    break
        request.session.save()
        precio = calcul_p(request)
        data = JsonResponse({'cuenta': request.session['cuenta'], 'precio': precio})
        return HttpResponse(data, 'application/json')


class VentaCancelarCuenta(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        request.session['cuenta'] = []
        request.session.save()
        data = JsonResponse({'listo': 'Se a cancelado la cuenta.'})
        return HttpResponse(data, content_type='application/json')


class VentaPagarCuenta(LoginRequiredMixin, View):
    # @transaction.atomic
    def get(self, request, *args, **kwargs):
        total = calcul_p(request)
        # Validamos si encontramos productos en la compra
        if total == 0:
            data = JsonResponse(
                {'mensaje': 'No hay productos agrregados, la cuenta es de $%s.' % str(total), 'tipo': False,
                 'cambio': ''})
            return HttpResponse(data, content_type='application/json')
        # Prevenir posibles problemas al trabajar con la cantidad enviada
        try:
            efectivo = Decimal(request.GET['efectivo'])
        except:
            data = JsonResponse(
                {'mensaje': 'Debes enviar una cantidad en forma numerica.', 'tipo': False, 'cambio': ''})
            return HttpResponse(data, content_type='application/json')
        # Validamos que el efectivo no sea negativo y sea mayor a lo que se paga
        if efectivo <= 0 or efectivo < total:
            data = JsonResponse({
                'mensaje': 'Has ingresado $%s. Debes ingresar una cantidad que cubra el total de la cuenta. $%s' % (
                    str(efectivo), str(total)), 'tipo': False, 'cambio': ''})
        elif efectivo >= total:
            # Creamos la cuenta con un numero de tiket generico
            cambio = efectivo - total
            c = Cuenta.objects.create(tiket='0000', total=total, efectivo=efectivo, cambio=cambio)
            # Creamos un Tiket para la cuenta en base al id de la cuenta y la fecha de creacion
            x = ''
            val = len(str(c.id))
            while (val < 10):
                x += '0'
                val = val + 1
            x += str(c.id)
            today = datetime.date.today()
            x = str(today).replace('-', '') + x
            # Actualizamos el Nuevo tiket de al cuenta
            Cuenta.objects.filter(id=c.id).update(tiket=x)
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
                                      descuento=False, precio=precio, cantidad=cantidad, subtotal=sub, cuenta=c)
            request.session['cuenta'] = []
            # {'codigo': prod.codigo, 'descripcion': prod.descripcion, 'punitario':str(prod.punitario), 'pmayoreo':str(prod.pmayoreo), 'cantidad':str(1)}
            data = JsonResponse({'mensaje': 'El pago ha sido realizado correctamente.', 'tipo': True, 'total': total,
                                 'efectivo': efectivo, 'cambio': cambio, 'url': '/Tiket/%i/' % c.id})
        # Posible error no detectado ???
        else:
            data = JsonResponse({'mensaje': 'Ha ocurrido un error, intenta nuevamente.', 'tipo': False, 'cambio': ''})
        return HttpResponse(data, content_type='application/json')


class VentaTiket(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        # Datos del ticket
        try:
            pk = kwargs.get('pk')
            cuenta = Cuenta.objects.get(id=pk)
            sql = Ventas.objects.filter(cuenta=pk)
        except:
            raise Http404
        # Preparamos Respuesta PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="somefilename.pdf"'
        pdf_name = 'tiket.pdf'
        # Guardaremos el PDF en un buffer
        buff = BytesIO()
        # PDF
        doc = SimpleDocTemplate(buff,
                                pagesize=(80*mm, 297*mm),
                                rightMargin=3*mm,
                                leftMargin=3*mm,
                                topMargin=0,
                                bottomMargin=0,
                                # topPadding=0,
                                # leftPadding=100*mm,
                                # rightPadding=20*mm,
                                )
        clientes = []
        # Estilos
        styles = getSampleStyleSheet()
        # Titulo
        styleH = styles['Heading1']
        styleH.fontName = 'Helvetica-Bold'
        styleH.alignment = TA_CENTER
        styleH.textColor = colors.green
        styleH.textColor = colors.white
        styleH.fontSize = 15
        styleH.backColor  = colors.black
        #lista de productos
        styleN = styles["Normal"]
        styleN.fontSize = 6
        styleN.fontName = 'Helvetica-Bold'
        styleN.alignment = TA_JUSTIFY
        # Datos de ticket
        styleM = styles["BodyText"]
        styleM.fontName = 'Helvetica-Bold'
        styleM.fontSize = 6
        styleM.alignment = TA_CENTER
        # Codigo del ticket
        barcode=code128.Code128(cuenta.tiket, barWidth=1.55)
        # Encabezado del ticket
        header = Paragraph('Papeleria y Regalos Alex', styleH)
        # Datos de empresa
        direccion = Paragraph('Calle del Rosario #15, Colonia Guadalupe', styleM)
        estado = Paragraph('JEREZ - ZACATECAS', styleM)
        telefono = Paragraph('Comercio al por menor', styleM)
        # Fecha de emision
        fecha = 'FECHA: %s' % cuenta.creado.strftime('%d/%m/%Y')
        hora = 'HORA: %s' % cuenta.creado.strftime('%I:%M:%S %p')
        emitidotxt = '%s %s' % (fecha, hora)
        emitido = Paragraph(emitidotxt, styleM)
        # Imagen
        I = Image(BASE_DIR + '/static/img/car.png', width=78, height=60)
        # Tabla para encabezado
        tas = Table([
            # ['',''],
            ['',I],
            [direccion, ''],
            [estado,''],
            [telefono,''],
            [Paragraph('RFC: FORR600502AN3', styleM),''],

            [fecha,hora],
        ], rowHeights=12)
        tas.setStyle(TableStyle(
            [
                # ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
                # ('BACKGROUND',(0,0),(1,0),colors.black),
                # ('ALIGN',(0,0),(1,0),'CENTER'),
                # ('FONTSIZE', (0, 0), (1, 0), 10),
                # Fechas emitido
                ('FONTSIZE', (0, -1), (1, -1), 6),
                ('ALIGN',(0,-1),(0,-1),'LEFT'),
                ('ALIGN',(1,-1),(1,-1),'RIGHT'),
                # Fucionamos Imagen
                ('SPAN',(1,0),(1,-2)),
                # Fucionamos titulo
                # ('SPAN',(0,0),(1,0)),
                # Negritas para la tabla
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ]
        ))
        # Tabla para items del ticket
        encabezado = ('NOMBRE','  ',' ', 'PRECIO', 'CANT', 'SUBTOTAL')
        productos = []
        estilos_tabla = []
        cont = 1
        for p in sql:
            productos.append((Paragraph(p.nombre.upper(), styleN),' ',' ', p.precio, p.cantidad, p.subtotal))
            estilos_tabla.append(('SPAN',(0,cont),(2,cont)))
            cont = cont + 1
        productos.append(('','','', '', 'TOTAL:', '$ %s' % str(cuenta.total)))
        productos.append(('','','', '', 'PAGO:', '$ %s' % str(cuenta.efectivo)))
        productos.append(('','','', '', 'CAMBIO:', '$ %s' % str(cuenta.cambio)))
        estilos_tabla = estilos_tabla + [
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
                ('LINEBELOW', (0, -1), (-1, -1), 2, colors.black),
                ('LINEABOVE', (0, 0), (-1, 0), 2, colors.black),
                ('LINEABOVE', (0, -3), (-1, -3), 2, colors.black),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (5, -1), 6),
                # ('LEFTPADDING',(4,0),(4,-1),-15),
                # ('LEFTPADDING',(4,0),(4,-1),15),
                ('BACKGROUND',(-2,-3),(-1,-1), colors.lightgrey),
                ('ALIGN',(3,0),(3,-1),'RIGHT'),
                ('ALIGN',(4,0),(4,-1),'CENTER'),
                ('ALIGN',(5,0),(5,-1),'RIGHT'),
                # ('ALIGN',(4,-3),(-1,-1),'RIGHT'),
                ('VALIGN', (1,1), (-1, -1), 'MIDDLE'),
                # fucionamos 3 celdas para el nombre de prod
                # ('SPAN',(0,-4),(2,-4)),
                # ('LINEBELOW', (0, -1), (-1, -1), 1, colors.grey),
            ]
        t = Table([encabezado] + productos, colWidths=12*mm,)
        t.setStyle(TableStyle(estilos_tabla))
        tbar = Table([
            [barcode],
            [cuenta.tiket],
        ])
        tbar.setStyle(TableStyle(
            [
                # Fechas emitido,
                ('ALIGN',(0,0),(0,0),'LEFT'),
                ('ALIGN',(0,-1),(0,-1),'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 6),
            ]
        ))
        # Texto de agradecimiento
        cajero = Paragraph('Te atiende %s %s'% (request.user.first_name, request.user.last_name), styleM)
        agradecimiento = Paragraph('GRACIAS POR SU PREFERENCIA', styleM)
        # Agregamos contenido al PDF
        clientes.append(header)
        # clientes.append(Spacer(1, 2.2 * mm))
        clientes.append(tas)
        # clientes.append(emitido)
        clientes.append(t)
        clientes.append(cajero)
        clientes.append(agradecimiento)
        clientes.append(Spacer(1, 5.2 * mm))
        clientes.append(tbar)


        doc.build(clientes)
        response.write(buff.getvalue())
        buff.close()
        return response

from xhtml2pdf import pisa
import cStringIO as StringIO
from django.template.loader import get_template
from django.template import Context
from cgi import escape
from VentaAlex.settings import BASE_DIR

class VentaTikets(LoginRequiredMixin, View):
    # template_name = 'Venta/ticket.html'

    # def get_context_data(self, **kwargs):
    #     sql = Ventas.objects.filter(cuenta=7)
    #     total = calcul_sql(sql)
    #     context = {'prod': sql, 'total': total}
    #     return context

    def render_to_pdf(template_src, context_dict):
        template = get_template(template_src)
        context = Context(context_dict)
        html  = template.render(context)
        result = StringIO.StringIO()

        pdf = pisa.pisaDocument(StringIO.StringIO(html.decode("utf-8")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

    def get(self, request, *args, **kwargs):
        sql = Ventas.objects.filter(cuenta=7)
        total = calcul_sql(sql)
        context = {'prod': sql, 'total': total,'pagesize':'A6', 'ruta':BASE_DIR.replace('\\','/')}

        template = get_template('Venta/ticket.html')
        context = Context(context)
        html  = template.render(context)
        result = StringIO.StringIO()

        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
