var $codigo = $('#codigo');
var $tablaVenta = $('#tVentaProd');

/**
 * Creara un producto en un tr, para poder representar el carrito de
 * compra.
 * @param {string} code: Codigo de barras.
 * @param {string} name: Nombre del producto.
 * @param {boolean} withDiscount: indicara el tipo de precio a usar.
 * @param {integer} price: Precio del producto.
 * @param {integer} quantity: Cantidad de productos.
 * @returns {jQuery}
 */
function renderProductCart(code, name, withDiscount, price, quantity) {
    var cssGlyphicon = 'glyphicon glyphicon-thumbs-down';
    var cssColor = 'btn btn-success discount';
    var title = 'Quitar descuento';
    if (withDiscount) {
         cssGlyphicon = 'glyphicon glyphicon-thumbs-up';
         cssColor = 'btn btn-warning discount';
         title = 'Agregar descuento';
    }
    var $code = $('<td/>', {'text': code});
    var $name = $('<td/>', {'text': name});
    var $btnDiscount = $('<td/>').append(
        $('<button/>', {
            'type': 'button',
            'data-discount': withDiscount,
            'class': cssColor,
            'title': title
        }).on('click', changeDiscountProduct).append($('<spam/>',
            {'class': cssGlyphicon})));
    var $price = $('<td/>', {'text': price});
    var $upQuantity = $('<spam/>',{'class': 'input-group-btn'}).append(
            $('<button/>', {
                'type': 'button',
                'class': 'btn btn-info',
                'title': 'Aumentar'
            }).on('click', upProduct).append($('<spam/>',
                {'class': 'glyphicon glyphicon-chevron-up'})));
    var $downQuantity = $('<spam/>',{'class': 'input-group-btn'}).append(
            $('<button/>', {
                'type': 'button',
                'class': 'btn btn-info',
                'title': 'Disminuir'
            }).on('click', downProduct).append($('<spam/>',
                {'class': 'glyphicon glyphicon-chevron-down'})));
    var $inputQuantity = $('<input/>', {
            'placeholder': 'Cantidad',
            'class': 'form-control text-center',
            'data-quantity': quantity,
            'value': quantity
        }).on('change', changeQuantityProduct).on('focus', selectInput);
    var $groupQuantity = $('<td/>').append($('<div/>',
        {'class': 'input-group'}).append($downQuantity, $inputQuantity,
        $upQuantity));
    var $btnRemove = $('<td/>', {'class': 'width-ten-percent'}).append(
        $('<button/>', {
            'type': 'button',
            'class': 'btn btn-danger',
            'title': 'Quitar'
        }).on('click', removeProduct).append(
            $('<spam/>', {'class': 'glyphicon glyphicon-remove'})));
    var $itemProduct = $('<tr/>', {
        'class': 'tr-product',
        'data-code': code
    }).append($code, $name, $btnDiscount, $price, $groupQuantity, $btnRemove);
    return $itemProduct
}

/**
 * A partir de una lista de productos dubujara los productos en una tabla.
 * @param {array} products: lista de productos.
 */
function renderCart(products) {
    $tablaVenta.html('');
    $.each(products, function (i, item) {
        if (item.with_discount) {
            var price = item.price_down;
        } else {
            var price = item.price_up;
        }
        $tablaVenta.append(renderProductCart(item.code, item.name, item.with_discount, price, item.quantity));
    });
}

/**
 * Dibujara los precios del carrito de compra.
 * @param {object} cart: objeto con las variables subtotal, descuento y
 * todal.
 */
function renderCartStatus(cart) {
    var $subtotal = $('<p/>').append(
        $('<b/>', {'text': 'Subtotal:'}),
        $('<b/>', {'text': '$ ' + cart.subtotal, 'class': 'pull-right'})
    );
    var $discount = $('<p/>').append(
        $('<b/>', {'text': 'Descuento:'}),
        $('<b/>', {'text': '$ -' + cart.discount, 'class': 'pull-right'})
    );
    var $total = $('<p/>').append(
        $('<b/>', {'text': 'TOTAL:'}),
        $('<b/>', {'text': '$ ' + cart.total, 'class': 'pull-right'})
    );
    var $name = $('<p/>', {'text': name});
    $('#cart').html('').append($subtotal, $discount, $total);
}

/**
 * Dibuja un iframe para visualizar un pdf con el ticket de compra, para
 * posteriormente solicitar la imprecion del mismo.
 * @param {string} url: Url donde esta el el ticket.
 */
function renderTicket(url) {
    var name = 'visualizador-pdf';
    var $iframe = $('<iframe/>', {
        'id': name,
        'name': name,
        'src': url,
        'width': '100%',
        'height': '600px'
    });
    $('.well').append($iframe);
    setTimeout(function () {
        window.frames[name].focus();
        window.frames[name].print();
    }, 2000);
    setTimeout(function () {
        $('#visualizador-pdf').remove();
    }, 30000);
}

/**
 * Dibuja las sugerencias de busqueda en un modal.
 * @param {array} products: lista de productos.
 */
function renderSuggestions(products) {
    $('#modal-body').html('');
    if (products.length > 0) {
        $.each(products, function (i, item) {
            var $code = $('<td/>', {'text': item.code});
            var $name = $('<td/>', {'text': item.name});
            var $tr = $('<tr/>', {
                'role': 'button',
                'data-code': item.code
            }).append($code, $name).on('click', selectProuct);
            $('#modal-body').append($tr);
        });
    } else {
        var $tr = $('<tr/>').append($('<td/>', {
            'text': 'No se encontraron coincidencias'
        }));
        $('#modal-body').append($tr);
    }
    $('#suggestions').modal('show');
}

/**
 * Limpia el carrito de compras, y los precios del mismo.
 * @param {integer} id: id de la cuenta para formar la url donde se
 * encuentra el ticket de la misma.
 */
function paidCart(id) {
    var url = url_ticket + id + '/';
    renderTicket(url);
    $('#percent_off').val(0);
    $('#cash').val(0);
    renderCart([]);
    renderCartStatus({'subtotal': 0, 'discount': 0, 'total': 0});
}

/**
 * Realiza la petición al servidor mediante ajax.
 * @param {object} data: Datos que se enviaran en la petición.
 * @param {string} url: Dirección a la cual se realizara la petición.
 * @param {string} methodType: Tipo de metodo http con el cual se
 * realizara la petición (get/post).
 */
function ajaxChangeProduct(data, url, methodType) {
    $.ajax({
        async: false,
        data: data,
        url: url,
        type: methodType,
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken",
                $('[name=csrfmiddlewaretoken]').val());
        },
        success: function (data, textStatus, jqXHR) {
            if (methodType == 'get') {
                renderCartStatus(data);
            } else if (methodType == 'post' && url == url_cart_pay) {
                paidCart(data.pk);
            } else if (methodType == 'post') {
                if (jqXHR.status == 200) {
                    getCartStatus();
                    renderCart(data);
                } else {
                    renderSuggestions(data);
                }
            } else if (methodType == 'delete') {
                $tablaVenta.html('');
                getCartStatus();
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            var data = jqXHR.responseJSON;
            if ('cash' in data) {
                $('#cash').data('content', data.cash);
                $('#cash').popover().click();
            }
        }
    });
}

/**
 * Gestiona una consulta al servidor para buscar productos por el codigo
 * de barras.
 */
function searchProuct(e){
    e.preventDefault();
    var data = {'word': $codigo.val()};
    ajaxChangeProduct(data, url_search_product, 'post');
    $codigo.val('').focus();
}

/**
 * Selecciona un producto de las sugerencias para agregarlo al carrito.
 */
function selectProuct() {
    $codigo.val($(this).data('code'));
    $('#form_search').submit();
}

/**
 * Gestiona una consulta al servidor para agregar uno mas a la cantidad de
 * productos.
 */
function upProduct(e) {
    var $inputQuantity = $(this).parents('td').find('input');
    var $trProduct = $(this).parents('tr');
    var $btnWithDiscount = $trProduct.find('button.discount');
    var quantity = Number($inputQuantity.val()) + 1;
    var data = {
        'code': $trProduct.data('code'),
        'with_discount': $btnWithDiscount.data('discount'),
        'quantity': quantity
    };
    ajaxChangeProduct(data, url_change_product, 'post');
}

/**
 * Gestiona una consulta al servidor para disminuir uno menos a la
 * cantidad de productos.
 */
function downProduct(e) {
    var $inputQuantity = $(this).parents('td').find('input');
    var $trProduct = $(this).parents('tr');
    var $btnWithDiscount = $trProduct.find('button.discount');
    var quantity = Number($inputQuantity.val()) - 1;
    var data = {
        'code': $trProduct.data('code'),
        'with_discount': $btnWithDiscount.data('discount'),
        'quantity': quantity
    };
    ajaxChangeProduct(data, url_change_product, 'post');
}

/**
 * Gestiona una consulta al servidor para cambiar la cantidad de productos.
 */
function changeQuantityProduct() {
    var $trProduct = $(this).parents('tr');
    var $btnWithDiscount = $trProduct.find('button.discount');
    var data = {
        'code': $trProduct.data('code'),
        'with_discount': $btnWithDiscount.data('discount'),
        'quantity': Number($(this).val())
    };
    ajaxChangeProduct(data, url_change_product, 'post');
}

/**
 * Gestiona una consulta al servidor para cambiar al tipo de precio del
 * producto.
 */
function changeDiscountProduct(e) {
    var $trProduct = $(this).parents('tr');
    var $inputQuantity = $trProduct.find('input');
    var withDiscount = Boolean($(this).data('discount'));
    if (withDiscount) {
        withDiscount = false;
    } else {
        withDiscount = true;
    }
    var data = {
        'code': $trProduct.data('code'),
        'with_discount': withDiscount,
        'quantity': Number($inputQuantity.val())
    };
    ajaxChangeProduct(data, url_change_product, 'post');
}

/**
 * Gestiona una consulta al servidor para eliminar el producto.
 */
function removeProduct() {
    var data = {
        'code': $(this).parents('tr').data('code'),
        'with_discount': false,
        'quantity': 0
    };
    ajaxChangeProduct(data, url_change_product, 'post');
}

/**
 * Gestiona una consulta al servidor para obtener precio todal del carrito
 * de compra.
 */
function getCartStatus() {
    var data = {
        'percent_off': $('#percent_off').val()
    };
    ajaxChangeProduct(data, url_cart_status, 'get');
}

/**
 * Gestiona una consulta al servidor para pagar lo que este en el carrito
 * de compra.
 */
function payCart() {
    var data = {
        'percent_off': $('#percent_off').val(),
        'cash': $('#cash').val()
    };
    ajaxChangeProduct(data, url_cart_pay, 'post');
}

/**
 * Permite seleccionar el contenido del input al seleccionarlo el mismo.
 */
function selectInput() {
    $(this).select();
}

/**
 * Permite seleccionar el contenido del input al seleccionarlo el mismo.
 */
function selectCash() {
    $(this).select();
    $(this).popover('destroy');
}

/**
 * Permite negar la antrada de teclas que no cincidan con un numero:
 * Backspace = 8, Enter = 13, ‘0′ = 48, ‘9′ = 57, ‘.’ = 46, ‘-’ = 43
 * @param {event} e: evento que contiene el caracter tecleado.
 * @returns {boolean}: Esto permitira la incercion del caracter al input.
 */
function filterFloat(e) {
    var key = window.Event ? e.which : e.keyCode;
    var chark = String.fromCharCode(key);
    var tempValue = $(this).val() + chark;
    if (key >= 48 && key <= 57) {
        if (filter(tempValue) === false) {
            return false;
        } else {
            return true;
        }
    } else {
        if (key == 8 || key == 13 || key == 0) {
            return true;
        } else if (key == 46) {
            if (filter(tempValue) === false) {
                return false;
            } else {
                return true;
            }
        } else {
            return false;
        }
    }
}

/**
 * Gestiona la peticion al servidor para eliminar la lista de productos
 * en el carrito de compra.
 */
function cleanCart() {
    ajaxChangeProduct({}, url_cart_status, 'delete');
}

/**
 * Valida si el parametro enviado coincide con el patron de numero con
 * solo 2 decimales.
 * @param key {Numeric}: numero a comparar con el patron.
 * @returns {boolean}: regresa si el dato enviado coincide con el patrón.
 */
function filter(key) {
    var pattern = /^([0-9]+\.?[0-9]{0,2})$/;
    if (pattern.test(key) === true) {
        return true;
    }
    return false;
}

/**
 * Evento para seleccionar (focus) al input de descuento.
 */
function keyPercentOff() {
    $('#percent_off').focus();
}

/**
 * Evento para seleccionar (focus) al input de efectivo.
 */
function keyFocusCash() {
    $('#cash').focus();
}

/**
 * Evento para seleccionar (focus) al input de codigo de barras.
 */
function keyFocusCode() {
    $codigo.focus();
}

/**
 * Evento para pagar (click en el boton de pagar).
 */
function keyPay() {
    $('#pagar_cuenta').click();
}

/**
 * Inicializa la aplicacion, una vez que se cargan todos los scripts.
 */
$(document).ready(function () {
    $codigo.focus();
    renderCart(JSON.parse(account));
    getCartStatus();
});

$('#cash').on('keypress', filterFloat);
$('#cash').on('focus', selectCash);
$('#percent_off').on('change', getCartStatus);
$('#form_search').on('submit', searchProuct);
$('#pagar_cuenta').on('click', payCart);
$('#clean_cart').on('click', cleanCart);
// Focus en descuento
$(document).on('keydown', null, 'alt+7', keyPercentOff);
$codigo.on('keydown', null, 'alt+7', keyPercentOff);
$('#cash').on('keydown', null, 'alt+7', keyPercentOff);
// Focus en efectivo
$(document).on('keydown', null, 'alt+8', keyFocusCash);
$codigo.on('keydown', null, 'alt+8', keyFocusCash);
$('#percent_off').on('keydown', null, 'alt+8', keyFocusCash);
// Focus en buscador
$(document).on('keydown', null, 'alt+9', keyFocusCode);
$('#cash').on('keydown', null, 'alt+9', keyFocusCode);
$('#percent_off').on('keydown', null, 'alt+9', keyFocusCode);
// Pagar cuenta
$(document).on('keydown', null, 'alt+1', keyPay);
$codigo.on('keydown', null, 'alt+1', keyPay);
$('#cash').on('keydown', null, 'alt+1', keyPay);
$('#percent_off').on('keydown', null, 'alt+1', keyPay);
