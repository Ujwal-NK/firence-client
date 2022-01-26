function upper(t) {
    t.value = t.value.toUpperCase();
}

function togglePass() {
    passField = document.getElementById("pass_box");
    passIconHide = document.getElementById("pass_hide");
    passIconUnHide = document.getElementById("pass_unhide");
    if (passField.type == "password") {
        passIconHide.style.display = "none";
        passIconUnHide.style.display = "block";
        passField.type = "text";
    } else {
        passIconHide.style.display = "block";
        passIconUnHide.style.display = "none";
        passField.type = "password";
    }
}

function passHash() {
    document.getElementById("pass_hash").value = md5(document.getElementById("pass_box").value)
}

document.onkeyup = function () {
    u = document.getElementById("id_box");
    p = document.getElementById("pass_box");
    if (u.value != "" && p.value != "") {
        document.getElementById("submit").style.display = "block"
    } else {
        document.getElementById("submit").style.display = "none"
    }
}
