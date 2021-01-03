$(document).ready(function () {


    $('#id_reemplazo').on('change', function () {
        if ($(this).is(':checked')) {
            $("#id_categoria_reemplazo").prop("disabled", false);
        } else {
            $("#id_categoria_reemplazo").prop("disabled", true);
            $('#id_categoria_reemplazo').val(null).trigger('change');
        }
    });

    /*-----------------------Notifica que el perfil se acualizo correctamente-------------*/
    /*$(document).on('submit', '#updateProfile', function (e) {
        e.preventDefault();
        var form = $(this).closest("form");
        $.ajax({
            url: form.attr("data-update-profile-url"),
            type: 'POST',
            data: form.serialize(),
            dataType: 'json',
            success: function (data) {
                if (data.is_taken) {
                    $.notify.defaults({ globalPosition: 'bottom right', autoHideDelay: 3000 });
                    $.notify(data.error_message);

                }else{
                    $.notify.defaults({ globalPosition: 'bottom right', autoHideDelay: 3000 });
                    $.notify(data.success_message, "success");
                }
            }
        });
    });*/
    /*------------------------------------------------------------------------------------*/

    /*--------------------Valida DNI------------------------------------------------------*/
    /*$("#id_dni").change(function () {
        var form = $(this).closest("form");
        var div = document.getElementById("dni_label");
        var ex_regular_dni;
        ex_regular_dni = /^\d{8}(?:[-\s]\d{4})?$/;
        console.log(document.getElementById("id_dni").value);
        if (ex_regular_dni.test(document.getElementById("id_dni").value) == true) {
            $.ajax({
                url: div.getAttribute("data-validate-dni-url"),
                data: form.serialize(),
                dataType: 'json',
                success: function (data) {
                    if (data.is_taken) {
                        $("#id_dni").notify(data.error_message, { position: 'bottom left' });
                    }
                }
            });
        } else {
            $("#id_dni").notify('Dni erroneo, formato no válido', { position: 'bottom left' });
        }
    })*/
    /*------------------------------------------------------------------------------------*/
})