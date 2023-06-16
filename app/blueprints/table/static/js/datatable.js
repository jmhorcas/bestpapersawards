$(document).ready( function () {
    $('#bpa_table').DataTable({
        paging: false,
        dom: '<"search"f><"search_info"i>rt<"bottom"lp><"clear">',
        columnDefs: [
            {
                targets: [2, 3, 4, -1, -2, -4],
                className: 'dt-center'
            },
            {
                targets: [0],
                className: 'dt-right'
            },
            {
                targets: [3],
                orderable: false
            }
          ]
    }
    );
} );

$(document).ready( function () {
    $('#bpa_admin_table').DataTable({
        paging: false,
        columnDefs: [
            {
                targets: [2, 3, 4, -1, -2, -3, -4, -5, -6],
                className: 'dt-center'
            },
            {
                targets: [0],
                className: 'dt-right'
            },
            {
                targets: [3],
                orderable: false
            }
          ]
    }
    );
} );


// $('#sortTable').DataTable();

// $(document).ready(function(){
//     $("#myInput").on("keyup", function() {
//       var value = $(this).val().toLowerCase();
//       $("#myTable tr").filter(function() {
//         $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
//       });
//     });
//   });

$('#search').addClass('d-flex p-2');