var id_product = null;
var method = null;
var url = null;
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
 * Limpia el contenido del formulario para la marca.
 */
function cleanBrandForm() {
    $('#id_marca_modal').val('');
}

/**
 * Limpia el contenido del formulario para el producto.
 */
function cleanProductForm() {
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
 * Inserta los valores del formulario (modal) a la lista de productos.
 * @param {number} pk: Valor del campo a mostrar.
 * @param {string} descripcion: Valor del campo a mostrar.
 * @param {string} marca: Valor del campo a mostrar.
 * @param {boolean} vunidad: Valor del campo a mostrar.
 * @param {number} punitario: Valor del campo a mostrar.
 * @param {number} pmayoreo: Valor del campo a mostrar.
 */
function setList(pk, descripcion, marca, vunidad, punitario, pmayoreo) {
    $('.tr-product').each(function () {
        if ($(this).data('product') == pk) {

            $(this).children('td').eq(0).children('a').text(descripcion);

            $(this).children('td').eq(1).children('strong').text(marca);

            var $icon = $(this).children('td').eq(2).children('i');
            if (vunidad) {
                $($icon).removeClass('fa-thumbs-o-down text-red').addClass('fa-thumbs-o-up text-green');
            } else {
                $($icon).removeClass('fa-thumbs-o-up text-green').addClass('fa-thumbs-o-down text-red');
            }

            $(this).children('td').eq(3).text('$ ' + Number(punitario).toFixed(2));
            $(this).children('td').eq(4).text('$ ' + Number(pmayoreo).toFixed(2));
        }
    })
}

/**
 * Gestiona la consulta al servidor para guardar la informacion de la nueva marca.
 * * @param {event} e: Evento propio del boton al hacer click.
 */
function saveNewBrand(e) {
    e.preventDefault();
    method = 'post';
    var brand = $('#id_marca_modal').val();
    data = {'marca': brand};
    brandAjax(base_url_brand, method, data)
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
            $('#help-marca').text('').parent().removeClass('has-error');
        },
        success: function (data) {
            if (type_method == 'post') {
                $('#myModal').modal('toggle');
                document.getElementById('audio_n').play();
            }
        },
        error: function (jqXHR) {
            var errors = jqXHR.responseJSON;
            $.each(errors, function(key, msg){
                if (key == 'marca') {
                    $('#help-marca').text(msg).parent().addClass('has-error');
                } else  {
                    $('#help-marca').text(msg).parent().addClass('has-error');
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
            } else if (type_method == 'put') {
                var name_marca = $('#marca option:selected').text();
                setList(id_product, data.descripcion, name_marca, data.vunidad, data.punitario, data.pmayoreo);
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
function loadModal() {
    id_product = $(this).data('pk');
    url = base_api_url + id_product + '/';
    method = 'get';
    data = {};

    productAjax(url, method, data);
}

/**
 * Gestiona la consulta al servidor para guardar la informacion del producto modificado.
 */
function saveProduct() {
    url = base_api_url + id_product + '/';
    method = 'put';
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
$('.edit-product').on('click', loadModal);
$('#btnAddBrand').on('click', cleanBrandForm);
$('#btnAddProduct').on('click', cleanProductForm);
$('#guardar').on('click', saveProduct);
$('#btnmarca').on('click', saveNewBrand);
