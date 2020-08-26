$(document).ready(function () {

    //$('#date_inicio').inputmask("dd/mm/yyyy");  //static mask
    $('#date_inicio').inputmask({ "mask": "99/99/9999", "placeholder": "dd/mm/yyyy"}); //specifying options
    //$('#date_inicio').inputmask("9-a{1,3}9{1,3}"); //mask with dynamic syntax

    $('#date_fin').inputmask({ "mask": "99/99/9999" , "placeholder": "dd/mm/yyyy"}); //specifying options
    $('#date_reintegro').inputmask({ "mask": "99/99/9999", "placeholder": "dd/mm/yyyy" }); //specifying options

    $('input[name=fech_inicio]').on('change', function () {
        var fecha = new Date($(this).val());
        var dias = 2
        var dias2 = $('#dias_agregados').val();
        dias3 = dias + dias2
        console.log(fecha);
        fecha.setDate(fecha.getDate() + dias);
    })
});