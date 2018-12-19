window.setTimeout(function () {
    $(".alert").slideUp(500, function () {
        $(this).remove();
    });
}, 2000);


function showUpdateBox() {
    document.getElementById("updateBox").style.display = "block";
    document.getElementById("profileBox").style.display = "none";
    document.getElementById("error_msg").style.display = "none";
}

function passwordValidation() {
    let old_pw = document.getElementById("old_password").value;
    let new_pw = document.getElementById("new_password").value;
    let pw_cfm = document.getElementById("password_cfm").value;
    let error_msg = document.getElementById("error_msg");
    let btn = document.getElementById("update_password");
    document.getElementById("error_msg").className = "alert";

    if (old_pw.length < 6) {
        error_msg.innerText = "Old password too short!";
        error_msg.innerText = "Previous password too short!";
        error_msg.style.display = "block";
        $('#error_msg').delay(2000).slideUp();
        event.preventDefault();
    } else if (new_pw.length < 6) {
        error_msg.innerText = "New password too short!";
        error_msg.style.display = "block";
        $('#error_msg').delay(2000).slideUp();
        event.preventDefault();
    } else if (new_pw !== pw_cfm) {
        error_msg.innerText = "Password doesn't match!";
        error_msg.style.display = "block";
        $('#error_msg').delay(2000).slideUp();
        event.preventDefault();
    } else {
        btn.submit();
    }
}

$(document).ready(function () {
    $('#MyImage').hover(function () {
        $('#penLayer').fadeToggle();
    })
});

function F_Open_dialog() {
    document.getElementById("fileInput").click();
}

document.getElementById("fileInput").addEventListener("change", readFile, false);

function readFile() {
    if (this.files && this.files[0]) {
        var data = new FormData();
        data.append('file', this.files[0]);
        $.ajax({
            url: 'users/avatar',
            type: 'POST',
            cache: false,
            processData: false,
            contentType: false,
            data: data,
            success: function (result) {
                $('#MyImage').css('background-image', `url(${result['avatar_url']})`);
            }
        })
    }
}


