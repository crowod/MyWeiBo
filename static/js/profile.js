
function showUpdateBox() {
    document.getElementById("updateBox").style.display = "block";
<<<<<<< HEAD
=======
    document.getElementById("profileBox").style.display = "none";
>>>>>>> master
}

function passwordValidation() {
    let old_pw = document.getElementById("old_password").value;
    let new_pw = document.getElementById("new_password").value;
    let pw_cfm = document.getElementById("password_cfm").value;
    let error_msg = document.getElementById("error_msg");
    let btn = document.getElementById("updateButton");

    if (old_pw.length < 6) {
<<<<<<< HEAD
        error_msg.innerText = "Old password too short!";
=======
        error_msg.innerText = "Previous password too short!";
>>>>>>> master
        error_msg.style.display = "block";
    } else if (new_pw.length < 6) {
        error_msg.innerText = "New password too short!";
        error_msg.style.display = "block";
    } else if (new_pw !== pw_cfm) {
        error_msg.innerText = "Password doesn't match!";
        error_msg.style.display = "block";
    } else {
        btn.submit();
    }
}