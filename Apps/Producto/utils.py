from string import digits, ascii_uppercase, ascii_lowercase
from random import choice
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.graphics.barcode import code39

from .models import Producto


def random_string(length=1, uppercase=False, lowercase=False):
    """
    Genera una cadena aleatoria de caracteres, que puede contener numeros,
    letras mayusculas y letras minusculas, el primer caracter sera siempre
    una letra mayuscula.
    :param length: (int) Cantidad de caracteres que contendra la cadena.
    :param uppercase: (boolean) Valida si la cadena contendra letras
    mayusculas.
    :param lowercase: (boolean) Valida si la cadena contendra letras
    minusculas.
    :return: (str) Cadena aleatoria.
    """
    characters = digits
    code = str()

    if uppercase:
        characters += ascii_uppercase
    if lowercase:
        characters += ascii_lowercase

    while len(code) < length:
        character = choice(characters)
        if len(code) == 0:
            character = choice(ascii_uppercase)

        code += character

    return code


def barcode_two_column_format(products=list()):
    """
    Genera un pdf con un maximo 20 códigos de barras, con un formato de 2
    columnas.
    :param products: Lista (list) de diccionarios (dict) con formato
            [{'pk': 1, 'quantity': 2}]
    :return: Archivo PDF
    """
    buffer = BytesIO()
    template = canvas.Canvas(buffer, pagesize=A4)
    x_axis = 10 * mm
    y_axis = 260 * mm
    cont = 1
    for item in products:
        product = Producto.objects.get(pk=item.get('pk'))
        barcode = code39.Extended39(product.codigo,
                                    barWidth=0.5 * mm,
                                    barHeight=20 * mm,
                                    checksum=False)
        cont_quantity = 0
        while cont_quantity < item.get('quantity'):
            template.drawString(x_axis + 5 * mm,
                                y_axis + 22 * mm,
                                product.descripcion)
            barcode.drawOn(template, x_axis, y_axis)
            template.drawString(x_axis + 35 * mm,
                                y_axis - 5 * mm,
                                product.codigo)

            x_axis = x_axis + 90 * mm
            cont_quantity += 1
            cont += 1

            if (cont % 2) == 1:
                x_axis = x_axis - 180 * mm
                y_axis = y_axis - 35 * mm

    template.showPage()
    template.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def barcode_three_column_format(products=list()):
    """
    Genera un pdf con un maximo 30 códigos de barras, con un formato de 3
    columnas.
    :param products: Lista (list) de diccionarios (dict) con formato
            [{'pk': 1, 'quantity': 2}]
    :return: Archivo PDF
    """
    buffer = BytesIO()
    template = canvas.Canvas(buffer, pagesize=A4)
    x_axis = 0 * mm
    y_axis = 275 * mm
    cont = 0

    for item in products:
        product = Producto.objects.get(pk=item.get('pk'))
        cont_quantity = 0
        while cont_quantity < item.get('quantity'):
            barcode = code39.Extended39(product.codigo,
                                        barWidth=0.3 * mm,
                                        barHeight=12 * mm,
                                        checksum=False)
            template.setFontSize(6, 15)

            template.drawString(x_axis + 5 * mm,
                                y_axis + 13 * mm,
                                product.descripcion)
            barcode.drawOn(template, x_axis, y_axis)
            template.drawString(x_axis + 25 * mm,
                                y_axis - 3 * mm,
                                product.codigo)

            x_axis = x_axis + 72.5 * mm
            cont += 1

            if cont == 3:
                x_axis -= 217.5 * mm
                y_axis -= 26.5 * mm
                cont = 0
            cont_quantity += 1

    template.showPage()
    template.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def barcode_six_column_format(products=list()):
    """
    Genera un pdf con un maximo 150 códigos de barras, con un formato de 6
    columnas.
    :param products: Lista (list) de diccionarios (dict) con formato
            [{'pk': 1, 'quantity': 2}]
    :return: Archivo PDF
    """
    buffer = BytesIO()
    template = canvas.Canvas(buffer, pagesize=A4)
    x_axis = 0 * mm
    y_axis = 275 * mm
    cont = 0
    template.drawString(x_axis + 73 * mm,
                        y_axis + 10 * mm,
                        'Plantilla con 150 codigos de barras')

    for item in products:
        product = Producto.objects.get(pk=item.get('pk'))
        cont_quantity = 0
        while cont_quantity < item.get('quantity'):
            barcode = code39.Extended39(product.codigo,
                                        barWidth=0.17 * mm,
                                        barHeight=5 * mm,
                                        checksum=False)
            template.setFontSize(6, 15)
            barcode.drawOn(template, x_axis, y_axis)
            template.drawString(x_axis + 13 * mm,
                                y_axis - 2.4 * mm,
                                product.codigo)

            x_axis = x_axis + 34 * mm
            cont += 1

            if cont == 6:
                x_axis -= 204 * mm
                y_axis -= 10.5 * mm
                cont = 0
            cont_quantity += 1

    template.showPage()
    template.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
