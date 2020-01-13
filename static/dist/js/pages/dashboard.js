/*
 * Author: Abdullah A Almsaeed
 * Date: 4 Jan 2014
 * Description:
 *      This is a demo file used only for the main dashboard (index.html)
 **/

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

  // bootstrap WYSIHTML5 - text editor
  $('.textarea').summernote({
    height:300,
  })

  //-----funcion que agrega y elimina input para agregar afiliados a confeccion de comisiones-----//
  $(".add-more").click(function () {
    var html = $(".copy").html();
    $(".after-add-more").after(html);
  });

  $("body").on("click", ".remove", function () {
    $(this).parents(".form-group").remove();

  });
  //---------------------------------------------------------------------------------------------//

  //Add text editor
  $('#compose-textarea').summernote();

  //---------Tabla dinamica para el itinerario------------------------//
  const $tableID = $('#table');
  const $BTN = $('#export-btn');
  const $EXPORT = $('#export');
  const newTr = `<tr class="hide">
                  <td class="pt-3-half" contenteditable="true">Apellido y Nombre</td>
                  <td class="pt-3-half" contenteditable="true">Día</td>
                  <td class="pt-3-half" contenteditable="true">Mes</td>
                  <td class="pt-3-half" contenteditable="true">Salida de:</td>
                  <td class="pt-3-half" contenteditable="true">horario</td>
                  <td class="pt-3-half" contenteditable="true">Llegada a:</td>
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

  $('#boton_cargar_comisiones').click(function () {
    $.ajax({
      url: 'confecion_comision.html',
      success: function (data) {
        $('#div_dinamico_anim').html(data);
        $('#div_dinamico_anim div').slideDown(1000);
      }
    });
  });
})
