$(document).on("submit", "#register", function (e) {
    e.preventDefault();
    var username = $("#username").val();
    var firstname = $("#firstname").val();
    var lastname = $("#lastname").val();
    var email = $("#email").val();
    var password = $("#password").val();
    var cpassword = $("#cpassword").val();
    var emailreg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
    var charReg = /[ `!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;

    if (username == "" || username == null) {
        error("Please enter username", "#response")
        return false;
    } else if (charReg.test(username) == true) {
        error("No sepcial charachters are allowed in username", "#response");
        return false;
    } else if (firstname == "" || firstname == null) {
        error("Please enter firstname", "#response")
        return false;
    } else if (lastname == "" || lastname == null) {
        error("Please enter lastname", "#response")
        return false;
    } else if (email == "" || email == null) {
        error("Please enter email", "#response")
        return false;
    } else if (emailreg.test(email) == false) {
        error("Invalid email address", "#response");
        return false;
    } else if (password == "" || password == null) {
        error("Please enter password", "#response")
        return false;
    } else if (charReg.test(password) == false) {
        error("Password must have at least one special character and digit in it", "#response");
        return false;
    } else if (cpassword == "" || cpassword == null) {
        error("Please enter confirm password", "#response")
        return false;
    } else if (password !== cpassword) {
        error("Password not matched", "#response")
        return false;
    } else {
        $.ajax({
            url: "/register/",
            type: "POST",
            cache: false,
            data: JSON.stringify({
                username: username,
                firstname: firstname,
                lastname: lastname,
                email: email,
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
                        window.open("/login/", '_self');
                    }, 1000);

                } else if (data["status"] == false) {
                    error(data["message"], "#response");
                }
            },
            complete: function () {
                $("#btn").html('Register');
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
                error(msg, "#response")
            },
        });
    }
});