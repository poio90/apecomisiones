$(document).ready(function () {

    /*-----------------------Notifica que el perfil se acualizo correctamente-------------*/
    $(document).on('submit', '#updateProfile', function (e) {
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
    });
    /*------------------------------------------------------------------------------------*/

    /*--------------------Valida DNI------------------------------------------------------*/
    $("#id_dni").change(function () {
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
    })
    /*------------------------------------------------------------------------------------*/

    /*----Desactiva boton Guardar hasta que se completen los campos del formulario--------*/

    SNButton.init("updateButtonProfile", {
        fields: ["id_num_afiliado","id_last_name","id_first_name","id_dni","id_e mail","id_num_tel"],
    })
})