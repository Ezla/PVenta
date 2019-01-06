var datatable = undefined;
var row = undefined;
var modal_status = undefined;
var item_pk = undefined;
var url_listed = '/api/listed/';

/**
 * Regresa un registro jquey (tr) listo para ser agregado a la tabla.
 * @param {object} item: datos del registro para agregar en al tabla.
 * @returns {jQuery}
 */
function renderRecord(item) {
    var name;
    if (item.type == '1') {
        name = 'Monografía';
    } else if (item.type == '2') {
        name = 'Biografia';
    } else if (item.type == '3') {
        name = 'Mapa';
    }
    var $pk = $('<td/>', {'text': item.pk});
    var $number = $('<td/>', {'text': item.number});
    var $name = $('<td/>', {'text': item.name});
    var $type = $('<td/>', {'text': name});
    var $active = $('<td/>', {'text': item.active});
    var $tr = $('<tr/>', {
        'role': 'button',
        'data-code': item.pk
    }).append($pk, $number, $name, $type, $active);
    return $tr
}

/**
 * Dibuja los registros en la tabla (tr) y aplica el cargado de DataTable
 * en la tabla generada.
 * @param {array} products: lista de productos.
 */
function renderListed(products) {
    $('#table-body').html('');
    if (products.length > 0) {
        $.each(products, function (i, item) {
            var $tr = renderRecord(item);
            $('#table-body').append($tr);
        });
        datatable = $('#table-listed').DataTable({
            dom: 'Bfrtip',
            "language": {
                "url": "/static/json/tools/datatables/Spanish.json"
            },
            buttons: [
                {
                    text: 'Re numerar',
                    action: function (e, dt, node, config) {
                        $("#confirmation-modal").modal('show');
                    }
                },
                'csv',
                {
                    extend: 'pdfHtml5',
                    pageSize: 'A4',
                    exportOptions: {
                        columns: [0, 1, 2]
                    },
                },
                {
                    text: 'Agregar nuevo',
                    action: function (e, dt, node, config) {
                        item_pk = undefined;
                        modal_status = 'post';
                        openModal('', 0, '', true);
                    }
                }
            ],
            pageLength: 100,
            select: true
        });
        $('#table-listed tbody').on('dblclick', 'tr', function () {
            row = datatable.row(this);
            var data = row.data();
            var id_active = (data[4] == 'true');
            var id_type;
            switch (data[3]) {
                case 'Monografía':
                    id_type = 1;
                    break;
                case 'Biografia':
                    id_type = 2;
                    break;
                case 'Mapa':
                    id_type = 3;
                    break;
                default:
                    id_type = '';
            }
            item_pk = data[0];
            modal_status = 'put';
            openModal(data[2], data[1], id_type, id_active);
        });
    } else {
        var $tr = $('<tr/>').append($('<td/>', {
            'text': 'No se encontraron coincidencias'
        }));
        $('#table-body').append($tr);
    }
}

/**
 * Gestiona la peticion para obtener la lista al servidor.
 */
function getListed() {
    runAjax({}, url_listed, 'get');
}

/**
 * Setea los datos en el modal, para abrir el modal.
 * @param {string} name: Nombre del producto.
 * @param {number} number: Numero de lista.
 * @param {number} type: Tipo de producto.
 * @param {boolean} active: Si el producto est activo.
 */
function openModal(name, number, type, active) {
    $('#id_name').val(name);
    $('#id_number').val(number);
    $('#id_type').val(type);
    $('#id_active').prop('checked', active);
    $('#help-name').text('').parent().removeClass('has-error');
    $('#help-number').text('').parent().removeClass('has-error');
    $('#help-type').text('').parent().removeClass('has-error');
    $('#help-active').text('').parent().removeClass('has-error');
    $("#listed-modal").modal('show');
}

/**
 * Inicializa comportamiento del modal.
 */
function initalModal() {
    var modalConfirm = function (callback) {
        $("#modal-btn-si").on("click", function () {
            $("#confirmation-modal").modal('hide');
            callback(true);
        });
        $("#modal-btn-no").on("click", function () {
            $("#confirmation-modal").modal('hide');
            callback(false);
        });
    };
    modalConfirm(function (confirm) {
        if (confirm) {
            reNumberListed();
        }
    });
}

/**
 * Gestiona la peticion para re numerar la lista.
 */
function reNumberListed() {
    $('#table-body').hide();
    $('.loading-container').show();
    runAjax({}, '/api/listed/enumerate/', 'get');
}

/**
 * Gestiona la consulta al servidor para guardar el registro.
 */
function saveListed() {
    var url_modal = url_listed;
    var data = {
        'name': $('#id_name').val(),
        'number': $('#id_number').val(),
        'type': $('#id_type').val(),
        'active': $('#id_active').prop('checked')
    };
    if (modal_status == 'put') {
        url_modal = url_listed.concat(item_pk, '/');
    }
    runAjax(data, url_modal, modal_status);
}

/**
 * Realiza la petición al servidor mediante ajax.
 * @param {object} data: Datos que se enviaran en la petición.
 * @param {string} url: Dirección a la cual se realizara la petición.
 * @param {string} methodType: Tipo de metodo http con el cual se
 * realizara la petición (get/post).
 */
function runAjax(data, url, methodType) {
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
            if (methodType == 'get' && url == url_listed) {
                $('.loading-container').hide();
                renderListed(data);
            } else if (methodType == 'get' && url == '/api/listed/enumerate/') {
                $('.loading-container').hide();
                $('#table-body').show();
                datatable.destroy();
                renderListed(data);
            } else if (methodType == 'post') {
                $("#listed-modal").modal('hide');
                var $newTr = renderRecord(data);
                datatable.row.add($newTr).draw();
            } else if (methodType == 'put') {
                $("#listed-modal").modal('hide');
                var id_type;
                switch (data.type) {
                    case '1':
                        id_type = 'Monografía';
                        break;
                    case '2':
                        id_type = 'Biografia';
                        break;
                    case '3':
                        id_type = 'Mapa';
                        break;
                    default:
                        id_type = '';
                }
                var new_item = [data.pk, data.number, data.name, id_type, data.active];
                row.data(new_item).invalidate();
            }
        },
        error: function (jqXHR) {
            var errors = jqXHR.responseJSON;
            $.each(errors, function(key, msg){
                if (key == 'name') {
                    $('#help-name').text(msg).parent().addClass('has-error');
                } else if (key == 'number') {
                    $('#help-number').text(msg).parent().addClass('has-error');
                } else if (key == 'type') {
                    $('#help-type').text(msg).parent().addClass('has-error');
                } else if (key == 'active') {
                    $('#help-active').text(msg).parent().addClass('has-error');
                }
            });
        }
    });
}

/**
 * Llama el metodo click asociado al botono de agregar producto.
 */
function keyOpenModalListed() {
    item_pk = undefined;
    modal_status = 'post';
    openModal('', 0, '', true);
}

$(document).ready(function () {
    getListed();
    initalModal();
});

$('#guardar').on('click', saveListed);
$(document).on('keydown', null, 'alt+9', keyOpenModalListed);
