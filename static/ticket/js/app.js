$(document).ready(function () {

    console.log('Iniciando app ....');

    $('[data-toggle="tooltip"]').tooltip();
    
    toastr.options = {
        "closeButton": false,
        "debug": false,
        "positionClass": "toast-top-right",
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "5000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    }
    
    $(".open-loading").click(function() {
        $('#loading-dialog').modal('show');
    });

    $("#flash-messages > ul > div").each(function (index) {

        var div = $(this);
        var className = div.attr('class');
        var text = div.text();

        switch (className) {

            case 'success':
                toastr.success(text);
                break;

            case 'error':
                toastr.error(text);
                break;

            case 'info':
                toastr.info(text);
                break;

        }

    });

});