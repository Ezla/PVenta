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
