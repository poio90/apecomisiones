$(document).ready(function () {

    //$('#date_inicio').inputmask("dd/mm/yyyy");  //static mask
    $('#date_inicio').inputmask({ "mask": "99/99/9999", "placeholder": "dd/mm/yyyy" }); //specifying options
    //$('#date_inicio').inputmask("9-a{1,3}9{1,3}"); //mask with dynamic syntax

    $('#date_fin').inputmask({ "mask": "99/99/9999", "placeholder": "dd/mm/yyyy" }); //specifying options
    $('#date_reintegro').inputmask({ "mask": "99/99/9999", "placeholder": "dd/mm/yyyy" }); //specifying options

    /* Función que muestra mensaje de error en alertas */
    function message_error(message) {
        swal.fire({
            title: 'Oops...!',
            text: message,
            icon: 'error',
            allowOutsideClick: false,
            allowEscapeKey: false,
            allowEnterKey: false,
        });
    }

    function message_succes(message, pdf_url, url) {
        swalWithBootstrapButtons.fire({
            title: message,
            text: "Desea imprimir el documento?",
            icon: 'success',
            showCancelButton: true,
            confirmButtonText: 'Si',
            cancelButtonText: 'No',
            reverseButtons: true,
            allowOutsideClick: false,
            allowEscapeKey: false,
            allowEnterKey: false,
        }).then((result) => {
            if (result.isConfirmed) {
                window.open(pdf_url);
                window.location.href = url
            } else if (
                /* Read more about handling dismissals below */
                result.dismiss === Swal.DismissReason.cancel
            ) {
                window.location.href = url
            }
        })
    }

    /* Estilos de los botones cuando pregunta si desea imprimir el docuemnto*/
    const swalWithBootstrapButtons = swal.mixin({
        customClass: {
            confirmButton: 'btn btn-success ml-2',
            cancelButton: 'btn btn-danger mr-2'
        },
        buttonsStyling: false
    })

    $('#form_licencia').on('submit', function (e) {
        e.preventDefault();
        var parametros = $(this).serializeArray();
        var div = document.getElementById(this.id);
        var url = div.getAttribute("data-url");
        $.ajax({
            url: div.getAttribute("data-validate-url"),
            type: 'POST',
            data: parametros,
            dataType: 'json',
        }).done(function (response) {
            /** mas adelante acomodar todo en una sola función*/
            if (!response.hasOwnProperty('success_message')) {
                message_error(response.error,);
            } else {
                message_succes(response.success_message, response.pdf_url, url);
            }
        })
    })



    $('#example tbody').on('click','a[rel="delete"]' ,function () {
       

    })
});