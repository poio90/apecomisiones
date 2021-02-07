$(document).ready(function () {

  'use strict'

  // Make the dashboard widgets sortable Using jquery UI
  $('.connectedSortable').sortable({
    placeholder: 'sort-highlight',
    connectWith: '.connectedSortable',
    handle: '.card-header, .nav-tabs',
    forcePlaceholderSize: true,
    zIndex: 999999
  })
  $('.connectedSortable .card-header, .connectedSortable .nav-tabs-custom').css('cursor', 'move')

  // jQuery UI sortable for the todo list
  $('.todo-list').sortable({
    placeholder: 'sort-highlight',
    handle: '.handle',
    forcePlaceholderSize: true,
    zIndex: 999999
  })

  //-----funcion que agrega y elimina input para agregar afiliados a confeccion de comisiones-----//

  $('#id_user').prop('required', false)

  $("body").on("click", '#add-more', function () {
    //Toma el id de full name para
    var form = document.querySelector('#id_integrantes_x_solicitud_set-TOTAL_FORMS');
    var select = $('.copy div').first().clone();

    //accede al primer elemento del objeto select
    select[0].firstElementChild.firstElementChild.id = "id_integrantes_x_solicitud_set-" + form.value + "-user"
    select[0].firstElementChild.firstElementChild.name = "integrantes_x_solicitud_set-" + form.value + "-user"

    //accede al siguiente elemento del primer elemento del objeto select
    select[0].firstElementChild.nextElementSibling.id = "id_integrantes_x_solicitud_set-" + form.value + "-DELETE";
    select[0].firstElementChild.nextElementSibling.name = "integrantes_x_solicitud_set-" + form.value + "-DELETE";

    $('.form-repaet').append(select);
    $('#id_integrantes_x_solicitud_set-' + form.value + '-user').last().next().remove();
    $('#id_integrantes_x_solicitud_set-' + form.value + '-user').prop('required', true);

    form.value = parseInt(form.value) + 1;

  });

  $("body").on("click", '#add-more-anticipo', function () {
    //Toma el id de full name para
    var form = document.querySelector('#id_integrantes_x_anticipo_set-TOTAL_FORMS');
    var select = $('.copy div').first().clone();
    //accede al primer elemento del objeto select
    select[0].firstElementChild.firstElementChild.id = "id_integrantes_x_anticipo_set-" + form.value + "-user"
    select[0].firstElementChild.firstElementChild.name = "integrantes_x_anticipo_set-" + form.value + "-user"

    //accede al siguiente elemento del primer elemento del objeto select
    select[0].firstElementChild.nextElementSibling.id = "id_integrantes_x_anticipo_set-" + form.value + "-DELETE";
    select[0].firstElementChild.nextElementSibling.name = "integrantes_x_anticipo_set-" + form.value + "-DELETE";

    $('.form-repaet').append(select);
    $('#id_integrantes_x_anticipo_set-' + form.value + '-user').last().next().remove();
    $('#id_integrantes_x_anticipo_set-' + form.value + '-user').prop('required', true);

    form.value = parseInt(form.value) + 1;

  });

  // select the target node (con esto se logra que los select sean funcionales)
  var target = document.getElementById('form-repaet');

  if (target) {
    // create an observer instance
    var observer = new MutationObserver(function (mutations) {
      //loop through the detected mutations(added controls)
      mutations.forEach(function (mutation) {
        //addedNodes contains all detected new controls
        if (mutation && mutation.addedNodes) {
          mutation.addedNodes.forEach(function (elm) {
            //solo se aplica select2 al elemento select
            var text_name = elm.firstElementChild.firstElementChild.name;
            //obtiene el valor del primer hijo del padre del padre del elemento en cuestion 
            //que en este caso es el select
            var indice = parseInt(elm.parentElement.parentElement.firstElementChild.value) - 1;
            //text_name.match(/[0-9]/)[0] devuelve cualquier numero encontrado en la cadena text_name
            //y replace() remplaza el numero encontrado por match por indice
            text_name = text_name.replace( text_name.match(/[0-9]/)[0],indice);
            if (elm && elm.nodeName === "DIV") {
              $(elm).find('select[name="' + text_name + '"]').select2({
                theme: 'bootstrap4',
                width: $(this).data('width') ? $(this).data('width') : $(this).hasClass('w-100') ? '100%' : 'style',
                placeholder: $(this).data('placeholder'),
                allowClear: Boolean($(this).data('allow-clear')),
              });
            }
          });
        }
      });
    });
    // pass in the target node, as well as the observer options
    observer.observe(target, {
      childList: true
    });

    // later, you can stop observing
    //observer.disconnect();
  }

  $("body").on("click", ".remove", function () {
    $(this).parents(".form-row").remove();
    var form = $(this).parents(".form-row").clone();
    if (form[0].firstElementChild.childNodes[5].id) {
      form[0].firstElementChild.firstElementChild.required = false
      var id = form[0].firstElementChild.childNodes[5].id;
      $('.caja').append(form);
      $('input[id="' + id + '"]').attr('checked', true);
    }
  });
  //---------------------------------------------------------------------------------------------//

  //---------Tabla dinamica para el itinerario------------------------//
  const $tableID = $('#table');
  const $BTN = $('#export-btn');
  const $EXPORT = $('#export');
  
  $('.table-add').on('click', 'button', () => {
    //const $clone = $tableID.find('tbody tr').last().clone(true).removeClass('hide table-line');
    var form = document.querySelector('#id_itinerario_set-TOTAL_FORMS');
    const newTr = `<tr>
                  <td class="d-none d-print-block">
                    <input type="hidden" name="itinerario_set-`+ form.value +`-id_itinerario" id="id_itinerario_set-`+ form.value +`-id_itinerario">
                  </td>
                  <td class="pt-3-half">
                    <input type="text" name="itinerario_set-`+ form.value +`-nombre_afiliado" maxlength="150" class="form-control" id="id_itinerario_set-`+ form.value +`-nombre_afiliado">
                  </td>
                  <td class="pt-3-half">
                    <input type="text" name="itinerario_set-`+ form.value +`-dia" maxlength="10" class="form-control" id="id_itinerario_set-`+ form.value +`-dia">
                  </td>
                  <td class="pt-3-half">
                    <input type="text" name="itinerario_set-`+ form.value +`-mes" maxlength="10" class="form-control" id="id_itinerario_set-`+ form.value +`-mes">
                  </td>
                  <td class="pt-3-half">
                    <input type="text" name="itinerario_set-`+ form.value +`-salida" maxlength="45" class="form-control" id="id_itinerario_set-`+ form.value +`-salida">
                  </td>
                  <td class="pt-3-half">
                    <input type="time" name="itinerario_set-`+ form.value +`-hora_salida" class="form-control" id="id_itinerario_set-`+ form.value +`-hora_salida">
                  </td>
                  <td class="pt-3-half">
                    <input type="text" name="itinerario_set-`+ form.value +`-llegada" maxlength="45" class="form-control" id="id_itinerario_set-`+ form.value +`-llegada">
                  </td>
                  <td class="pt-3-half">
                    <input type="time" name="itinerario_set-`+ form.value +`-hora_llegada" class="form-control" id="id_itinerario_set-`+ form.value +`-hora_llegada">
                  </td>
                  <td>
                    <span class="d-none d-print-block">
                      <input type="checkbox" name="itinerario_set-`+ form.value +`-DELETE" id="id_itinerario_set-`+ form.value +`-DELETE">
                    </span>      
                    <span class="table-remove"><button type="button" class="btn btn-danger btn-rounded btn-sm my-0">Remover</button>
                      </span>   
                    </td>
                </tr>`;
    
    form.value = parseInt(form.value) + 1
    /*if ($tableID.find('tbody tr').length === 0) {
      $('tbody').append(newTr);
    }*/
    //$clone.find('button').attr("disabled", false);
    $tableID.find('table').append(newTr);
  });

  $tableID.on('click', '.table-remove', function () {
    $(this).parents('td').find('input[type="checkbox"]').attr('checked',true)
    $(this).parents('tr').hide();
  });

  $tableID.on('click', '.table-up', function () {

    const $row = $(this).parents('tr');
    if ($row.index() === 1) {
      return;
    }

    $row.prev().before($row.get(0));
  });

  $tableID.on('click', '.table-down', function () {

    const $row = $(this).parents('tr');
    $row.next().after($row.get(0));
  });

  // A few jQuery helpers for exporting only
  jQuery.fn.pop = [].pop;
  jQuery.fn.shift = [].shift;

  $BTN.on('click', () => {

    const $rows = $tableID.find('tr:not(:hidden)');
    const headers = [];
    const data = [];

    // Get the headers (add special header logic here)
    $($rows.shift()).find('th:not(:empty)').each(function () {
      headers.push($(this).text().toLowerCase());
    });

    // Turn all existing rows into a loopable array
    $rows.each(function () {
      const $td = $(this).find('td');
      const h = {};

      // Use the headers from earlier to name our hash keys
      headers.forEach((header, i) => {

        h[header] = $td.eq(i).text();
      });

      data.push(h);
    });

    // Output the result
    $EXPORT.text(JSON.stringify(data));
  });
  //----------------------------------------------------------------------------------//
})
