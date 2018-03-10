def validate_product(data):
    errores = {}
    cont = 0
    # ---codigo---
    if not data.get('code39'):
        if not data.get('codigo'):
            msg = 'Este campo es obligatorio.'
            errores.update({'codigo': msg})
            cont = 1
        elif len(data.get('codigo')) < 8:
            msg = 'El codigo de barras debe contener al menos ocho caracteres.'
            errores.update({'codigo': msg})
            cont = 1
    # ---punitario---
    if data.get('punitario') < data.get('pmayoreo'):
        msg = 'El precio unitario debe ser mayor que el precio  por mayoreo.'
        errores.update({'punitario': msg})
        cont = 1
    if data.get('punitario') < 0:
        msg = 'Este campo no puede contener numeros negativos.'
        errores.update({'punitario': msg})
        cont = 1
    # ---pmayoreo---
    if data.get('punitario') < data.get('pmayoreo'):
        msg = 'El precio por mayoreo debe ser menor al precio unitario.'
        errores.update({'pmayoreo': msg})
        cont = 1
    if data.get('pmayoreo') < 0:
        msg = 'Este campo no puede contener numeros negativos.'
        errores.update({'pmayoreo': msg})
        cont = 1
    # ---inventario---
    if data.get('inventario'):
        # ---cantidad---
        if data.get('cantidad') is None:
            msg = 'Este campo es obligatorio, cuando inventario esta activo.'
            errores.update({'cantidad': msg})
            cont = 1
        elif data.get('cantidad') < 0:
            msg = 'Este campo no puede contener numeros negativos.'
            errores.update({'cantidad': msg})
            cont = 1
        # ---minimo---
        if data.get('minimo') is None:
            msg = 'Este campo es obligatorio, cuando inventario esta activo.'
            errores.update({'minimo': msg})
            cont = 1
        elif data.get('minimo') < 0:
            msg = 'Este campo no puede contener numeros negativos.'
            errores.update({'minimo': msg})
            cont = 1
    if not data.get('marca'):
        msg = 'Este campo es obligatorio.'
        errores.update({'marca': msg})
        cont = 1

    return cont, errores
