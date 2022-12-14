let curcat = null
let additioncard = document.getElementById("additioncard");

function checkSession() {
    // if localstorage has a session, then redirect to home
    try {
        if (localStorage.getItem("session") == null) {
            window.location.href = "login.html";
        }
    } catch (error) {
        window.location.href = "login.html"
    }
}

// haalt de categorieen op
function getCategories() {
    fetch('http://localhost:8080/categories')
        .then(response => response.json())
        .then(data => {
            let list = data.categories;
            console.log(list);
            document.getElementById("cardtitle").innerHTML = "Domeinen";
            let breadcrumb = document.getElementById("breadcrumb");
            breadcrumb.innerHTML = ` `;
            let categories = document.getElementById("categories");
            categories.innerHTML = "";
            additioncard.style.display = "none";
            document.getElementById("woorden").innerHTML = "";
            list.forEach(element => {
                categories.insertAdjacentHTML('beforeend', `<button id="${element.toLowerCase()}" class="btn btn-primary" onclick="getSubCategorie('${element}')" type="button" style="background: rgb(89,182,195);border-color: rgb(89,182,195);">${element}`); });
        }
        )
}

// haalt de subcategorieen op
function getSubCategorie(category) {
    console.log(category);
    document.getElementById("categories").innerHTML = "";
    document.getElementById("woorden").innerHTML = "";
    fetch(`http://localhost:8080/subcategories/${category}`)
        .then(response => response.json())
        .then(data => {
            let list = data.categories;
            console.log(list);
            let categories = document.getElementById("categories");
            document.getElementById("cardtitle").innerHTML = category;
            additioncard.style.display = "none";
            let breadcrumb = document.getElementById("breadcrumb");
            breadcrumb.innerHTML = `<li onclick="getCategories()" class="breadcrumb-item"><a href="#"><span>Domeinen</span></a></li><li class="breadcrumb-item"><a href="#"><span> </span></a></li>`;
            list.forEach(element => {
                categories.insertAdjacentHTML('beforeend', `<button id="${element.toLowerCase()}" class="btn btn-primary" onclick="getSearchTerms('${element}', '${category}')" type="button" style="background: rgb(89,182,195);border-color: rgb(89,182,195);">${element}`); });
})
}

// haalt de zoektermen op
function getSearchTerms(subcategory, category) {
    console.log(subcategory);
    document.getElementById("categories").innerHTML = "";
    additioncard.style.display = "block";
    fetch(`http://localhost:8080/searchterms/${subcategory}`)
        .then(response => response.json())
        .then(data => {
            let list = data.all;
            console.log(list);
            let wordslist = document.getElementById("woorden");
            wordslist.innerHTML = "";
            document.getElementById("cardtitle").innerHTML = subcategory;
            curcat = subcategory;
            let breadcrumb = document.getElementById("breadcrumb");
            breadcrumb.innerHTML = `<li onclick="getCategories()" class="breadcrumb-item"><a href="#"><span>Domeinen</span></a></li> <li onclick="getSubCategorie('${category}')" class="breadcrumb-item"><a href="#"><span>${category}</span></a></li>`
            list.forEach(element => {
                wordslist.insertAdjacentHTML('beforeend', `<div id="div${element.ID}" class="d-flex align-items-center" style="border-right-width: 1px;">
                <p style="margin-top: 12px;margin-right: 12px;margin-left: 12px;">${element.name}</p><button onclick="deleteWord(${element.ID})" class="btn btn-primary" type="button" style="background: rgb(223,87,78);border-color: rgb(255,255,255);">Delete</button>
            </div>`)
});
})
}

// verwijderd een zoekterm uit de database
function deleteWord(word) {
    console.log(word);
    fetch(`http://localhost:8080/delete/searchterms?id=${word}&session=${localStorage.getItem("session")}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.status == "deleted") {
                document.getElementById(`div${word}`).remove();
            }
        })

}

// voegt een zoekterm toe aan de database
function addWord() {
    let word = document.getElementById("newword").value;
    console.log(word);
    fetch(`http://localhost:8080/add/searchterms?term=${word}&subcategory=${curcat}&session=${localStorage.getItem("session")}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.status == "denied") {
                alert("You are not allowed to do this");
                console.log("You are not allowed to do this");
            } else if (data.status == "failed") {
                console.log("failed");
                document.getElementById("errortext").style.display = "block";
                //hide after 3 seconds
                setTimeout(function () {
                    document.getElementById("errortext").style.display = "none";
                }, 3000);
            } else {
                document.getElementById("woorden").insertAdjacentHTML('beforeend', `<div id="div${data.status.ID}" class="d-flex align-items-center" style="border-right-width: 1px;">
                <p style="margin-top: 12px;margin-right: 12px;margin-left: 12px;">${word}</p><button onclick="deleteWord(${data.status.ID})" class="btn btn-primary" type="button" style="background: rgb(223,87,78);border-color: rgb(255,255,255);">Delete</button>
            </div>`)
            }
        })
    word.value = "";

}

// checkt de status van de herberekening van de scores
function checkScores() {
    fetch(`http://vichogent.be:40046/api/status`)
        .then(response => response.json())
        .then(data => {
            if (data.status == "done") {
                document.getElementById("recalc").innerHTML = "Herbereken scores";
                document.getElementById("recalc").onclick = herberekenScores;
                document.getElementById("recalc").title = "Herbereken de scores van de verschillende categorie??n.";

            } else {
                document.getElementById("recalc").innerHTML = "Scores aan het herberekenen...";
                document.getElementById("loadingscreen").style.display = "block";
                document.getElementById("recalc").style.backgroundColor = "rgb(230, 158, 151)";
                document.getElementById("recalc").style.borderColor = "rgb(230, 158, 151)";
                document.getElementById("recalc").onclick = "alert('Scores worden herberekend, dit kan een paar minuten duren.')";
                document.getElementById("resultset").style.display = "none";
                realoadWhenDone();
                console.log("recalculating");
            }

        })
}

// start het herberekenen van de scores
function herberekenScores() {
    let confirmation = confirm("Scores worden herberekend, dit kan een paar minuten duren.", "Herbereken scores", "Annuleer");
        if (confirmation) {
        document.getElementById("loadingscreen").style.display = "block"
        document.getElementById("recalc").innerHTML = "Scores aan het herberekenen...";
        document.getElementById("recalc").style.backgroundColor = "rgb(230, 158, 151)";
        document.getElementById("recalc").style.borderColor = "rgb(230, 158, 151)";
        document.getElementById("resultset").style.display = "none";
        fetch(`http://vichogent.be:40046/api/recalculate/DikkeBerta`)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                document.getElementById("loadingscreen").style.display = "none";
                window.location.reload();
                alert("Scores zijn herberekend.")
                
            })
    } else {
        console.log("not confirmed");
        document.getElementById("loadingscreen").style.display = "none";
    }
}

// luistert of de herberekening klaar is en herlaadt de pagina als dat zo is.
function realoadWhenDone() {
    fetch(`http://vichogent.be:40046/api/status`)
        .then(response => response.json())
        .then(data => {
            if (data.status == "done") {
                window.location.reload();
                console.log("Recalculation done");
            } else {
                setTimeout(realoadWhenDone, 1000);
            }
        })
}

// luistert naar een enter key 
function enterkeylistner() {
    document.getElementById("newword").addEventListener("keyup", (event) => {
        if (event.key === "Enter") {
          addWord();
        }
      });
    }


function init () {
    getCategories();
    checkSession();
    enterkeylistner();
    checkScores();
    document.getElementById("loadingscreen").style.display = "none"

}

window.onload = init;