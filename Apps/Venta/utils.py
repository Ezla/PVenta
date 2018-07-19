from decimal import Decimal, ROUND_UP


def process_cart(cart=list(), percent_off=0):
    """
    Calcula el precio total, subtotal y descuento de los productos en el
    carrito de compras.
    :param cart: (list) lista de productos que estan el el carrito.
    Esta lista lleva un formato del modelo SalesProduct.
    :param percent_off: (int) porcentaje de descuento aplicable.
    :return: (Decimal) cantidades calculadas de subtotal, total y
    descuento a partir de los productos que hay en el carrito.
    """
    subtotal = Decimal(0)

    for product in cart:
        with_discount = product.get('with_discount')
        quantity = product.get('quantity')
        if not with_discount:
            price = product.get('price_up')
        else:
            price = product.get('price_down')

        subtotal_product = Decimal(price) * Decimal(quantity)
        subtotal += subtotal_product

    discount = subtotal * Decimal(percent_off) / Decimal(100)
    # rounding
    total = subtotal - discount.quantize(Decimal('.01'), rounding=ROUND_UP)
    return subtotal, total, discount
