function checkSession() {
    // check if session is set
    if (localStorage.getItem("session") != null)
    {
        try {
            document.getElementById("loginbtn").style.display = "none";
        } catch (error) {
            console.log(error);
        }
        
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

