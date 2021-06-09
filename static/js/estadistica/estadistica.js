function loadInvoiceForm() {
    // Cargamos formualrio para editar
}

function renderInvoice(pk, folio, provider, amount, status, invoice_date, settlement_date){
    var $folio = $('<td/>').append($('<strong/>', {'text': folio}));
    var $provider = $('<td/>').append($('<strong/>', {'text': provider}));
    var $amount = $('<td/>').append($('<strong/>', {'text': '$ ' + amount}));
    var $status = $('<td/>', {'text': status});
    var $invoice_date = $('<td/>', {
        'class': 'hidden-xs',
        'text': invoice_date
    });
    var $settlement_date = $('<td/>', {
        'class': 'hidden-xs',
        'text': settlement_date
    });
    var $editInvoice = $('<td/>').append($('<div/>', {
        'class': 'btn-group pull-right'
    }).append($('<button/>', {
        'type': 'button',
        'class': 'btn btn-primary edit-invoice',
        'data-toggle': 'modal',
        'data-target': '#exampleModal',
        'data-pk': pk,
        'text': 'Editar'
    }).on('click', loadInvoiceForm)));
    var $itemInvoice = $('<tr/>', {
        'class': 'tr-invoice',
        'data-invoice': pk}).append($folio,$provider, $amount, $status, $invoice_date, $settlement_date, $editInvoice);
    return $itemInvoice;
}

function load_invoices() {
    var type_method = 'get';
    invoiceAjax(url_invoice, type_method, {});
}


/**
 * Realiza la petición al servidor para el modal de facturas.
 * @param {string} url: Dirección a la cual se realizara la petición.
 * @param {string} type_method: Tipo de metodo http con el cual se realizara la petición (get/put).
 * @param {object} data_ajax: Datos que se enviaran en la petición.
 */
function invoiceAjax(url, type_method, data_ajax) {
    $.ajax({
        url: url,
        type: type_method,
        data: data_ajax,
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", $('[name=csrfmiddlewaretoken]').val());
            $('.loading-container').removeClass('hidden');
        },
        success: function (data) {
            $('.loading-container').addClass('hidden');
            if (type_method == 'get') {
                $.each(data, function (index, item) {
                    var $invoice = renderInvoice(item.pk, item.folio,
                        item.provider_name, item.amount, item.status_name,
                        item.invoice_date,
                        item.settlement_date);
                    $('#list-invoices').append($invoice);
                });
                renderInvoice(data);
            } 
        },
        error: function (jqXHR) {
            $('.loading-container').addClass('hidden');
            var errors = jqXHR.responseJSON;
        }
    });
}
