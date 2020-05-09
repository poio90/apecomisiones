$(document).ready(function() {
    /*$('#key').on('keyup', function() {
        var key = $(this).val();
        var dataString = 'key='+key;
	$.ajax({
            type: "GET",
            url: "ajax.php",
            data: dataString,
            success: function(data) {
                //Escribimos las sugerencias que nos manda la consulta
                $('#suggestions').fadeIn(1000).html(data);
                //Al hacer click en alguna de las sugerencias
                $('.suggest-element').on('click', function(){
                        //Obtenemos la id unica de la sugerencia pulsada
                        var id = $(this).attr('id');
                        //Editamos el valor del input con data de la sugerencia pulsada
                        $('#key').val($('#'+id).attr('data'));
                        //Hacemos desaparecer el resto de sugerencias
                        $('#suggestions').fadeOut(1000);
                        alert('Has seleccionado el '+id+' '+$('#'+id).attr('data'));
                        return false;
                });
            }
        });
    });*/

    $('#datepicker').datepicker({
        uiLibrary: 'bootstrap4',
        locale: 'es-es',
        format: "yyyy-mm-dd",
    });
    
    $('#datepickerFin').datepicker({
        uiLibrary: 'bootstrap4',
        locale: 'es-es',
        format: "yyyy-mm-dd",
    });

    $("body").on("change","select",function () {
        var form = $(this).closest("select")
        var id = this.id;
        var div = document.getElementById(id);
        $.ajax({
            url: div.getAttribute("data-validate-afiliado-url"),
            data: form.serialize(),
            dataType: 'json',
            success: function (data) {
                $('#afiliado'+id).val(data.data[0].num_afiliado);
                /*$("").parent().children("input[name='" + data.name + "']").val(text);*/
                }
        });
    });
    
    
    $("#transporte").change(function () {
        var form = $(this).closest("#transporte");
        var div = document.getElementById("transporte");
        $.ajax({
            url: div.getAttribute("data-validate-transporte-url"),
            data: form.serialize(),
            dataType: 'json',
            success: function (data) {
                $('#patente').val(data.data[0].patente);
            }
        });
    });

    function resizable (el, factor) {
        var int = Number(factor) || 7.7;
        function resize() {el.style.width = ((el.value.length+1) * int) + 'px'}
        var e = 'keyup,keypress,focus,blur,change'.split(',');
        for (var i in e) el.addEventListener(e[i],resize,false);
        resize();
      }
    resizable(document.getElementById('input-name'),7);
    resizable(document.getElementById('input-dia'),7);
    resizable(document.getElementById('input-mes'),7);
    resizable(document.getElementById('input-salida'),7);
    resizable(document.getElementById('input-hora1'),7);
    resizable(document.getElementById('input-llegada'),7);
    resizable(document.getElementById('input-hora2'),7);
    
    $('input[name="km_salida"]').change(function(){
        var km_salida = $(this).val()
        var km_llegada = $('input[name="km_llegada"]').val()
        console.log(km_salida)
        console.log(km_llegada)
        if(km_llegada==0){
            $('input[name="km_total"]').val(km_salida);
        }else{
            $('input[name="km_total"]').val(km_llegada-km_salida);
        }
    })

    $('input[name="km_llegada"]').change(function(){
        var km_llegada = $(this).val()
        var km_salida = $('input[name="km_salida"]').val()
        console.log(km_salida)
        console.log(km_llegada)
        if(km_salida==0){
            $('input[name="km_total"]').val(km_llegada);
        }else{
            $('input[name="km_total"]').val(km_llegada-km_salida);
        }
    })

    // process the form
    /*$('form').submit(function(event) {
        // get the form data
        // there are many ways to get this data using jQuery (you can use the class or id also)
        var formData = {
            'name'              : $('input[name=name]').val(),
            'email'             : $('input[name=email]').val(),
            'superheroAlias'    : $('input[name=superheroAlias]').val()
        };
        // process the form
        $.ajax({
            type        : 'POST', // define the type of HTTP verb we want to use (POST for our form)
            url         : 'process.php', // the url where we want to POST
            data        : formData, // our data object
            dataType    : 'json', // what type of data do we expect back from the server
            encode      : true
        })
            // using the done promise callback
            .done(function(data) {
                // log data to the console so we can see
                console.log(data);
                // here we will handle errors and validation messages
            });
        // stop the form from submitting the normal way and refreshing the page
        event.preventDefault();
    });*/
});