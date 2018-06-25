/**
 * Agrega el producto desde la lisa de sugerencias (busqueda) a la lista
 * de selección.
 */
function selectSuggestions() {
    var pk = $(this).data('pk');
    var codigo = $(this).data('code');
    var descripcion = $(this).data('description');
    var $product = $('.tr-product[data-product=' + pk + ']');
    if ($product.length) {
        var quantity = Number($product.find('input').val()) + 1;
        $product.find('input').val(quantity)
    } else {
        var $item = renderProductOption(pk, codigo, descripcion);
        $('#options').append($item);
    }
    $('#buscar_prod').focus();
    if ($('#productsCollapse').hasClass('collapsed-box')) {
        $('#productsBtnCollapse').click();
    }
    validateStickers();
}

/**
 * Quita el producto de la lista de selcción.
 */
function removeProduct() {
    $(this).parent().parent().remove();
    validateStickers();
}

/**
 * Valida la cantidad de etiquetas y dibuja la cantidad de etiquetas
 * selecionadas en la plantilla de ejemplo.
 * @returns {boolean}
 */
function validateStickers() {

    var counter = 0;
    var stickers = 0;
    $('.input-sticker').each(function () {
        counter += Number($(this).val());
    });
    $('#counter-sticker').text(counter);
    $('.ul-sticker>li').removeClass('sticker-selected').each(function () {
        if (stickers < counter) {
            stickers++;
            $(this).addClass('sticker-selected');
        }
    });
    return counter == 30
}

/**
 * Renderisa un indicador que muestra el numero de coincidencias en la
 * busqueda de productos.
 * @param {Number} counter
 * @returns {jQuery}
 */
function renderCounterStatus(counter) {
    if (counter >= 0) {
        var $status = $('<strong/>', {'text': counter});
    } else {
        var $status = $('<spam/>', {'class': 'glyphicon glyphicon-search'});
    }
    return $status
}

/**
 * Renderisa un tr que le indica al usuario que no hay coincidencias
 * (resultados) en su busqueda.
 * @returns {jQuery}
 */
function renderNotMatches() {
    var $description = $('<td/>', {
        'text': 'No se encontraron coincidencias.',
        'class': 'text-center'
    });
    var $itemSuggestions = $('<tr/>').append($description);
    return $itemSuggestions
}

/**
 * Renderisa un tr con un producto para la lista de sugerencias (busqueda).
 * @param {Number} pk
 * @param {Number} code
 * @param {String} description
 * @returns {jQuery}
 */
function renderSuggestions(pk, code, description, brand_name) {
    var $code = $('<td/>', {'text': code});
    var $brand = $('<td/>', {'text': brand_name});
    var $description = $('<td/>', {'text': description});
    var $itemSuggestions = $('<tr/>', {
        'class': 'pointer',
        'data-pk': pk,
        'data-code': code,
        'data-description': description
    }).append($code, $description, $brand);
    $itemSuggestions.on('click', selectSuggestions);
    return $itemSuggestions
}

/**
 * Renderisa un tr con un prodcuto para la lista de seleccion.
 * @param {Number} pk
 * @param {Number} code
 * @param {String} description
 * @returns {jQuery}
 */
function renderProductOption(pk, code, description) {
    var $code = $('<td/>', {'text': code});
    var $description = $('<td/>', {'text': description});
    var $btnRemove = $('<td/>', {'class': 'width-ten-percent'}).append(
        $('<button/>', {
            'type': 'button',
            'class': 'btn btn-danger',
            'text': 'quitar'
        }).on('click', removeProduct));
    var $inputQuantity = $('<td/>').append(
        $('<input/>', {
            'placeholder': 'Cantidad',
            'class': 'form-control input-sticker text-center',
            'type': 'number',
            'value': 1,
            'min': 1,
            'max': 30
        }).on('change', validateStickers));
    var $itemProduct = $('<tr/>', {
        'class': 'tr-product',
        'data-product': pk
    }).append($code, $description, $inputQuantity, $btnRemove);
    return $itemProduct
}

/**
 * Renderisa un ul que se usara como una plantilla de ejemplo, para llevar
 * un conteo visual de las etiquetas.
 */
function renderStickerExample() {
    var size = $(this).val();
    var i;
    var $item;
    var $list = $('<ul/>', {'class': 'ul-sticker'});

    for (i = 0; i < size; i++) {
        $item = $('<li/>', {'class': 'sticker-30', 'text': i + 1});
        $list.append($item);
    }

    $('.template').html('').append($list);
    validateStickers();
}

/**
 * Gestiona una consulta al servidor para buscar productos segun se va
 * escribiendo en el buscador, y mostrara una litado de sugerencias.
 */
function searchProduct(e) {
    var word = $('#buscar_prod').val();
    if (e.keyCode != 27 && word.length > 0) {
        var url = '/api/search/products/' + word + '/';
        var type_method = 'get';
        productAjax(url, type_method, {});
    } else {
        var $counterStatus = renderCounterStatus(-1);
        $('#counter').html('').append($counterStatus);
        $('#search-suggestions').addClass('hidden');
        $('#buscar_prod').val('').focus();
    }
}

/**
 * Gestiona una consulta al servidor para general el pdf con los codigos
 * de los productos seleccionados, y lo muestra en un iframe.
 */
function generatePDF(e) {
    $('.template').html('');
    var preData = new Array();
    $('.tr-product').each(function () {
        preData.push({
            'pk': $(this).data('product'),
            'quantity': Number($(this).find('input').val())
        });
    });
    var procesoData = JSON.stringify(preData);
    var url = '/Codigo/PNG/?products=' + encodeURIComponent(procesoData);

    var $iframe = $('<iframe>', {'class': 'frame-pdf', 'src': url});
    $('.template').append($iframe);
}

/**
 * Realiza la petición al servidor para el modal para producto.
 * @param {string} url: Dirección a la cual se realizara la petición.
 * @param {string} type_method: Tipo de metodo http con el cual se realizara la petición (get/put).
 * @param {object} data_ajax: Datos que se enviaran en la petición.
 */
function productAjax(url, type_method, data_ajax) {
    $.ajax({
        url: url,
        type: type_method,
        data: data_ajax,
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", $('[name=csrfmiddlewaretoken]').val());
            $('#suggestions').html('');
        },
        success: function (data) {
            if (type_method == 'get') {
                $('#search-suggestions').removeClass('hidden');
                var counter = $(data).length;
                var $counterStatus = renderCounterStatus(counter);
                $('#counter').html('').append($counterStatus);
                if (counter > 0) {
                    $.each(data, function (key, item) {
                        var $itemSuggestions = renderSuggestions(item.pk, item.codigo, item.descripcion, item.brand_name);
                        $('#suggestions').append($itemSuggestions);
                    });
                } else {
                    var $itemSuggestions = renderNotMatches();
                    $('#suggestions').append($itemSuggestions);
                }
            }
        },
        error: function (jqXHR) {
            var errors = jqXHR.responseJSON;
            if (jqXHR.status == 404) {
                console.log('no encontrado');
            }
        }
    });
}

$('#buscar_prod').on('keyup', searchProduct);
$('#select-template').on('change', renderStickerExample);
$('#btnPrint').on('click', generatePDF);
