
$(document).on("submit", "#login", function (e) {
    e.preventDefault();
    var username = $("#username").val();
    var password = $("#password").val();
    if (username == "" || username == null) {
        error("Please enter username...", "#response")
        return false;
    } else if (password == "" || password == null) {
        error("Please enter password...", "#response")
        return false;
    } else {
    
        $.ajax({
            url: "/login/",
            type: "POST",
            cache: false,
            data: JSON.stringify({
                username: username,
                password: password
            }),
            contentType: "application/json",
            dataType: "json",
            beforeSend: function () {
                $("#btn").html(`<div class="loader"></div>`);
            },
            success: function (data) {
                if (data["status"] == true) {
                    success(data["message"], "#response");
                    setTimeout(function () {
                        window.open("/", '_self');
                    }, 1000);

                } else if (data["status"] == false) {
                    error(data["message"], "#response");
                }
            },
            complete: function () {
                $("#btn").html('Login');
            },
            error: function (jqXHR, exception) {
                var msg = '';
                if (jqXHR.status === 0) {
                    msg = 'Not connect.\n Verify Network.';
                } else if (jqXHR.status == 404) {
                    msg = 'Requested page not found. [404]';
                } else if (jqXHR.status == 500) {
                    msg = 'Internal Server Error [500].';
                } else if (exception === 'parsererror') {
                    msg = 'Requested JSON parse failed.';
                } else if (exception === 'timeout') {
                    msg = 'Time out error.';
                } else if (exception === 'abort') {
                    msg = 'Ajax request aborted.';
                } else {
                    msg = 'Uncaught Error.\n' + jqXHR.responseText;
                }
                $('#response').html(msg);
            },
        });
    }
});