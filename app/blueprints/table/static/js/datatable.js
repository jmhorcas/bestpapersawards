var table = $(document).ready( function () {
    $('#bpa_table').DataTable({
        //"sFilter": "dataTables_filter text-center",
        //dom: "<'row'<'col'f>>",
        paging: false,
        //"dom": "<'col-sm-12 col-md-4'><'col-sm-12 col-md-4'f><'col-sm-12 col-md-4'l>",
        //dom: "<'row'<'col-sm-12 col-md-4'><'col-sm-12 col-md-4'f><'col-sm-12 col-md-4'l>>" + "<'row'<'col-sm-12'tr>>" + "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
        //dom: "<'row'<'col'f>>" + "<'row'<'col'tr>>" + "<'row'<'col'i>>", // Use this for 100% search bar
        dom: "<'row gx-5'<'col-6'f><'col-5'i><'col-1 gx-0'B>>" + "<'row'<'col'tr>>" + "<'row'<'col-6'l><'col-6'p>>", 
        //dom: '<"search"f><"search_info"i>rt<"bottom"lp><"clear">',
        //sDom: 'z<"row-fluid"<"span4"C><"span4 lineitemcheckbox"><"span3"l>r><"row-fluid"<"span4 actiondropdown"><"span4"f><"span4 advsearch">><"row-fluid"<"span12 newrecordbutton">><"datatable-scroll"t><"row-fluid"<"span12"i><"span12 center"p>>',
        //sAlign: "left",
        order: [[1, 'desc']],
        language: {
            searchPlaceholder: "",
            search: "🔍",
        },
        columnDefs: [
            {
                targets: [1, 2, 3, 7],
                className: 'dt-center'
            },
            {
                targets: [2],
                orderable: false
            }
          ],
        buttons: [
            {
                extend: 'collection',
                //text: '<i class="mdi mdi-dots-horizontal mdi-icons-table"></i>',
                text: 'Export',
                //text: '<a class="btn btn-secondary dropbown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">Export</a>',
                //className: 'btn-fw-grey border-0 with-data-toggle',
                buttons: [
                    {
                        extend: 'copy',
                        text: '<a class="dropdown-item pl-0" href="#"><i class="mdi mdi-content-copy pr-2"></i>Copy</a>',
                    },
                    {
                        extend: 'excel',
                        text: 'Excel',
                        exportOptions: {
                            modifier: {
                                page: 'current'
                            }
                        }
                    },
                    {
                        extend: 'csv',
                        text: 'csv'
                    },
                    {
                        extend: 'pdf',
                        text: 'pdf'
                    },
                    {
                        extend: 'print',
                        text: 'print'
                    },
                ]
            }
            ]
    }
    );
} );

//$.fn.DataTable.ext.classes.sFilterInput = "form-control form-control-lg";
// https://datatables.net/extensions/buttons/
//table.buttons().container().appendTo( $('.col-sm-6:eq(0)', table.table().container() ) );
//table.buttons().container().appendTo( $('dropdown', table.table().container() ) );

