var datatable = undefined;

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
    var $number = $('<td/>', {'text': item.number});
    var $name = $('<td/>', {'text': item.name});
    var $type = $('<td/>', {'text': name});
    var $active = $('<td/>', {'text': item.active});
    var $tr = $('<tr/>', {
        'role': 'button',
        'data-code': item.pk
    }).append($number, $name, $type, $active);
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
                        $('#id_name').val('');
                        $('#id_number').val(0);
                        $('#id_type').val('');
                        $('#id_active').prop('checked', true);
                        $('#help-name').text('').parent().removeClass('has-error');
                        $('#help-number').text('').parent().removeClass('has-error');
                        $('#help-type').text('').parent().removeClass('has-error');
                        $('#help-active').text('').parent().removeClass('has-error');
                        $("#listed-modal").modal('show');
                    }
                }
            ],
            pageLength: 100,
            select: true
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
    runAjax({}, '/api/listed/', 'get');
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
    var data = {
        'name': $('#id_name').val(),
        'number': $('#id_number').val(),
        'type': $('#id_type').val(),
        'active': $('#id_active').prop('checked')
    };
    runAjax(data, '/api/listed/', 'post');
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
            if (methodType == 'get' && url == '/api/listed/') {
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

$(document).ready(function () {
    getListed();
    initalModal();
});

$('#guardar').on('click', saveListed);
