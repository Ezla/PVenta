    var $codigo = $('#codigo');
        $tablaVenta = $('#tVentaProd');
        $totalVenta = $('.total');
        $efectivo = $('#efectivo');
        $btnefectivo = $('#btnefectivo');
        $mensaje = $('#mensaje');
        $tprecio = $('#btx');
        chbT = '<div class="btn-group" data-toggle="buttons"><label class="btn btx btn-xs btn-success active"> <input type="checkbox" autocomplete="off" checked><span class="glyphicon glyphicon-ok"></span> </label></div>';
        chbF = '<div class="btn-group" data-toggle="buttons"><label class="btn btx btn-xs btn-success"> <input type="checkbox" autocomplete="off"><span class="glyphicon glyphicon-ok"></span> </label></div>';
        //funciones
        function Cancelar(e){
            $.ajax({
                async : false,
                url : '{% url "Venta:url_cancelar_cuenta_ajax" %}',
                type : 'get',
                success : function(data){
                    $tablaVenta.html('');
                    $totalVenta.html('$ 0');
                }
            });
            $codigo.focus();
        }

        function AumentarFil(e){
        	var parent = $(this).parent().parent().parent().html();
            var cod = $(parent).html();
            $.ajax({
                async: false,
                data : {'cod': cod},
                url : '{% url "Venta:url_aumentar_prod_ajax" %}',
                type : 'get',
                success : function(data){
                    var htmlp = '';
                    $.each(data.cuenta, function(i, item){
                        if(item.tprecio== false) {
                            htmlp = htmlp + '<tr class="info"><td class="cod">' + item.codigo + '</td><td title="' + item.descripcion + '">' + item.descripcion.slice(0,35) + '</td><td>' + item.punitario + '</td><td>'+chbF+'</td><td><div class="btn-group btn-group-xs"><button type="button" class="btn btn-success btn-xs aumentar"><span class="glyphicon glyphicon-plus-sign"></span></button><button class="btn btn-info">' + item.cantidad + '</button><button type="button" class="btn btn-warning btn-xs eliminar pull-right"><span class="glyphicon glyphicon-minus-sign"></span></button></div></td></tr>'
                        }else{
                            htmlp = htmlp + '<tr class="info"><td class="cod">' + item.codigo + '</td><td title="' + item.descripcion + '">' + item.descripcion.slice(0,35) + '</td><td>' + item.pmayoreo + '</td><td>'+chbT+'</td><td><div class="btn-group btn-group-xs"><button type="button" class="btn btn-success btn-xs aumentar"><span class="glyphicon glyphicon-plus-sign"></span></button><button class="btn btn-info">' + item.cantidad + '</button><button type="button" class="btn btn-warning btn-xs eliminar pull-right"><span class="glyphicon glyphicon-minus-sign"></span></button></div></td></tr>'
                        }
                    });
                    $tablaVenta.html(htmlp);
                    $totalVenta.html("$ "+ data.precio)
                }
            });
            $codigo.focus();
        }

        function EliminarFil(e){
        	var parent = $(this).parent().parent().parent().html();
            var cod = $(parent).html();
            $.ajax({
                async: false,
                data : {'cod': cod},
                url : '{% url "Venta:url_remover_prod_ajax" %}',
                type : 'get',
                success : function(data){
                    var htmlp = ''
                    $.each(data.cuenta, function(i, item){
                        if(item.tprecio== false) {
                            htmlp = htmlp + '<tr class="info"><td class="cod">' + item.codigo + '</td><td title="' + item.descripcion + '">' + item.descripcion.slice(0,35) + '</td><td>' + item.punitario + '</td><td>'+chbF+'</td><td><div class="btn-group btn-group-xs"><button type="button" class="btn btn-success btn-xs aumentar"><span class="glyphicon glyphicon-plus-sign"></span></button><button class="btn btn-info">' + item.cantidad + '</button><button type="button" class="btn btn-warning btn-xs eliminar pull-right"><span class="glyphicon glyphicon-minus-sign"></span></button></div></td></tr>'
                        }else{
                            htmlp = htmlp + '<tr class="info"><td class="cod">' + item.codigo + '</td><td title="' + item.descripcion + '">' + item.descripcion.slice(0,35) + '</td><td>' + item.pmayoreo + '</td><td>'+chbT+'</td><td><div class="btn-group btn-group-xs"><button type="button" class="btn btn-success btn-xs aumentar"><span class="glyphicon glyphicon-plus-sign"></span></button><button class="btn btn-info">' + item.cantidad + '</button><button type="button" class="btn btn-warning btn-xs eliminar pull-right"><span class="glyphicon glyphicon-minus-sign"></span></button></div></td></tr>'
                        }
                    });
                    $tablaVenta.html(htmlp);
                    $totalVenta.html("$ "+ data.precio)
                }
            });
            $codigo.focus();
        }

        function TipoPre(e){
        	var parent = $(this).parent().parent().parent().html();
            var cod = $(parent).html();
            $.ajax({
                async: false,
                data : {'cod': cod},
                url : '{% url "Venta:url_tipo_precio_ajax" %}',
                type : 'get',
                success : function(data){
                    var htmlp = ''
                    $.each(data.cuenta, function(i, item){
                        if(item.tprecio== false) {
                            htmlp = htmlp + '<tr class="info"><td class="cod">' + item.codigo + '</td><td title="' + item.descripcion + '">' + item.descripcion.slice(0,35) + '</td><td>' + item.punitario + '</td><td>'+chbF+'</td><td><div class="btn-group btn-group-xs"><button type="button" class="btn btn-success btn-xs aumentar"><span class="glyphicon glyphicon-plus-sign"></span></button><button class="btn btn-info">' + item.cantidad + '</button><button type="button" class="btn btn-warning btn-xs eliminar pull-right"><span class="glyphicon glyphicon-minus-sign"></span></button></div></td></tr>'
                        }else{
                            htmlp = htmlp + '<tr class="info"><td class="cod">' + item.codigo + '</td><td title="' + item.descripcion + '">' + item.descripcion.slice(0,35) + '</td><td>' + item.pmayoreo + '</td><td>'+chbT+'</td><td><div class="btn-group btn-group-xs"><button type="button" class="btn btn-success btn-xs aumentar"><span class="glyphicon glyphicon-plus-sign"></span></button><button class="btn btn-info">' + item.cantidad + '</button><button type="button" class="btn btn-warning btn-xs eliminar pull-right"><span class="glyphicon glyphicon-minus-sign"></span></button></div></td></tr>'
                        }
                    });
                    $tablaVenta.html(htmlp);
                    $totalVenta.html("$ "+ data.precio)
                }
            });
            $codigo.focus();
        }

        function Buscarpro(e){
            var dato = $codigo.val();
            $.ajax({
                async: false,
            	data : {'cod': dato},
            	url : '{% url "Venta:url_buscar_ajax" %}',
            	type : 'get',
            	success: function(data){
                    var htmlp = '';
                    var cont = 0;
                    $.each(data.cuenta, function(i, item){
                        if(cont == 0){
                            cont = 1;
                            if(item.tprecio== false) {
                                htmlp = htmlp + '<tr class="success loading"><td class="cod">' + item.codigo + '</td><td title="' + item.descripcion + '">' + item.descripcion.slice(0,35) + '</td><td>' + item.punitario + '</td><td>'+chbF+'</td><td><div class="btn-group btn-group-xs"><button type="button" class="btn btn-success btn-xs aumentar"><span class="glyphicon glyphicon-plus-sign"></span></button><button class="btn btn-info">' + item.cantidad + '</button><button type="button" class="btn btn-warning btn-xs eliminar pull-right"><span class="glyphicon glyphicon-minus-sign"></span></button></div></td></tr>'
                            }else{
                                htmlp = htmlp + '<tr class="success loading"><td class="cod">' + item.codigo + '</td><td title="' + item.descripcion + '">' + item.descripcion.slice(0,35) + '</td><td>' + item.pmayoreo + '</td><td>'+chbT+'</td><td><div class="btn-group btn-group-xs"><button type="button" class="btn btn-success btn-xs aumentar"><span class="glyphicon glyphicon-plus-sign"></span></button><button class="btn btn-info">' + item.cantidad + '</button><button type="button" class="btn btn-warning btn-xs eliminar pull-right"><span class="glyphicon glyphicon-minus-sign"></span></button></div></td></tr>'
                            }

                        }else{
                            if(item.tprecio== false) {
                                htmlp = htmlp + '<tr class="info"><td class="cod">' + item.codigo + '</td><td title="' + item.descripcion + '">' + item.descripcion.slice(0,35) + '</td><td>' + item.punitario + '</td><td>'+chbF+'</td><td><div class="btn-group btn-group-xs"><button type="button" class="btn btn-success btn-xs aumentar"><span class="glyphicon glyphicon-plus-sign"></span></button><button class="btn btn-info">' + item.cantidad + '</button><button type="button" class="btn btn-warning btn-xs eliminar pull-right"><span class="glyphicon glyphicon-minus-sign"></span></button></div></td></tr>'
                            }else{
                                htmlp = htmlp + '<tr class="info"><td class="cod">' + item.codigo + '</td><td title="' + item.descripcion + '">' + item.descripcion.slice(0,35) + '</td><td>' + item.pmayoreo + '</td><td>'+chbT+'</td><td><div class="btn-group btn-group-xs"><button type="button" class="btn btn-success btn-xs aumentar"><span class="glyphicon glyphicon-plus-sign"></span></button><button class="btn btn-info">' + item.cantidad + '</button><button type="button" class="btn btn-warning btn-xs eliminar pull-right"><span class="glyphicon glyphicon-minus-sign"></span></button></div></td></tr>'
                            }
                        }




                    });
                    $tablaVenta.html(htmlp);
                    $totalVenta.html("$ "+ data.precio);

            	}
            });
            $codigo.val('').focus();
            return false;
        }

        function Pagar(e){
            var dato = $efectivo.val();
            $efectivo.prop('disabled', true);
            $btnefectivo.prop('disabled', true);
            $.ajax({
                async : false,
                data : {'efectivo': dato},
                url : {% url "Venta:url_pagar" %},
                type : 'get',
                success : function(data){
                    $efectivo.val('');
                    $efectivo.focus();
                    if(data.tipo == true){
                        var html = '<div class="alert alert-success alert-dismissable">' +
                                '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">' +
                                '×</button>'+
                                '<table class="table table-hover"><tr><td><strong>Total: $ ' + data.total + '</strong></td><td><strong>Efectivo: $ ' + data.efectivo + '</strong></td><td><strong>Cambio: $ ' + data.cambio + '</strong></td></tr></table>' +
                                '<strong>¡Completado!</strong> '+ data.mensaje +'</div>'
                        $tablaVenta.html('');
                        $totalVenta.html('$ 0');
                    }else{
                        var html = '<div class="alert alert-warning alert-dismissable">' +
                                '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">' +
                                '×</button> <strong>¡Cuidado!</strong> '+data.mensaje+'</div>';
                    }

                    $mensaje.html(html);
                    $mensaje.fadeIn().delay(20000).fadeOut();
                    tiempo = setTimeout(function(){
                        $efectivo.prop('disabled', false);
                        $btnefectivo.prop('disabled', false);
                        $efectivo.focus();
                        },10000);

                }
            });
            return false;
        }
        function focus(e){
            $efectivo.delay(2000).focus();
            //return false;
        }
        //Eventos

	    $(document).ready($codigo.focus());

        $('#cancelar').on('click', Cancelar);

        $('#pagar_cuenta').on('click', focus);

        $tablaVenta.on('click', '.aumentar', AumentarFil);

        $tablaVenta.on('click', '.eliminar', EliminarFil);

        $tablaVenta.on('click', '.btx', TipoPre);

        $('#formxD').on('submit',Buscarpro);

        $('#formPago').on('submit',Pagar);
