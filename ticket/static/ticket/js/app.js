$(document).ready(function () {

    console.log('Iniciando app ....');

    function getCookie(c_name) {
        if (document.cookie.length > 0)
        {
            c_start = document.cookie.indexOf(c_name + "=");
            if (c_start != -1)
            {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if (c_end == -1) c_end = document.cookie.length;
                return unescape(document.cookie.substring(c_start,c_end));
            }
        }
        return "";
    }

    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
    
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