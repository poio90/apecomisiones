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
  $("body").on("click",'.add-more', function () {
    //Toma el id de full name para 
    var id = $(".full_name").attr('id')//agregado por mi
    $(".copy select").attr("id", id);//agregado por mi
    $(".copy input").attr("id", 'afiliado' + id);//agregado por mi
    //$(".copy select").prop('required',true);//agregado por mi
    var html = $(".copy").html();
    $("#after-add-more").append(html);
    id = parseInt(id);//agregado por mi
    $(".full_name").attr('id', id = id + 1);//agregado por mi
  });

  // select the target node (con esto se logra que los select sean funcionales)
  var target = document.getElementById('after-add-more');

  if (target) {
    // create an observer instance
    var observer = new MutationObserver(function (mutations) {
      //loop through the detected mutations(added controls)
      mutations.forEach(function (mutation) {
        //addedNodes contains all detected new controls
        if (mutation && mutation.addedNodes) {
          mutation.addedNodes.forEach(function (elm) {
            //only apply select2 to select elements
            if (elm && elm.nodeName === "DIV") {
              $(elm).find('select[name="afiliado[]"]').select2({
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
    $(this).parents(".form-group").remove();
    var id = $(".full_name").attr('id')//agregado por mi
    id = parseInt(id);//agregado por mi
    $(".full_name").attr('id', id = id - 1);//agregado por mi
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
