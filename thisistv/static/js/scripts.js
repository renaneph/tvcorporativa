$(document).ready(function(){

    $(function () {
        $('#datatable').DataTable({
            responsive: true, lengthChange: true, autoWidth: false,
            buttons: ["copy", "csv", "excel", "pdf", "print", "colvis"],
            lengthMenu: [
                [10, 25, 50, -1],
                [10, 25, 50, 'Todos'],
            ],
            pagingType: 'full_numbers',
            language: {
                url: "/static/plugins/datatables/pt-BR.json"
            },
            dom: 'lBfrtip',
        });
        
      });
    
});