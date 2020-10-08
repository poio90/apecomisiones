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

  $('#id_user').prop('required',false)

  $("body").on("click", '#add-more', function () {
    //Toma el id de full name para
    var form = document.querySelector('#id_integrantes_x_solicitud_set-TOTAL_FORMS');
    var select = $('.copy div').first().clone();
    select[0].firstElementChild.firstElementChild.id = "id_integrantes_x_solicitud_set-" + form.value + "-user";
    select[0].firstElementChild.firstElementChild.name = "integrantes_x_solicitud_set-" + form.value + "-user";
    $('.form-wrapper').append(select)
    $('#id_integrantes_x_solicitud_set-' + form.value + '-user').last().next().remove()
    $('#id_integrantes_x_solicitud_set-' + form.value + '-user').prop('required',true)
    form.value = parseInt(form.value) + 1;
  });


  /*$("body").on("click",'#add-more', function () {
    //Toma el id de full name para
    var id = $(this).attr('id');//agregado por mi
    //id = parseInt(id) + 1;//agregado por mi
    //$(".copy select").attr("indice", id);//agregado por mi
    //$(".copy input").attr("id", 'afiliado' + id);//agregado por mi
    //$("#after-add-more").append($("#copy").html());
    console.log($("#copy").html())
    //$(".copy select").prop('required',true);//agregado por mi
    //$(this).attr('id', id = id + 1);//agregado por mi
  });*/

  // select the target node (con esto se logra que los select sean funcionales)
  var target = document.getElementById('form-wrapper');

  if (target) {
    // create an observer instance
    var observer = new MutationObserver(function (mutations) {
      //loop through the detected mutations(added controls)
      mutations.forEach(function (mutation) {
        //addedNodes contains all detected new controls
        if (mutation && mutation.addedNodes) {
          mutation.addedNodes.forEach(function (elm) {
            //only apply select2 to select elements
            var form = document.querySelector('#id_integrantes_x_solicitud_set-TOTAL_FORMS');
            var indice = parseInt(form.value) - 1
            if (elm && elm.nodeName === "DIV") {
              $(elm).find('select[name="integrantes_x_solicitud_set-' + indice + '-user"]').select2({
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
    console.log($(this).parents(".form-row"));
    $(this).parents(".form-row").remove()
    var form = document.querySelector('#id_integrantes_x_solicitud_set-TOTAL_FORMS');
    form.value = parseInt(form.value) - 1;
  });
  //---------------------------------------------------------------------------------------------//

  //---------Tabla dinamica para el itinerario------------------------//
  const $tableID = $('#table');
  const $BTN = $('#export-btn');
  const $EXPORT = $('#export');
  const newTr = `<tr class="hide">
                  <td class="pt-3-half">
                    <input id="input-name" class="input_edit"/>
                  </td>
                  <td class="pt-3-half">
                    <input id="input-dia" class="input_edit"/>
                  </td>
                  <td class="pt-3-half">
                    <input id="input-mes" class="input_edit"/>
                  </td>
                  <td class="pt-3-half">
                    <input id="input-salida" class="input_edit"/>
                  </td>
                  <td class="pt-3-half">
                    <input id="input-hora1" class="input_edit"/>
                  </td>
                  <td class="pt-3-half">
                    <input id="input-llegada" class="input_edit"/>
                  </td>
                  <td class="pt-3-half">
                    <input id="input-hora2" class="input_edit"/>
                    </td>
                  <td>
                    <span class="table-remove">
                      <button type="button" class="btn btn-danger btn-rounded btn-sm my-0">Remove</button>
                    </span>
                  </td>
                </tr>`;

  $('.table-add').on('click', 'i', () => {

    const $clone = $tableID.find('tbody tr').last().clone(true).removeClass('hide table-line');

    if ($tableID.find('tbody tr').length === 0) {
      $('tbody').append(newTr);
    }
    $clone.find('button').attr("disabled", false);
    //$clone.find('input').prop('required',true);
    $tableID.find('table').append($clone);
  });

  $tableID.on('click', '.table-remove', function () {

    $(this).parents('tr').detach();
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
