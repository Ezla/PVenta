var datatable = undefined;

/**
 * Dibuja los registros en la tabla (tr) y aplica el cargado de DataTable
 * en la tabla generada.
 * @param {array} products: lista de productos.
 */
function renderListed(products) {
    $('#table-body').html('');
    if (products.length > 0) {
        $.each(products, function (i, item) {
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
            $('#table-body').append($tr);
        });
        datatable = $('#table-listed').DataTable({
            dom: 'Bfrtip',
            "language": {
                "url": "/static/json/tools/datatables/Spanish.json"
            },
            buttons: [
                'csv',
                {
                    extend: 'pdfHtml5',
                    pageSize: 'A4',
                    exportOptions: {
                        columns: [0, 1, 2]
                    },
                },
                {
                    text: 'Re numerar',
                    action: function (e, dt, node, config) {
                        $("#confirmation-modal").modal('show');
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
            }
        },
    });
}

$(document).ready(function () {
    getListed();
    initalModal();
});
