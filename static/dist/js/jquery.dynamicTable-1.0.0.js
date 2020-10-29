/**
 * @name        jquery.dynamicTable-1.0.0.js
 * @author      Dinesh Maind
 * @version     1.0.0
 * @date        2017-08-04
 * @copyright   (c) 2016 Dinesh Maind
 * @licence     Open Licence
 * @homepage
 * @example
 */

; (function($) {
    'use strict';

    $.fn.dynamicTable = function(options) {
        var settings = $.extend({}, {
            showActionColumn: true,
            buttons: {
                addButton: '<input type="button" value="Add" class="btn btn-primary" />',
                cancelButton: '<input type="button" value="Cancel" class="btn btn-primary" />',
                deleteButton: '<input type="button" value="Delete" class="btn btn-danger" />',
                editButton: '<input type="button" value="Edit" class="btn btn-primary" />',
                saveButton: '<input type="button" value="Save" class="btn btn-success" />',
            },
            columns: [],
            data: [],
            getControl: function(columnKey) {
                return '<input type="text" class="form-control" />';
            },
        }, options);

        var populateActionButtons = function(tableRow, addButton, cancelButton, deleteButton, editButton, saveButton) {
            var showHideButtons = function(tableCell, localFlags) {
                var theButtons = {
                    cancelButton: $(tableCell).find('*[data-codeapi-cancelcommand]'),
                    deleteButton: $(tableCell).find('*[data-codeapi-deletecommand]'),
                    editButton: $(tableCell).find('*[data-codeapi-editcommand]'),
                    saveButton: $(tableCell).find('*[data-codeapi-savecommand]')
                };

                if (theButtons.cancelButton) {
                    if (localFlags.cancel) {
                        $(theButtons.cancelButton).show();
                    } else {
                        $(theButtons.cancelButton).hide();
                    }
                }

                if (theButtons.deleteButton) {
                    if (localFlags.delete) {
                        $(theButtons.deleteButton).show();
                    } else {
                        $(theButtons.deleteButton).hide();
                    }
                }

                if (theButtons.editButton) {
                    if (localFlags.edit) {
                        $(theButtons.editButton).show();
                    } else {
                        $(theButtons.editButton).hide();
                    }
                }

                if (theButtons.saveButton) {
                    if (localFlags.save) {
                        $(theButtons.saveButton).show();
                    } else {
                        $(theButtons.saveButton).hide();
                    }
                }
            };

            var tableCell = $('<td></td>');
            $(tableRow).append($(tableCell));

            if (saveButton) {
                var localButton = $($(saveButton).clone());
                $(localButton).attr('data-codeapi-savecommand', 'true');
                $(localButton).hide();
                $(tableCell).append(' ');
                $(tableCell).append($(localButton));

                $(localButton).click(function() {
                    $(this).parents('tr:first').find('*[data-codeapi-inputkey]').each(function() {
                        var inputControl = $(this);
                        var spanControl = $(inputControl).parent().find('span[data-codeapi-displaykey="' + $(inputControl).attr('data-codeapi-inputkey') + '"]');
                        $(spanControl).attr('data-codeapi-value', encodeURIComponent($(inputControl).val()));
                        if ($(inputControl).is('select')) {
                            $(spanControl).text($(inputControl).find('option:selected').text());
                        } else {
                            $(spanControl).text($(inputControl).val());
                        }

                        $(inputControl).hide();
                        $(spanControl).show();
                    });

                    showHideButtons($(tableCell), {
                        cancel: false,
                        delete: true,
                        edit: true,
                        save: false,
                    });
                });
            }

            if (editButton) {
                var localButton = $($(editButton).clone());
                $(localButton).attr('data-codeapi-editcommand', 'true');
                $(tableCell).append(' ');
                $(tableCell).append($(localButton));

                $(localButton).click(function() {
                    $(this).parents('tr:first').find('*[data-codeapi-inputkey]').each(function() {
                        var inputControl = $(this);
                        var spanControl = $(inputControl).parent().find('span[data-codeapi-displaykey="' + $(inputControl).attr('data-codeapi-inputkey') + '"]');

                        $(inputControl).val(decodeURIComponent($(spanControl).attr('data-codeapi-value')));

                        $(inputControl).show();
                        $(spanControl).hide();
                    });

                    showHideButtons($(tableCell), {
                        cancel: true,
                        delete: false,
                        edit: false,
                        save: true,
                    });
                });
            }

            if (deleteButton) {
                var localButton = $($(deleteButton).clone());
                $(localButton).attr('data-codeapi-deletecommand', 'true');
                $(tableCell).append(' ');
                $(tableCell).append($(localButton));

                $(localButton).click(function() {
                    var table = $(this).parents("table:first");
                    $(this).parents('tr:first').replaceWith('');
                    resetSrNoColumn(table);
                });
            }

            if (cancelButton) {
                var localButton = $($(cancelButton).clone());
                $(localButton).attr('data-codeapi-cancelcommand', 'true');
                $(localButton).hide();
                $(tableCell).append(' ');
                $(tableCell).append($(localButton));

                $(localButton).click(function() {
                    $(this).parents('tr:first').find('*[data-codeapi-inputkey]').each(function() {
                        var inputControl = $(this);
                        var spanControl = $(inputControl).parent().find('span[data-codeapi-displaykey="' + $(inputControl).attr('data-codeapi-inputkey') + '"]');

                        $(inputControl).val(decodeURIComponent($(spanControl).attr('data-codeapi-value')));

                        $(inputControl).hide();
                        $(spanControl).show();
                    });

                    showHideButtons($(tableCell), {
                        cancel: false,
                        delete: true,
                        edit: true,
                        save: false,
                    });
                });
            }
        };

        var resetSrNoColumn = function(table) {
            $(table).find("td[data-codeapi-srno]").not(':first').each(function(index, element) {
                $(this).text((index + 1));
            });
        };

        return this.each(function() {
            var addButton = settings.buttons.addButton;
            var cancelButton = settings.buttons.cancelButton;
            var deleteButton = settings.buttons.deleteButton;
            var editButton = settings.buttons.editButton;
            var saveButton = settings.buttons.saveButton;

            var $this = $(this);
            $this.empty();

            // Header row
            var tableRow = $('<tr></tr>');
            $this.append($(tableRow));

            var tableCell = $('<th>#</th>');
            $(tableRow).append($(tableCell));

            // key, text
            for (var x = 0; x < settings.columns.length; x++) {
                tableCell = $('<th>' + settings.columns[x].text + '</th>');
                $(tableRow).append($(tableCell));
            }

            if (settings.showActionColumn) {
                tableCell = $('<th>Action</th>');
                $(tableRow).append($(tableCell));
            }

            if (settings.showActionColumn) {
                // Input row
                tableRow = $('<tr></tr>');
                $this.append($(tableRow));

                tableCell = $('<td data-codeapi-srno="0"></td>');
                $(tableRow).append($(tableCell));

                for (var x = 0; x < settings.columns.length; x++) {
                    tableCell = $('<td></td>');
                    $(tableRow).append($(tableCell));

                    var inputControl = $(settings.getControl(settings.columns[x].key));
                    $(inputControl).attr('data-codeapi-inputkey', settings.columns[x].key);
                    $(inputControl).attr('data-codeapi-defaultvalue', $(inputControl).val());
                    $(tableCell).append($(inputControl));
                }

                if (addButton) {
                    tableCell = $('<td></td>');
                    $(tableRow).append($(tableCell));

                    var localButton = $($(addButton).clone());
                    
                    $(tableCell).append(' ');
                    $(tableCell).append($(localButton));

                    $(localButton).click(function() {
                        var table = $(this).parents("table:first");
                        var currentRow = $(this).parents('tr:first');
                        var newRow = $('<tr></tr>');
                        $(table).append($(newRow));

                        var newTableCell = $('<td data-codeapi-srno="0"></td>');
                        $(newRow).append($(newTableCell));

                        currentRow.find('td').not(':first,:last').each(function() {
                            var tableCell = $(this);
                            var key = $(tableCell).find('*[data-codeapi-inputkey]').attr('data-codeapi-inputkey');
                            var newTableCell = $('<td></td>');
                            $(newRow).append($(newTableCell));
                            var currentInput = $(tableCell).find('*[data-codeapi-inputkey]');
                            var inputControl = $(currentInput).clone();
                            $(inputControl).val($(currentInput).val());
                            $(inputControl).hide();
                            $(newTableCell).append($(inputControl));

                            var spanControl = $('<span></span>');
                            $(spanControl).attr('data-codeapi-displaykey', key);
                            $(spanControl).attr('data-codeapi-value', encodeURIComponent($(inputControl).val()));
                            if ($(inputControl).is("select")) {
                                $(spanControl).text($(inputControl).find('option:selected').text());
                            } else {
                                $(spanControl).text($(inputControl).val());
                            }
                            $(newTableCell).append($(spanControl));

                            $(currentInput).val($(currentInput).attr('data-codeapi-defaultvalue'));
                        });

                        if (settings.showActionColumn) {
                            populateActionButtons(newRow, addButton, cancelButton, deleteButton, editButton, saveButton);
                        }

                        resetSrNoColumn($(table));
                    });
                } else {
                    tableCell = $('<td>&nbsp;</td>');
                    $(tableRow).append($(tableCell));
                }
            }

            // Data rows
            for (var x = 0; x < settings.data.length; x++) {
                tableRow = $('<tr></tr>');
                $this.append($(tableRow));

                tableCell = $('<td data-codeapi-srno="' + (x + 1) + '">' + (x + 1) + '</td>');
                $(tableRow).append($(tableCell));

                for (var y = 0; y < settings.columns.length; y++) {
                    tableCell = $('<td></td>');
                    $(tableRow).append($(tableCell));

                    var inputControl = $(settings.getControl(settings.columns[y].key));
                    $(inputControl).attr('data-codeapi-inputkey', settings.columns[y].key);
                    $(inputControl).val(settings.data[x][settings.columns[y].key]);
                    $(inputControl).hide();
                    $(tableCell).append($(inputControl));

                    var spanControl = $('<span></span>');
                    $(spanControl).attr('data-codeapi-displaykey', settings.columns[y].key);
                    $(spanControl).attr('data-codeapi-value', encodeURIComponent($(inputControl).val()));
                    if ($(inputControl).is("select")) {
                        $(spanControl).text($(inputControl).find('option:selected').text());
                    } else {
                        $(spanControl).text($(inputControl).val());
                    }
                    $(tableCell).append($(spanControl));
                }

                if (settings.showActionColumn) {
                    populateActionButtons(tableRow, addButton, cancelButton, deleteButton, editButton, saveButton);
                }
            }
        });
    };

    $.fn.getTableData = function() {
        var data = [];

        $(this).find("tr").each(function() {
            if ($(this).find('span[data-codeapi-displaykey]').length > 0) {
                var objModel = {};

                $(this).find('span[data-codeapi-displaykey]').each(function() {
                    var key = 'data-codeapi-displaykey';
                    var valueKey = 'data-codeapi-value';
                    objModel[$(this).attr(key)] = decodeURIComponent($(this).attr(valueKey));
                });

                data.push(objModel);
            }
        });

        return data;
    };
})(jQuery);