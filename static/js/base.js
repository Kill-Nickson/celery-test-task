$(document).ready(function () {

  // Denotes total number of rows
  var rowIdx = 0;

  // jQuery button click event to add a row
  $('#addBtn').on('click', function () {

    // Adding a row inside the tbody.
    $('#tbody').append(`
        <tr class="col-names">
            <td class="row-index text-center">
                <p>${++rowIdx}</p>
            </td>
            <td class="text-center col-name">
                <input type="text" class="form-control">
            </td>
            <td class="text-center col-type">
                <select class="types form-control">
                    <option value="full-name">Full name</option>
                    <option value="integer">Integer</option>
                    <option value="company">Сompany</option>
                    <option value="job">Job</option>
                </select>
            </td>
            <td class="text-center"></td>
            <td class="text-center"></td>
            <td class="text-center">
                <button class="btn btn-danger remove" type="button">Remove</button>
            </td>
        </tr>`);
  });

  // jQuery button click event to remove a row.
  $('#tbody').on('click', '.remove', function () {

    // Getting all the rows next to the row
    // containing the clicked button
    var child = $(this).closest('tr').nextAll();

    // Iterating across all the rows
    // obtained to change the index
    child.each(function () {

      // Getting <tr> id.
      var id = $(this).attr('id');

      // Getting the <p> inside the .row-index class.
      var idx = $(this).children('.row-index').children('p');

      // Gets the row number from <tr> id.
      var dig = parseInt(id.substring(1));

      // Modifying row index.
      idx.html(`${dig - 1}`);

      // Modifying row id.
      $(this).attr('id', `R${dig - 1}`);
    });

    // Removing the current row.
    $(this).closest('tr').remove();

    // Decreasing total number of rows by 1.
    rowIdx--;
  });

  $(document).on('change','.types',function(e){
   if (this.value == 'integer'){
    $(this).parent().after(`<td class="text-center min"><input type="text" class="form-control"></td>`);
    $(this).parent().after(`<td class="text-center max"><input type="text" class="form-control"></td>`);
    $(this).parent().after().next().next().next().remove();
    $(this).parent().after().next().next().next().remove();
   }
  });

  $('#new-schema-form').submit(function(e) {
    e.preventDefault();

    var serializedData = {'csrfmiddlewaretoken': this.querySelector('[name="csrfmiddlewaretoken"]').value}
    serializedData['title'] = document.querySelector('[name="title"]').value
    serializedData['column_separator'] = document.querySelector('[name="column_separator"]').value
    serializedData['columns'] = '';

    var oTable = document.getElementsByClassName('col-table')[0];
    var rowLength = oTable.rows.length;

    for (i = 1; i < rowLength; i++){
       var rowData = '';
       var oCells = oTable.rows.item(i).cells;

       var colNameField = oCells.item(1).getElementsByTagName("input")[0].value;

       var selectElem = oCells.item(2).getElementsByTagName("select")[0];
       var selectField = selectElem.options[selectElem.selectedIndex].text;

       rowData+=selectField;
       rowData+=':::';
       rowData+=colNameField;

       if (selectField == 'Integer'){
        var minField = oCells.item(3).getElementsByTagName("input")[0].value;
        var maxField = oCells.item(4).getElementsByTagName("input")[0].value;
        rowData+=':::';
        rowData+=minField;
        rowData+=':::';
        rowData+=maxField;
       }
       serializedData['columns']+=rowData;
       serializedData['columns']+=';';
    }

    console.log(serializedData);
    $.ajax({
        url: $('new-schema-form').data('url'),
        data: serializedData,
        type: 'post',
        success: function (response) {
            location.href = "http://127.0.0.1:8000/schemas/"
        }
    })
  });

  $('#generate-data').submit(function(e) {
    e.preventDefault();

    var serializedData = {}
    serializedData['rows-amount'] = document.querySelector('[name="rows-amount"]').value

    console.log(serializedData);
    $.ajax({
        url: $('generate-data').data('url'),
        data: serializedData,
        type: 'get',
        success: function (response) {
            location.reload();
        }
    })
  });

  $('.download-btn').click(function() {
    var serializedData = {'path': this.value}
    $.ajax({
      url: $('.download-btn').data('url'),
      data: serializedData,
      type: 'get',
      success: function (data) {
        var blob=new Blob([data]);
        var link=document.createElement('a');
        link.href=window.URL.createObjectURL(blob);
        link.download="dataset.csv";
        link.click();
      }
    })
  });
});