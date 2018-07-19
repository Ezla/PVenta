from decimal import Decimal


def validateAccount(account):
    errors = {}
    subtotal = account.get('subtotal', 0)
    percent_off = account.get('discount')
    discount = (subtotal * Decimal(percent_off.percentage)) / Decimal(100)
    total = subtotal - discount
    if subtotal <= 0:
        msg = 'Este campo tiene que ser mayor a cero.'
        errors.update({'subtotal': msg})
    cash = account.get('cash', 0)
    if cash <= 0 and cash < total:
        msg = 'Este campo tiene que ser mayor al total (${}).'.format(
            total)
        errors.update({'cash': msg})
    return errors
