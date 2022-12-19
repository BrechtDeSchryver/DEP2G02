
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
                let score = bedrijf.score == null ? `<i class="fas fa-times" title="Niet beoordeeld"></i>` : bedrijf.score.replace(".", ",");
                tbl.insertAdjacentHTML("beforeend", `
                <tr>
    <td id="bedrijfsnaam" title="Klik om te vergelijken" onclick="addToCompare('${bedrijf.ondernemingsNummer}')"><span class="clickableList" id="${bedrijf.ondernemingsNummer}">${bedrijf.name}</span></td>
    <td id="personeel" class="text-end">${bedrijf.personeel}</td>
    <td id="omzet" class="text-end">${numberWithCommas(bedrijf.turnover)}</td>
    <td id="beurs" class="text-center">${beurs}</td>
    <td id="score" class="text-end">${score}</td>
    <td><a id="detailsbtn" class="btn btn-sm morebtn" role="button" href="search.html?btw=${bedrijf.ondernemingsNummer}" style="background: rgb(89,182,195);color: rgb(255,255,255);">Details</a></td>
</tr>
                `)
            })

            let compare = localStorage.getItem("compare");
        if (compare != null && compare != "") {
            let comparearray = compare.split(",");
            console.log(comparearray);
            comparearray.forEach((btw) => {
                console.log(btw)
                //wait for the list to load
                compareStyle(btw, "add");
            })
        }


        })
        // get the items from the compare list and style them

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
        initBedrijvenlist();
        tooltipAlert(btw, "Bedrijf toegevoegd aan vergelijking!");
        compareStyle(btw, "add");
    } else {
        let comparearray = compare.split(",");
        if (comparearray.length > 1) {
            alert("Je kan maar 2 bedrijven tegelijk vergelijken");
        } else { 
            if (comparearray.includes(btw)) {
                alert("Dit bedrijf staat al in de vergelijking.");
            } else {
        compare = compare + "," + btw;
        localStorage.setItem("compare", compare);
        initBedrijvenlist();
        compareStyle(btw, "add");
        tooltipAlert(btw, "Bedrijf toegevoegd aan vergelijking!");
            }
    
    }
    //document.getElementById("comparebtn").innerHTML = `<i class="fas fa-chart-bar fa-fw"></i> Vergelijk (${localStorage.getItem("compare").split(",").length})`;
}
}

function tooltipAlert(item, text) {
    // add data-bs-toggle="tooltip" to the element using bootstrap tooltip
    item = document.getElementById(item);
    item.setAttribute("data-bs-toggle", "tooltip");
    item.setAttribute("data-bs-placement", "top");
    item.setAttribute("title", text);
    item.setAttribute("data-bs-trigger", "manual");
    item.setAttribute("data-bs-delay", "0");
    item.setAttribute("data-bs-html", "true");
    item.setAttribute("data-bs-animation", "false");

    // show tooltip
    var tooltip = new bootstrap.Tooltip(item);
    tooltip.show();
    // hide after 2 seconds
    setTimeout(function() {
        tooltip.hide();
    }, 4000);

}

function compareStyle (item, action) {
    item = document.getElementById(item);
    if (action == "add") {
        item.style.color = "rgb(89,182,195)";
        item.style.fontWeight = "bold";
    } else {
        item.style.color = "rgb(133,135,150)";
        item.style.fontWeight = "normal";
    }

}

function removeFromCompare(btw) {
    let compare = localStorage.getItem("compare");
    if (compare != null && compare != "") {
        compare = compare.split(",");
        compare = compare.filter((item) => item != btw);
        compareStyle(btw, "remove");
        if (compare.length == 0) {
            localStorage.removeItem("compare");
            document.getElementById("badge").style.display = "none";
        } else {
        compare = compare.join(",");
        localStorage.setItem("compare", compare);
        }
    } else {localStorage.setItem("compare", "");}
        
    //document.getElementById("comparebtn").innerHTML = `<i class="fas fa-chart-bar fa-fw"></i> Vergelijk (${localStorage.getItem("compare").split(",").length})`;
    initBedrijvenlist();
}

function returnCompare(btw) {
    let compare = localStorage.getItem("compare");
    if (compare != null) {
        compare = compare.split(",");
        if (compare.includes(btw))
            return true;
        else
            return false;
    } else
        return false;
}

function initBedrijvenlist() {
    let menu = document.getElementById("comparemenu");
    let compare = localStorage.getItem("compare");
    menu.innerHTML = `<h6 class="dropdown-header" style="background: rgb(89,182,195);border-width: 1px;border-color: rgb(89,182,195);">Vergelijken</h6>`;
    let counter = 0;
    if (compare != null && compare != "") {
        
        compare = compare.split(",");
        compare.forEach((btw) => {
            fetch(`http://localhost:8080/bedrijf/btw/${btw}`)
                .then((res) => res.json())
                .then((data) => {
                    menu.insertAdjacentHTML("beforeend", `
                    <a class="dropdown-item d-flex align-items-center" href="#" style="border-radius: 0px;border-bottom-left-radius: 6px;border-bottom-right-radius: 6px;">
    <div class="me-3"><i class="fas fa-minus-circle" style="font-size: 19.6px;color: rgb(213,44,33);" onclick="removeFromCompare('${data.bedrijven[0].ondernemingsNummer}')"></i></div>
    <div><span class="small text-gray-500">${data.bedrijven[0].ondernemingsNummer}</span>
        <p>${data.bedrijven[0].name}</p>
    </div>
</a>
                    `)
                })
                counter++;
        })

        console.log(counter);
        if (counter >= 2) {
            let comparebtn = document.getElementById("comparebtn");
            comparebtn.innerHTML = `<i class="fas fa-chart-bar fa-fw"></i> Vergelijk (${counter})`;
            comparebtn.style.display = "block";
        } else {
            let comparebtn = document.getElementById("comparebtn");
            comparebtn.style.display = "none";
        }
        if (counter == 0) {
            document.getElementById("badge").style.display = "none";
        } else {
            document.getElementById("badge").style.display = "block";
            document.getElementById("badge").innerHTML = `${counter}`;
        }
    }

    
    
    /*menu.insertAdjacentHTML("beforeend", `
    <a class="dropdown-item d-flex align-items-center" href="#" style="border-radius: 0px;border-bottom-left-radius: 6px;border-bottom-right-radius: 6px;">
    <div class="me-3"><i class="fas fa-minus-circle" style="font-size: 19.6px;color: rgb(213,44,33);"></i></div>
    <div><span class="small text-gray-500">BE64646544654</span>
        <p>Bedrijfnaam</p>
    </div>
</a>
    `)   */
}

/** grote getallen leesbaar maken door een punt te zetten om de 3 cijfers */
function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
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

    getBedrijven(getUrlVars()["sector"]);
    initSorting();
    initBedrijvenlist();
}
window.onload = init;