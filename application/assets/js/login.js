
function checkSession() {
    // if localstorage has a session, then redirect to home
    if (localStorage.getItem("session") != null) {
        window.location.href = "index.html";
    }
}


function login() {
    let button = document.getElementById("submitbtn");
    button.onclick = function () {
        fetch(`http://localhost:8080/getuser?user=${document.getElementById("InputUser").value}&pass=${document.getElementById("InputPassword").value}`)
      .then((res) => res.json())
      .then((data) => {
        try {
            console.log(data.session);
            if(data.session != "false"){
                localStorage.setItem("session", data.session);
                window.location.href = "index.html";
            }else{
                // show error for 5 seconds
                document.getElementById("errortext").style.display = "block";
                // hide error after 5 seconds
                setTimeout(function(){ document.getElementById("errortext").style.display = "none"; }, 5000);
            }
        } catch (error) {
            console.log(error);
        }
      })
      .catch((error) => {
        console.log(error);
      });
}
}


function init() {
    login();
    document.getElementById("errortext").style.display = "none";
    checkSession();
}

window.onload = init;