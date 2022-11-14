function checkSession() {
    // check if session is set
    if (localStorage.getItem("session") != null)
    {
        fetch(`http://localhost:8080/checksession?pass=${localStorage.getItem("session")}`)
        .then((res) => res.json())
        .then((data) => {
            if (data.check == localStorage.getItem("session")) {

        try {
            document.getElementById("loginbtn").style.display = "none";
            document.getElementById("navconfig").style.display = "block";
        } catch (error) {
            console.log(error);
        }
        
    }}).catch((error) => {
        console.log(error);
        console.log("Is the API running and the site on localhost?")
      });

    } 
    else {
        try {
            document.getElementById("profiledropdown").style.display = "none";
        } catch (error) {
            console.log(error);
        }
    } 

}
checkSession();

// remove localstorage session when logout is clicked
function logout() {
    localStorage.removeItem("session");
    window.location.href = "index.html";
}



let logoutbtn = document.getElementById("logoutbutton");
logoutbtn.onclick = function () {
    logout();
}

