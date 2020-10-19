$(document).ready(function () {

    /*$('#myform').on("change","select", function (e) {
        var form = $(this).closest("select")
        var id = this.id;
        var div = document.getElementById('after-add-more');
        console.log(form[0].getAttribute('id'));
        $.ajax({
            url: div.getAttribute("data-validate-afiliado-url"),
            data: form.serialize(),
            dataType: 'json',
            success: function (data) {
                $('#afiliado' + id).val(data.data[0].num_afiliado);
                $("").parent().children("input[name='" + data.name + "']").val(text);
            }
        });
    })*/



    $('.form-repaet').on('select2:select', function (e) {
        var data = e.params.data;
        var form = $(this)
        var id = e.target.attributes
        //var div = document.getElementById('after-add-more');
        console.log(e.target);
        /*$.get(div.getAttribute("data-validate-afiliado-url"),{ pk : data.element.value}, function(response){
            $('#afiliado' + id).val(response.data[0].num_afiliado);
        })*/
    });

    /*$('#after-add-more select').each(function () {
        $(this).select2({
            theme: 'bootstrap4',
            width: $(this).data('width') ? $(this).data('width') : $(this).hasClass('w-100') ? '100%' : 'style',
            placeholder: $(this).data('placeholder'),
            allowClear: Boolean($(this).data('allow-clear')),
        });
    });*/

    $('.sel').each(function () {
        $(this).select2({
            theme: 'bootstrap4',
            width: $(this).data('width') ? $(this).data('width') : $(this).hasClass('w-100') ? '100%' : 'style',
            placeholder: $(this).data('placeholder'),
            allowClear: Boolean($(this).data('allow-clear')),
        });
    });

    $("#transporte").change(function () {
        var form = $(this).closest("#transporte");
        var div = document.getElementById(this.id);
        $.get(div.getAttribute("data-validate-transporte-url"), form.serialize(), function (response) {
            $('#patente').val(response.data[0].patente);
        })
    })


    $('input[name="km_salida"]').change(function () {
        var km_salida = $(this).val()
        var km_llegada = $('input[name="km_llegada"]').val()
        if (km_llegada == 0) {
            $('input[name="km_total"]').val(km_salida);
        } else {
            $('input[name="km_total"]').val(km_llegada - km_salida);
        }
    })

    $('input[name="km_llegada"]').change(function () {
        var km_llegada = $(this).val();
        var km_salida = $('input[name="km_salida"]').val();
        if (km_salida == 0) {
            $('input[name="km_total"]').val(km_llegada);
        } else {
            $('input[name="km_total"]').val(km_llegada - km_salida);
        }
    })

    /* Función que muestra mensaje de error en alertas */
    function message_error(obj) {
        var html = '';
        $.each(obj, function (key, value) {
            html += value;
        })

        swal.fire({
            title: 'Oops...!',
            text: html,
            icon: 'error',
            allowOutsideClick: false,
            allowEscapeKey: false,
            allowEnterKey: false,
        });
    }

    /* Estilos de los botones cuando pregunta si desea imprimir el docuemnto*/
    const swalWithBootstrapButtons = swal.mixin({
        customClass: {
            confirmButton: 'btn btn-success ml-2',
            cancelButton: 'btn btn-danger mr-2'
        },
        buttonsStyling: false
    })

    $('#myform').on('submit', function (e) {
        e.preventDefault();
        var parametros = $(this).serializeArray();
        var div = document.getElementById(this.id);
        if ($(".form-repaet")[0].children.length > 0) {
            $.ajax({
                url: div.getAttribute("data-validate-url"),
                type: 'POST',
                data: parametros,
                dataType: 'json',
            }).done(function (data) {
                /** mas adelante acomodar todo en una sola función */
                if (!data.hasOwnProperty('pdf_url')) {
                    message_error(data)
                } else {
                    var url = '';
                    $.each(data, function (key, value) {
                        url += value;
                    })
                    swalWithBootstrapButtons.fire({
                        title: 'Solicitud de anticipo creada con exito!',
                        text: "Desea imprimir el documento?",
                        icon: 'success',
                        showCancelButton: true,
                        confirmButtonText: 'Si',
                        cancelButtonText: 'No',
                        reverseButtons: true
                    }).then((result) => {
                        if (result.isConfirmed) {
                            window.open(url);
                            window.location.href = div.getAttribute("data-url")
                        } else if (
                            /* Read more about handling dismissals below */
                            result.dismiss === Swal.DismissReason.cancel
                        ) {
                            window.location.href = div.getAttribute("data-url")
                        }
                    })
                }

            })
        } else {
            swal.fire({
                title: 'Oops...!',
                text: 'Lista de usuarios vacía',
                icon: 'error',
                allowOutsideClick: false,
                allowEscapeKey: false,
                allowEnterKey: false,
            });
        }
    })

});