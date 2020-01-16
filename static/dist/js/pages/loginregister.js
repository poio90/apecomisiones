$(document).ready(function () {
    /*--------------------------------control de filiados registrados------------------------------ */
    $("#id_username").change(function () {
        var form = $(this).closest("form");
        var div = document.getElementById("usuario");
        $.ajax({
            url: div.getAttribute("data-validate-username-url"),
            data: form.serialize(),
            dataType: 'json',
            success: function (data) {
                if (data.is_taken) {
                    $("#usuario").notify(data.error_message, { position: 'right' });
                }
            }
        });
    });
    $("#id_num_afiliado").change(function () {
        var form = $(this).closest("form");
        var div = document.getElementById("afiliado");
        $.ajax({
            url: div.getAttribute("data-validate-afiliado-url"),
            data: form.serialize(),
            dataType: 'json',
            success: function (data) {
                if (data.is_taken) {
                    $("#afiliado").notify(data.error_message, { position: 'right' });
                }
            }
        });
    });
    /*------------------------------------------------------------------------------------------- */
})