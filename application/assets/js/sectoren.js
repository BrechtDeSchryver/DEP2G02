
/** alle sectoren ophalen en displayen in de tabel op het dashboard */
function getSectoren() {
    fetch(`http://www.vichogent.be:40021/sectoren/all`)
      .then((res) => res.json())
      .then((date) => {
        return date;
      })
      .then((data) => {
        console.log(data.sectoren[1]);
        document.getElementById("dataTable_info").innerHTML = `<b>${data.sectoren.length - 1}</b> resultaten`
        let tabel = document.getElementById("sectorentbl")
        let i = 1;

        while (i < document.getElementById("maxvals").value){
            tabel.insertAdjacentHTML("beforeend", `
        <tr>
            <td>${data.sectoren[i].Ibid_omschrijving}</td>
            <td>${data.sectoren[i].aantal}</td>
            <td><a class="btn btn-sm morebtn" role="button" href="sector.html?sector=${data.sectoren[i].Ibid_omschrijving}" style="background: rgb(89,182,195);color: rgb(255,255,255);">Meer</a></td>
        </tr>
        
        `)
            i += 1;
        }
    
    
    })
      .catch((error) => {
        console.log(error);
      });
}

/** zoekt de aanwezigheid van de ingegeven sub-string in de sectornamen en geeft deze sectoren weer in de tabel  */
function zoek() {
    let zoekwoord = document.getElementById("searchbar").value;
    console.log(zoekwoord)
    tabel = document.getElementById("sectorentbl");
    tabel.innerHTML = " ";
    fetch(`http://www.vichogent.be:40021/sectoren/all`)
      .then((res) => res.json())
      .then((date) => {
        return date;
      })
      .then((data) => {
        let i =1;
        while (i < document.getElementById("maxvals").value){
            if (data.sectoren[i].Ibid_omschrijving.toLowerCase().includes(zoekwoord)){
            console.log(data.sectoren[i].Ibid_omschrijving)
            tabel.insertAdjacentHTML("beforeend", `
        <tr>
            <td>${data.sectoren[i].Ibid_omschrijving}</td>
            <td>${data.sectoren[i].aantal}</td>
            <td><a class="btn btn-sm morebtn" role="button" href="sector.html?sector=${data.sectoren[i].Ibid_omschrijving}" style="background: rgb(89,182,195);color: rgb(255,255,255);">Meer</a></td>
        </tr>
        
        `)}
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
    getSectoren();
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
    getSectoren();
    document.getElementById("searchbar").addEventListener("keyup", function(){
        if (event.keyCode === 13) {
        event.preventDefault();

       } else{
         if (document.getElementById("searchbar").value == '') {
           console.log("leeg")
           getSectoren();
         } else {
          zoek();
         }
       }
    })
}
window.onload = init;