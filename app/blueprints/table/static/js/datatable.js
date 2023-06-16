$(document).ready( function () {
    $('#bpa_table').DataTable({
        //"sFilter": "dataTables_filter text-center",
        //dom: "<'row'<'col'f>>",
        paging: false,
        //"dom": "<'col-sm-12 col-md-4'><'col-sm-12 col-md-4'f><'col-sm-12 col-md-4'l>",
        //dom: "<'row'<'col-sm-12 col-md-4'><'col-sm-12 col-md-4'f><'col-sm-12 col-md-4'l>>" + "<'row'<'col-sm-12'tr>>" + "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
        //dom: "<'row'<'col'f>>" + "<'row'<'col'tr>>" + "<'row'<'col'i>>", // Use this for 100% search bar
        dom: "<'row'<'col-6'f><'col-6'i>>" + "<'row'<'col'tr>>" + "<'row'<'col-6'l><'col-6'p>>", 
        //dom: '<"search"f><"search_info"i>rt<"bottom"lp><"clear">',
        //sDom: 'z<"row-fluid"<"span4"C><"span4 lineitemcheckbox"><"span3"l>r><"row-fluid"<"span4 actiondropdown"><"span4"f><"span4 advsearch">><"row-fluid"<"span12 newrecordbutton">><"datatable-scroll"t><"row-fluid"<"span12"i><"span12 center"p>>',
        //sAlign: "left",
        language: {
            searchPlaceholder: "Search",
            search: "",
        },
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

$.fn.DataTable.ext.classes.sFilterInput = "form-control form-control-lg";

$(document).ready( function () {
    $('#bpa_admin_table').DataTable({
        //paging: false,
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
