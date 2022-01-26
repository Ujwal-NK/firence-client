window.sessionStorage.setItem("auth", "success");

function checkInputs() {
    var input = document.getElementById('srn');
    input.value = input.value.toUpperCase();
    buttonState();
    if (String(input.value).length > 0) {
        document.getElementById("nameOption").disabled = true;
    } else {
        document.getElementById("nameOption").disabled = false;
    }

    var nameLabel = document.getElementById("nameOption");
    if (nameLabel.value == "") {
        document.getElementById("srn").disabled = false;
    } else {
        document.getElementById("srn").disabled = true;
    }
}

function buttonState() {
    if (document.getElementById("srn").value == "" && document.getElementById("nameOption").value == "") {
        document.getElementById("submit").style.display = "none";
        console.log("Making none");
    } else {
        document.getElementById("submit").style.display = "block";
        console.log("Visible");
    }
}

function checkButton() {
    if (document.getElementById("radio_3").checked) {
        document.getElementById("reportBox").style.display = "block";
        document.getElementById("reportBox").disabled = false;

    } else {
        document.getElementById("reportBox").style.display = "none";
        document.getElementById("reportBox").disabled = true;
    }
}

function clean() {
    document.getElementById("srn").value = "";
    checkInputs()
}

function clearOption() {
    document.getElementById("nameOption").selectedIndex = 0;

    document.querySelector("#nameOption").innerHTML = '';

    getPeopleList();
    checkInputs()
}

function override() {
    if (window.confirm("Send an OVERRIDE Request?")) {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/", true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({
            "OVERRIDE": "OVERRIDE"
        }));
        document.getElementById("button_override").style.display = "none";
        setTimeout(function () {
            document.getElementById("button_override").style.display = "block";
        }, 5000);
    }
}

function getPeopleList() {
    var resp = "";
    document.getElementById("refresh_list").classList.add("rotate");
    console.log(document.getElementById("refresh_list").classList)
    // Creating a XMLHttpRequest Variable
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            resp = this.responseText;
        }
    };
    xhttp.open("POST", "/", false);
    xhttp.send("peopleList");
    console.log(resp);
    if (resp != "[]") {
        var people = resp.substr(1, resp.indexOf(']') - 1).split(",")
        console.log(people);
        var sel = document.getElementById("nameOption");
        let opt = document.createElement("option");
        opt.appendChild(document.createTextNode("None"))
        opt.value = ""
        sel.appendChild(opt);
        for (let x = 0; x < people.length; x++) {
            people[x] = people[x].trim();
            people[x] = people[x].substr(people[x].indexOf('\'') + 1, people[x].length - 2)
            let opt = document.createElement("option");
            opt.appendChild(document.createTextNode(people[x]))
            opt.value = people[x]
            sel.appendChild(opt);
        }
    }
    setTimeout(function () {
        document.getElementById("refresh_list").classList.remove("rotate");
    }, 2000);

}

function validateMyForm() {
    srn_field = document.getElementById("srn");
    name_field = document.getElementById("nameOption");
    radio = document.getElementById("radio_3");
    query_field = document.getElementById("reportBox");
    console.log("SRN FIELD:", srn_field.value == "");
    console.log("NAME FIELD:", name_field.value == "");
    console.log("RADIO CHECK:", radio.checked)
    if (srn_field.value == "" && name_field.value == "") {
        // returnToPreviousPage();
        alert("Please fill the required Fields");
        return false;
    }
    if (radio.checked == true && query_field.value == ""){
        alert("Please Entry a keyword for query");
        return false;
    }
    // alert("validations passed");
    // return true;
    console.log(document.getElementsByTagName("form")[0])
    document.getElementsByTagName("form")[0].submit();
}

function returnToPreviousPage() {
    window.history.back();
}

