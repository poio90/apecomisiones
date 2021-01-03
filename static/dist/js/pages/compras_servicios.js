$(document).ready(function () {

    const $divID = $('#form-wrapper');

    $('#requerido-add').on('click', () => {
        var form = document.querySelector('#id_detallerequerido_set-TOTAL_FORMS');
        const newTr = `<div class="form-row">
                    <div class="d-none d-print-block">
                    <input type="hidden" name="detallerequerido_set-`+ form.value + `-id_detalle" 
                        id="id_detallerequerido_set-`+ form.value + `-id_detalle">
                    </div>
                    <div class="col-md-6 mt-2">
                    <input type="text" name="detallerequerido_set-`+ form.value + `-detalle_requerido" maxlength="200" 
                        class="form-control" placeholder="Detalle de lo requerido" id="id_detallerequerido_set-`+ form.value + `-detalle_requerido">
                    </div>
                    <div class="col-md-5 mt-2">
                    <input type="number" name="detallerequerido_set-`+ form.value + `-monto" step="any" class="form-control" 
                        placeholder="Monto" id="id_detallerequerido_set-`+ form.value + `-monto">
                    </div>
                    <div class="col-md-1 mt-2">
                        <span class="d-none d-print-block">
                            <input type="checkbox" name="detallerequerido_set-0-DELETE" id="id_detallerequerido_set-`+ form.value + `-DELETE">
                        </span>
                        <span>
                            <button type="button" class="requerido-remove btn btn-danger btn-block">Quitar</button>
                        </span>
                    </div>
                </div>`

        form.value = parseInt(form.value) + 1;
        $divID.find('#form-repaet').append(newTr);
    });

    $divID.on('click', '.requerido-remove', function () {
        $(this).parents('.form-row').find('input[type="checkbox"]').attr('checked', true);
        $(this).parents('.form-row').hide();
    });

    $('#id_vehículo').on('change', function () {
        if ($(this).is(':checked')) {
            $("#id_rep_vehículo").prop("disabled", false);
            $("#id_transporte").prop("disabled", false);
            $("#id_transporte").prop("required", true);
        } else {
            $("#id_rep_vehículo").prop("disabled", true);
            $("#id_rep_vehículo").val("")
            $("#id_transporte").prop("disabled", true);
            $('#id_transporte').val(null).trigger('change');
        }
    });

});