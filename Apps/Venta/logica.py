from decimal import Decimal
import barcode
from datetime import datetime


def calcul_p(request):
    precio = 0
    if request.session['cuenta']:
        for x in request.session['cuenta']:
            if not x['tprecio']:
                precio = precio + (Decimal(x['punitario']) * Decimal(x['cantidad']))
            else:
                precio = precio + (Decimal(x['pmayoreo']) * Decimal(x['cantidad']))
    return precio


def calcul_sql(venta):
    precio = 0
    if venta:
        for x in venta:
            precio += x.subtotal
    return precio


def add_notif(request, msg, ico):
    formato = '%d/%m/%y %I:%M %p'
    fecha = datetime.today()
    datef = fecha.strftime(formato)
    mensaje = {
        'msj': msg,
        'time': datef,
        'icono': ico,
               }
    request.session['notificaciones'].insert(0, mensaje)
    request.session['song'] = True
    request.session['visto'] = True
    request.session['cantidad'] += 1
    request.session.save()


def status_bar(request):
    if request.session.get('status_bar') == '':
        request.session['status_bar'] = ' sidebar-collapse'
    else:
        request.session['status_bar'] = ''
    request.session.save()

def crear_ean13(valor, archivo):
    ean = barcode.get('ean13', valor, writer=barcode.writer.ImageWriter())
    # mostramos el codigo de barras en consola
    print(ean.to_ascii())
    # generamos el archivo
    filename = ean.save(archivo)
    return filename


def crear_isbn13(valor, archivo):
    """ El valor de isbn13 tiene que empezar por 978 or 979"""
    isbn = barcode.ISBN13(valor, writer=barcode.writer.ImageWriter())
    # mostramos el codigo de barras en consola
    print(isbn.to_ascii())
    # generamos el archivo
    filename = isbn.save(archivo)
    return filename


def crear_code39(valor, archivo):
    code39 = barcode.Code39(valor, writer=barcode.writer.ImageWriter())
    # mostramos el codigo de barras en consola
    print(code39.to_ascii())
    # generamos el archivo
    filename = code39.save(archivo)
    return filename

    # crear_ean13("123456789012", "ean13")

    # crear_isbn13("978123456", "isbn13")

    # crear_code39("123456789012", "code39")
