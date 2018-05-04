var id_product = null;
var method = null;
var url = null;
var type_form = null;
var data = {};

/**
 * Calcula segun el precio unitario, un 10% menos y lo ingresa en el campo de precio al mayoreo.
 */
function calculateDiscount() {
    var price = $('#punitario').val();
    $('#pmayoreo').val(price * 0.9);
}

/**
 * Si el campo "code39" esta seleccionado, el campo "codigo" es habilitado, y viceversa.
 */
function updateStateCode() {
    if ($('#code39').prop('checked')) {
        $('#codigo').prop('disabled', true);
    } else {
        $('#codigo').prop('disabled', false);
    }
}

/**
 * Gestiona la busquea del producto cuando se escribe en el input del codigo.
 * @param {event} e: Evento al teclear una letra.
 */
function searchCodeProduct(e) {
    if (e.keyCode == 13) {
        var code = $('#codigo').val();
        if (code.length >= 10) {
            var url = '/api/search/product/' + code + '/';
            var type_method = 'get';
            searchProductAjax(url, type_method, {})
        }
    }
}

/**
 * Realiza la petición al servidor para para consultar eistencia de un producto.
 * @param {string} url: Dirección a la cual se realizara la petición.
 * @param {string} type_method: Tipo de metodo http con el cual se realizara la petición (get/put).
 * @param {object} data_ajax: Datos que se enviaran en la petición.
 */
function searchProductAjax(url, type_method, data_ajax) {
    $.ajax({
        url: url,
        type: 'get',
        data: {'coigo': 'qwerrtqww'},
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", $('[name=csrfmiddlewaretoken]').val());
        },
        success: function (data) {
            var msg = 'El producto con codigo "' + data.codigo + '" ya existe como el siguiente producto: '+ data.descripcion;
            $('#help-codigo').text(msg).parent().addClass('has-error');
        },
        error: function (jqXHR) {
            if (jqXHR.status == 404) {
                $('#help-codigo').text('').parent().removeClass('has-error');
            }
        }
    });
}

/**
 * Si el campo "inventario" esta seleccionado, los campos "cantidad" y "minimo" son habilitados, y viceversa.
 */
function updateInventario() {
    if ($('#inventario').prop('checked')) {
        $('#cantidad').prop('disabled', false);
        $('#minimo').prop('disabled', false);
    } else {
        $('#cantidad').prop('disabled', true);
        $('#minimo').prop('disabled', true);
    }
}

/**
 * Inserta nuevas opciones en el select de marcas (modal) segun la lista enviada.
 * @param {object} brands: Lista de marcas.
 */
function setBrans(brands) {
    // removemos antiguas opciones
    $('#marca option').remove();

    // inserta nuevas opciones enviadas
    $.each(brands, function (key, item) {
        var option = $('<option/>', {
            'value': item.pk,
            'text': item.marca
        });
        $('#marca').append(option);
    });
}

/**
 * Gestiona la consulta al servidor para cargar la informacion de todas las marcas.
 */
function loadBrands() {
    method = 'get';
    data = {};
    brandAjax(base_url_brand, method, data)
}

/**
 * Limpia el contenido del formulario para la marca.
 */
function cleanBrandForm() {
    $('#id_marca_modal').val('');

    // Quita mensaje de error en campo del formulario si es que lo tiene
    $('#help-marca-name').text('').parent().removeClass('has-error');
}

/**
 * Limpia el contenido del formulario para el producto.
 */
function cleanProductForm() {
    type_form = 'post';

    // limpiamos contenido del formulario
    $('#code39').prop('checked', false);
    $('#vunidad').prop('checked', false);
    $('#inventario').prop('checked', false);
    $('#codigo').val('');
    $('#descripcion').val('');
    $('#punitario').val('');
    $('#pmayoreo').val('');
    $('#cantidad').val('');
    $('#minimo').val('');
    $('#marca').val('');

    // actualiza estado de campos (enable / disable)
    updateStateCode();
    updateInventario();

    // Quita mensaje de error en campo del formulario si es que lo tiene
    $('#help-codigo').text('').parent().removeClass('has-error');
    $('#help-descripcion').text('').parent().removeClass('has-error');
    $('#help-marca').text('').parent().removeClass('has-error');
    $('#help-punitario').text('').parent().removeClass('has-error');
    $('#help-pmayoreo').text('').parent().removeClass('has-error');
    $('#help-cantidad').text('').parent().removeClass('has-error');
    $('#help-minimo').text('').parent().removeClass('has-error');
}

/**
 * Inserta los valores proporcionados a los campos correspondientes del formulario (modal).
 * @param {boolean} code39: Valor del campo a mostrar.
 * @param {string} codigo: Valor del campo a mostrar.
 * @param {string} descripcion: Valor del campo a mostrar.
 * @param {boolean} vunidad: Valor del campo a mostrar.
 * @param {number} punitario: Valor del campo a mostrar.
 * @param {number} pmayoreo: Valor del campo a mostrar.
 * @param {boolean} inventario: Valor del campo a mostrar.
 * @param {number} cantidad: Valor del campo a mostrar.
 * @param {number} minimo: Valor del campo a mostrar.
 * @param {number} marca: Valor del campo a mostrar.
 */
function setForm(code39, codigo, descripcion, vunidad, punitario, pmayoreo, inventario, cantidad, minimo, marca) {
    $('#code39').prop('checked', code39);
    $('#vunidad').prop('checked', vunidad);
    $('#inventario').prop('checked', inventario);
    $('#codigo').val(codigo);
    $('#descripcion').val(descripcion);
    $('#punitario').val(punitario);
    $('#pmayoreo').val(pmayoreo);
    $('#cantidad').val(cantidad);
    $('#minimo').val(minimo);
    $('#marca').val(marca);

    // actualiza estado de campos (enable / disable)
    updateStateCode();
    updateInventario();
}

/**
 * Regresa un renglon (tr) que mostrara el registro del producto para que el usuario pueda interactuar con el.
 * @param {number} pk: Valor del campo a mostrar.
 * @param {string} descripcion: Valor del campo a mostrar.
 * @param {string} marca: Valor del campo a mostrar.
 * @param {boolean} vunidad: Valor del campo a mostrar.
 * @param {number} punitario: Valor del campo a mostrar.
 * @param {number} pmayoreo: Valor del campo a mostrar.
 * @returns {jQuery}: Objeto del DOM.
 */
function createVisualProuct(pk, descripcion, marca, vunidad, punitario, pmayoreo) {
    var classSale = 'fa f fa-thumbs-o-down text-red';
    if (vunidad){
        classSale = 'fa f fa-thumbs-o-up text-green';
    }
    var $description = $('<td/>').append($('<a/>', {
        'class': 'btn btn-default btn-sm btn-block',
        'href': '/Producto/Consultar/' + pk +'/',
        'title': 'Ver detalles del producto.',
        'text': descripcion
    }));
    var $brand = $('<td/>', {
        'class': 'hidden-xs'
    }).append($('<strong/>', {
        'class': 'btn btn-primary btn-xs btn-block',
        'text': marca
    }));
    var $salePerUnit = $('<td/>', {
        'class': 'hidden-xs text-center'
    }).append($('<i/>', {
        'class': classSale
    }));
    var $unitPriece = $('<td/>', {
        'class': 'hidden-xs',
        'text': '$ ' + punitario
    });
    var $wholesalePrice = $('<td/>', {
        'class': 'hidden-xs',
        'text': '$ ' + pmayoreo
    });
    var $editProduct = $('<td/>').append($('<div/>', {
        'class': 'btn-group pull-right'
    }).append($('<button/>', {
        'type': 'button',
        'class': 'btn btn-primary edit-product',
        'data-toggle': 'modal',
        'data-target': '#exampleModal',
        'data-pk': pk,
        'text': 'Editar'
    }).on('click', loadProductForm)));
    var $itemProduct = $('<tr/>', {
        'class': 'tr-product',
        'data-product': pk}).append($description, $brand, $salePerUnit, $unitPriece, $wholesalePrice, $editProduct);
    return $itemProduct;
}

/**
 * Gestiona la consulta al servidor para guardar la informacion de la nueva marca.
 * @param {event} e: Evento propio del boton al hacer click.
 */
function saveNewBrand(e) {
    e.preventDefault();
    method = 'post';
    var brand = $('#id_marca_modal').val();
    data = {'marca': brand};
    brandAjax(base_url_brand, method, data);
}

/**
 * Realiza la petición al servidor para el modal para marca.
 * @param {string} url: Dirección a la cual se realizara la petición.
 * @param {string} type_method: Tipo de metodo http con el cual se realizara la petición (get/put).
 * @param {object} data_ajax: Datos que se enviaran en la petición.
 */
function brandAjax(url, type_method, data_ajax) {
    $.ajax({
        url: url,
        type: type_method,
        data: data_ajax,
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", $('[name=csrfmiddlewaretoken]').val());
            $('#help-marca-name').text('').parent().removeClass('has-error');
        },
        success: function (data) {
            if (type_method == 'get') {
                setBrans(data);
            } else if (type_method == 'post') {
                $('#myModal').modal('toggle');
                document.getElementById('audio_n').play();
                loadBrands();
            }
        },
        error: function (jqXHR) {
            var errors = jqXHR.responseJSON;
            $.each(errors, function(key, msg){
                if (key == 'marca') {
                    $('#help-marca-name').text(msg).parent().addClass('has-error');
                } else  {
                    $('#help-marca-name').text(msg).parent().addClass('has-error');
                }
            });
        }
    });
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
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", $('[name=csrfmiddlewaretoken]').val());
            $('#help-codigo').text('').parent().removeClass('has-error');
            $('#help-descripcion').text('').parent().removeClass('has-error');
            $('#help-marca').text('').parent().removeClass('has-error');
            $('#help-punitario').text('').parent().removeClass('has-error');
            $('#help-pmayoreo').text('').parent().removeClass('has-error');
            $('#help-cantidad').text('').parent().removeClass('has-error');
            $('#help-minimo').text('').parent().removeClass('has-error');
        },
        success: function (data) {
            if (type_method == 'get') {
                setForm(data.code39, data.codigo, data.descripcion, data.vunidad, data.punitario, data.pmayoreo, data.inventario, data.cantidad, data.minimo, data.marca);
            } else if (type_method == 'post') {
                var name_marca = $('#marca option:selected').text();
                $('tbody').prepend(createVisualProuct(data.pk, data.descripcion, name_marca, data.vunidad, data.punitario, data.pmayoreo));
                $('#exampleModal').modal('toggle');
                document.getElementById('audio_n').play();
            } else if (type_method == 'put') {
                var name_marca = $('#marca option:selected').text();
                var $visual_product = createVisualProuct(id_product, data.descripcion, name_marca, data.vunidad, data.punitario, data.pmayoreo);
                var tr = 'tr[data-product="' + id_product + '"]';
                var $prev_tr = $(tr).prev();
                $(tr).remove();
                $($prev_tr).after($visual_product);
                $('#exampleModal').modal('toggle');
                document.getElementById('audio_n').play();
            }
        },
        error: function (jqXHR) {
            var errors = jqXHR.responseJSON;
            $.each(errors, function(key, msg){
                if (key == 'codigo') {
                    $('#help-codigo').text(msg).parent().addClass('has-error');
                } else if (key == 'descripcion') {
                    $('#help-descripcion').text(msg).parent().addClass('has-error');
                }else if (key == 'marca') {
                    $('#help-marca').text(msg).parent().addClass('has-error');
                }else if (key == 'punitario') {
                    $('#help-punitario').text(msg).parent().addClass('has-error');
                }else if (key == 'pmayoreo') {
                    $('#help-pmayoreo').text(msg).parent().addClass('has-error');
                }else if (key == 'cantidad') {
                    $('#help-cantidad').text(msg).parent().addClass('has-error');
                }else if (key == 'minimo') {
                    $('#help-minimo').text(msg).parent().addClass('has-error');
                }
            });
        }
    });
}

/**
 * Gestiona la consulta al servidor para cargar la informacion del producto a modificar.
 */
function loadProductForm() {
    type_form = 'put';
    id_product = $(this).data('pk');
    url = base_api_url + id_product + '/';
    method = 'get';
    data = {};

    productAjax(url, method, data);
}

/**
 * Gestiona la consulta al servidor para guardar la informacion del producto.
 */
function saveProduct() {
    // configuramos el tipo de gruardado
    if (type_form == 'put') {
        url = base_api_url + id_product + '/';
        method = 'put';
    } else {
        url = base_api_url;
        method = 'post';
    }

    data = {
        "code39": $('#code39').prop('checked'),
        "codigo": $('#codigo').val(),
        "descripcion": $('#descripcion').val(),
        "vunidad": $('#vunidad').prop('checked'),
        "punitario": $('#punitario').val(),
        "pmayoreo": $('#pmayoreo').val(),
        "inventario": $('#inventario').prop('checked'),
        "cantidad": $('#cantidad').val(),
        "minimo": $('#minimo').val(),
        "marca": $('#marca').val()
    };

    productAjax(url, method, data);
}

$('#code39').on('change', updateStateCode);
$('#calculate').on('click', calculateDiscount);
$('#inventario').on('change', updateInventario);
$('.edit-product').on('click', loadProductForm);
$('#btnAddBrand').on('click', cleanBrandForm);
$('#btnAddProduct').on('click', cleanProductForm);
$('#codigo').on('keyup', searchCodeProduct);
$('#guardar').on('click', saveProduct);
$('#btnmarca').on('click', saveNewBrand);
