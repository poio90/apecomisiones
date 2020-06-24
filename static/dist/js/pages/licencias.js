$(document).ready(function () {

    $('input[name=fech_inicio]').on('change',function(){
        var fecha = new Date($(this).val());
        var dias = 2
        var dias2 = $('#dias_agregados').val();
        dias3 = dias+dias2
        console.log(fecha);
        fecha.setDate(fecha.getDate() + dias);
        
        console.log(fecha);

    })

});