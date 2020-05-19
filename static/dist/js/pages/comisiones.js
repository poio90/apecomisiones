$(document).ready(function () {

    $('#datepicker').datepicker({
        uiLibrary: 'bootstrap4',
        locale: 'es-es',
        format: "yyyy-mm-dd",
    })

    $('#datepickerFin').datepicker({
        uiLibrary: 'bootstrap4',
        locale: 'es-es',
        format: "yyyy-mm-dd",
    })

    $("#myform").on("change", "select", function () {
        var form = $(this).closest("select")
        var id = this.id;
        var div = document.getElementById(id);
        $.ajax({
            url: div.getAttribute("data-validate-afiliado-url"),
            data: form.serialize(),
            dataType: 'json',
            success: function (data) {
                $('#afiliado' + id).val(data.data[0].num_afiliado);
                /*$("").parent().children("input[name='" + data.name + "']").val(text);*/
            }
        });
    })


    $("#transporte").change(function () {
        var form = $(this).closest("#transporte");
        var div = document.getElementById(this.id);
        $.ajax({
            url: div.getAttribute("data-validate-transporte-url"),
            data: form.serialize(),
            dataType: 'json',
            success: function (data) {
                $('#patente').val(data.data[0].patente);
            }
        });
    })

    $("#num_comision").on('change',function (){
        var form = $(this).closest('form').serialize();
        var div = document.getElementById(this.id);
        $.ajax({
            url: div.getAttribute("validate-num-comicion-url"),
            type: 'GET',
            dataType: 'json',
            data: form,
            success: function (data) {
                if(data.is_taken){
                    $("#imprimir").prop('disabled', true);
                    $("#archivar").prop('disabled', true);
                    swal({
                        title: "Revise los campos!",
                        text: 'El número de comisión que está intentando cargar ya existe.',
                        icon: "warning",
                        dangerMode: true,
                    });
                    $('#num_comision').val("");
                }else{
                    $("#imprimir").prop('disabled', false);
                    $("#archivar").prop('disabled', false);
                }
            }
        });
    })

    $('#myform').on('submit', function (e) { //use on if jQuery 1.7+

        var data = $("input[name='num_afiliado[]']").serializeArray();
        var form = $(this).closest('form').serialize();
        control = true;
        indice = 0;

        for (i = 0; i < data.length; i++) {
            for (var j = 0; j < data.length; j++) {
                if (i != j) {
                    if (data[i].value === data[j].value) {
                        control = false;
                        indice = j;
                        j = data.length;
                        i = j;
                    }
                }
            }
        }
        if (!control) {
            e.preventDefault();  //prevent form from submitting
            if (data[indice].value === "") {
                msg = "Hay un campo vacío para algún usuario."
            } else {
                msg = "Está intentando cargar el afiliado " + data[indice].value + " más de una vez."
            }
            swal({
                title: "Revise los campos!",
                text: msg,
                icon: "warning",
                dangerMode: true,
            });
        }
    })

    function resizable(el, factor) {
        var int = Number(factor) || 7.7;
        function resize() { el.style.width = ((el.value.length + 1) * int) + 'px' }
        var e = 'keyup,keypress,focus,blur,change'.split(',');
        for (var i in e) el.addEventListener(e[i], resize, false);
        resize();
    }
    resizable(document.getElementById('input-name'), 7);
    resizable(document.getElementById('input-dia'), 7);
    resizable(document.getElementById('input-mes'), 7);
    resizable(document.getElementById('input-salida'), 7);
    resizable(document.getElementById('input-hora1'), 7);
    resizable(document.getElementById('input-llegada'), 7);
    resizable(document.getElementById('input-hora2'), 7);

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
        console.log(km_salida)
        console.log(km_llegada)
        if (km_salida == 0) {
            $('input[name="km_total"]').val(km_llegada);
        } else {
            $('input[name="km_total"]').val(km_llegada - km_salida);
        }
    })
});