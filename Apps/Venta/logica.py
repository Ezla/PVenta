from decimal import Decimal
import barcode


def calcul_p(request):
    precio = 0
    if request.session['cuenta']:
        for x in request.session['cuenta']:
            if x['tprecio'] == False:
                precio = precio + (Decimal(x['punitario']) * Decimal(x['cantidad']))
            else:
                precio = precio + (Decimal(x['pmayoreo']) * Decimal(x['cantidad']))
    return precio


def calcul_sql(Venta):
    precio = 0
    if Venta:
        for x in Venta:
            precio += x.subtotal
    return precio


def crear_ean13(valor, archivo):
    ean = barcode.get('ean13', valor, writer=barcode.writer.ImageWriter())
    # mostramos el codigo de barras en consola
    print ean.to_ascii()
    # generamos el archivo
    filename = ean.save(archivo)


def crear_isbn13(valor, archivo):
    """ El valor de isbn13 tiene que empezar por 978 or 979"""
    isbn = barcode.ISBN13(valor, writer=barcode.writer.ImageWriter())
    # mostramos el codigo de barras en consola
    print isbn.to_ascii()
    # generamos el archivo
    filename = isbn.save(archivo)


def crear_code39(valor, archivo):
    code39 = barcode.Code39(valor, writer=barcode.writer.ImageWriter())
    # mostramos el codigo de barras en consola
    print code39.to_ascii()
    # generamos el archivo
    filename = code39.save(archivo)
    return filename


#crear_ean13("123456789012", "ean13")

#crear_isbn13("978123456", "isbn13")

#crear_code39("123456789012", "code39")