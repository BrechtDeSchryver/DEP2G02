let recentsorting = "desc"
/** alle sectoren ophalen en displayen in de tabel op het dashboard */
function getSectoren(sorting) {
    if (sorting == "asc") {
        recentsorting = "asc"
        let sortbtn = document.getElementById("sortbtn")
        sortbtn.title = "Klein naar groot"
        sortbtn.onclick = function() {getSectoren("desc")}
        document.getElementById("sortingicon").classList.remove("fa-sort-numeric-desc")
        document.getElementById("sortingicon").classList.add("fa-sort-numeric-asc")
    } 
    if (sorting == "desc") {
        recentsorting = "desc"
        let sortbtn = document.getElementById("sortbtn")
        sortbtn.title = "Groot naar klein"
        sortbtn.onclick = function() {getSectoren("asc")}
        document.getElementById("sortingicon").classList.remove("fa-sort-numeric-asc")
        document.getElementById("sortingicon").classList.add("fa-sort-numeric-desc")
    }

    fetch(`http://localhost:8080/sectors?sorting=${sorting}`)
      .then((res) => res.json())
      .then((date) => {
        return date;
      })
      .then((data) => {
        console.log(data.sectors[1]);
        document.getElementById("dataTable_info").innerHTML = `<b>${data.sectors.length - 1}</b> resultaten`
        let tabel = document.getElementById("sectorentbl")
        tabel.innerHTML = ""
        let i = 1;

        while (i < document.getElementById("maxvals").value){
            tabel.insertAdjacentHTML("beforeend", `
        <tr>
            <td>${data.sectors[i].sector_ID}</td>
            <td>${data.sectors[i].count}</td>
            <td><a class="btn btn-sm morebtn" role="button" href="sector.html?sector=${data.sectors[i].sector_ID}" style="background: rgb(89,182,195);color: rgb(255,255,255);">Details</a></td>
        </tr>
        
        `)
            i += 1;
        }
    
    
    })
      .catch((error) => {
        console.log(error);
      });
}


/** controleert of er in de local storage staat of de notificatie ooit al aangeklikt is */
function checkAlert() {
    const beta = localStorage.getItem('betaAlert');
    if (beta == null) {
        document.getElementById("alert").insertAdjacentHTML("afterbegin", `<span class="badge bg-danger badge-counter">1</span>`)
    }
}

/** handelt een verandering van de max value
 * maakt eerst tabel leeg en vult die dan weer op met het aantal van de max value
 */
function selectchange() {
    let tabel = document.getElementById("sectorentbl")
    tabel.innerHTML = " "
    console.log(document.getElementById("maxvals").value);
    getSectoren(recentsorting);
}

/**Verwijdert de notificatiebadge wanneer er op gelklikt wordt en slaat die ook op in de local storage  */
function removeAlert() {
    const beta = localStorage.getItem('betaAlert');
    if (beta != "seen") {
        localStorage.setItem("betaAlert", "seen");
        document.getElementById("alert").innerHTML = `<i class="fas fa-bell fa-fw"></i>`
    } 
}
/**Roept alle functies aan en detecteert het ingeven van letters en enter */
function init() {
    checkAlert();
    document.getElementById("alert").onclick = function() {removeAlert()};
    getSectoren("desc");
    
}
window.onload = init;