$(document).ready(function () {

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

    $('#myform').on('submit', function (e) { //use on if jQuery 1.7+

        var data = $("input[name='num_afiliado[]']").serializeArray();
        var km_total = $("input[name='km_total']").val();
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
        if(control && (km_total < 0)){
                control = false;
        }
        if (!control) {
            e.preventDefault();  //prevent form from submitting
            if (km_total < 0) {
                msg = "Los kilomtros recorridos no pueden ser valores negativos.";
            } else if(data[indice].value === "") {
                msg = "Hay un campo vacío para algún usuario."
            }else {
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
        if (km_salida == 0) {
            $('input[name="km_total"]').val(km_llegada);
        } else {
            $('input[name="km_total"]').val(km_llegada - km_salida);
        }
    })
});