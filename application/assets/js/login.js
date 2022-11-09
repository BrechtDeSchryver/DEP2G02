
function checkSession() {
    // if localstorage has a session, then redirect to home
    try {
        if (localStorage.getItem("session") != null) {
            window.location.href = "index.html";
        }
    } catch (error) {
        window.location.href = "index.html"
    }
}


function login() {
        fetch(`http://localhost:8080/getuser?user=${document.getElementById("InputUser").value.toLowerCase()}&pass=${document.getElementById("InputPassword").value}`)
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
        console.log("Is the API running and the site on localhost?")
      });

}

function enterkeylistner() {
    document.getElementById("InputPassword").addEventListener("keyup", (event) => {
        if (event.key === "Enter") {
          console.log('Enter key pressed')
          login();
        }
      });
      document.getElementById("InputUser").addEventListener("keyup", (event) => {
        if (event.key === "Enter") {
          console.log('Enter key pressed')
          login();
        }
      });
}


function init() {
    let button = document.getElementById("submitbtn");
    button.onclick = function () {login();}
    document.getElementById("errortext").style.display = "none";
    checkSession();
    enterkeylistner();
}

window.onload = init;