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
        $('#table-listed').DataTable({
            "language": {
                "url": "/static/json/tools/datatables/Spanish.json"
            }
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
    runAjax({}, '/api/listed/', 'get')
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
            if (methodType == 'get') {
                $('.loading-container').hide();
                renderListed(data);
            }
        },
    });
}

$(document).ready(function () {
    getListed();
});
