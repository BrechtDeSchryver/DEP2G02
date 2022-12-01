
/**Deze functie gaat de variabelen (?var=value) uitlezen */
function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(
      /[?&]+([^=&]+)=([^&]*)/gi,
      function (m, key, value) {
        vars[key] = value;
      }
    );
    return vars;
  }
  
function getBedrijven(sector, sortingkey, sorting) {
    sortingkey = sortingkey == undefined ? "name" : sortingkey;
    sorting = sorting == undefined ? "asc" : sorting;
    fetch(`http://localhost:8080/sector?sector=${sector}&sortingkey=${sortingkey}&sorting=${sorting}`)
        .then((res) => res.json())
        .then((data) => {
            let tbl = document.getElementById("bedrijventbl");
            tbl.innerHTML = " ";
            document.getElementById("dataTable_info").innerHTML = data.aantal + " resultaten";
            document.getElementById("naam").innerHTML = data.naam;
            document.getElementById("sectordetailsbtn").href = `sector.html?sector=${sector}`;
            document.getElementById("aantal").innerHTML = data.aantal;
            data.bedrijven.forEach((bedrijf) => {
                let beurs = bedrijf.beursgenoteerd == true ? `<i class="fas fa-check" title="Beursgenoteerd"></i>` : `<i class="fas fa-times" title="Niet beursgenoteerd"></i>`;
                tbl.insertAdjacentHTML("beforeend", `
                <tr>
    <td id="bedrijfnaam" title="${bedrijf.ondernemingsNummer}">${bedrijf.name}</td>
    <td id="personeel" class="text-end">${bedrijf.personeel}</td>
    <td id="omzet" class="text-end">${bedrijf.turnover}</td>
    <td id="beurs" class="text-center">${beurs}</td>
    <td id="score" class="text-end">${bedrijf.score}</td>
    <td><a id="detailsbtn" class="btn btn-sm morebtn" role="button" href="search.html?btw=${bedrijf.ondernemingsNummer}" style="background: rgb(89,182,195);color: rgb(255,255,255);">Details</a></td>
</tr>
                `)
            })
        })

}

function initSorting() {
    document.getElementById("namefield").onclick = function() {getBedrijven(getUrlVars()["sector"], "name", "desc")
changeSorting("namefield", "name", "asc")};
    document.getElementById("employeesfield").onclick = function() {getBedrijven(getUrlVars()["sector"], "total", "desc")
changeSorting("employeesfield", "total", "asc")};
    document.getElementById("turnoverfield").onclick = function() {getBedrijven(getUrlVars()["sector"], "turnover", "desc")
changeSorting("turnoverfield", "turnover", "asc")};
    document.getElementById("stocksfield").onclick = function() {getBedrijven(getUrlVars()["sector"], "beursgenoteerd", "desc")
changeSorting("stocksfield", "beursgenoteerd", "asc")};
    document.getElementById("scorefield").onclick = function() {getBedrijven(getUrlVars()["sector"], "score", "desc")
changeSorting("scorefield", "score", "asc")};
}

function changeSorting(id, key, sorting) {
    console.log(id);
    console.log(key);
    console.log(sorting);
    document.getElementById(id).onclick = function() {getBedrijven(getUrlVars()["sector"], key, sorting)
    changeSorting(id, key, sorting == "asc" ? "desc" : "asc")};
    let sortingicon = sorting == "asc" ? "fas fa-sort-up" : "fas fa-sort-down";
    document.getElementById(id+"arrow").classList = sortingicon;
}

function addToCompare(btw) {
    let compare = localStorage.getItem("compare");
    if (compare == null) {
        localStorage.setItem("compare", btw);
    } else {
        compare = compare + "," + btw;
        localStorage.setItem("compare", compare);
    }
    document.getElementById("comparebtn").innerHTML = `<i class="fas fa-chart-bar fa-fw"></i> Vergelijk (${localStorage.getItem("compare").split(",").length})`;
}

function removeFromCompare(btw) {
    let compare = localStorage.getItem("compare");
    if (compare != null) {
        compare = compare.split(",");
        compare = compare.filter((item) => item != btw);
        compare = compare.join(",");
        localStorage.setItem("compare", compare);
    } else
        localStorage.setItem("compare", "");
    document.getElementById("comparebtn").innerHTML = `<i class="fas fa-chart-bar fa-fw"></i> Vergelijk (${localStorage.getItem("compare").split(",").length})`;
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
    getBedrijven(getUrlVars()["sector"]);
    initSorting();
}
window.onload = init;