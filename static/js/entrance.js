//校验账号的格式
function check_code() {
    //获取账号
    var code = document.getElementById("id_email").value;
    var color1 = document.getElementById("id_email");
    //校验其格式(\w字母或数字或下划线)
    var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
    var reg_1 = /[A-Z]+/;
    if (code === "") {
        color1.style.border = "1px solid grey";
        return false;
    } else if (reg.test(code)) {
        if(reg_1.test(code))
            return false;
        //通过，增加ok样式
        color1.style.border = "1px solid green";
        return true;
    } else {
        //不通过，增加error样式
        color1.style.border = "1px solid red";
        return false;
    }
}

function check_pwd1() {
    var code2 = document.getElementById("id_pwd1").value;
    var color2 = document.getElementById("id_pwd1");
    var reg2 = /.{6,}/;
    if (code2 === "") {
        color2.style.border = "1px solid grey";
        return false;
    } else if (reg2.test(code2)) {
        color2.style.border = "1px solid green";
        return true;
    } else {
        color2.style.border = "1px solid red";
        return false;
    }
}

function check_username() {
    var code2 = document.getElementById("id_username").value;
    var color2 = document.getElementById("id_username");
    var reg2 = /^[a-z0-9_-]+$/;
    if (code2 === "") {
        color2.style.border = "1px solid grey";
        return false;
    } else if (reg2.test(code2)) {
        color2.style.border = "1px solid green";
        return true;
    } else {
        color2.style.border = "1px solid red";
        return false;
    }
}

function check_pwd2() {
    var code2 = document.getElementById("id_pwd1").value;
    var color2 = document.getElementById("id_pwd1");
    var code3 = document.getElementById("id_pwd2").value;
    var color3 = document.getElementById("id_pwd2");
    var reg3 = /.{6,}/;
    if (code3 === "") {
        color3.style.border = "1px solid grey";
        return false;
    } else if (reg3.test(code3)) {
        if (code3 === code2) {
            color3.style.border = "1px solid green";
            return true;
        } else {
            color2.style.border = "1px solid red";
            color3.style.border = "1px solid red";
            return false;
        }
    } else {
        color3.style.border = "1px solid red";
        return false;
    }
}

function check_commit() {
    let ad = document.getElementById("tip")
    if (!check_code()) {
        ad.innerText = "Invalid email";
        event.preventDefault();
    } else if (!check_pwd1()) {
        ad.innerText = "Password too short (6 chars. min)";
        event.preventDefault();
    } else if (!check_pwd2()) {
        ad.innerText = "Password mismatch!";
        event.preventDefault();
    } else if (!check_username()) {
        ad.innerText = "Invalid username!";
        event.preventDefault();
    }

    $('#tab-1').on("click", function () {
        $('.sign-up-htm form input').each(function () {
            $(this).val("")
        })
    });
    $('#tab-2').on("click", function () {
        $('.sign-in-htm form input').each(function () {
            $(this).val("")
        })
    })
}