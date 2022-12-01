
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

  /** Naar dashboard pagina gaan van een bedrijf via het btw-nummer
   */
  function getFromBTW(btw) {
    fetch(`http://localhost:8080/bedrijf/btw/${btw}`)
      .then((res) => res.json())
      .then((date) => {
        return date;
      })
      .then((data) => {
        console.log(data.bedrijven.length);
        if (data.bedrijven.length == 0) {
            document.getElementById("resultset").style.display = "none";
        } else{
            document.location.href = `search.html?btw=${data.bedrijven[0].ondernemingsNummer}`;}
      })
      .catch((error) => {
        console.log(error);
      });
  }

    /** Naar dashboard pagina gaan van een bedrijf via de naam*/
  function getFromNaam(naam) {
    fetch(`http://localhost:8080/bedrijf/naam/${naam}`)
      .then((res) => res.json())
      .then((date) => {
        return date;
      })
      .then((data) => {
        console.log(data.bedrijven.length);
        if (data.bedrijven.length == 0) {
            document.getElementById("resultset").style.display = "none";
        } else{
            document.location.href = `search.html?btw=${data.bedrijven[0].ondernemingsNummer}`;}
      })
      .catch((error) => {
        console.log(error);
      });
  }

  /** Controleert of de waarde in de searchbar een btw-nummer of een bedrijfsnaam is en zoekt deze */
  function zoek() {
    let zoekwaarde = document.getElementById("searchbar").value
    try {
        if (zoekwaarde.startsWith("BE") || zoekwaarde.startsWith("be") || digits.includes(parseInt(zoekwaarde[2]))) {
            getFromBTW(zoekwaarde);
        } else {
            getFromNaam(zoekwaarde);
        }
    } catch (error) {}
  }

  /** gaat een suggestie geven wanneer je een btw-nummer ingeeft in de searchbar 
 * :par_btw: het btw nummer van het bedrijf
*/
  function typeSugBTW(btw) {
    fetch(`http://localhost:8080/bedrijf/btw/${btw}`)
      .then((res) => res.json())
      .then((date) => {
        return date;
      })
      .then((data) => {
          let options = document.getElementById("options")
          console.log(data.bedrijven)
          options.innerHTML = ""
          let i = 0;
          let mtop = 10
          while (i < data.bedrijven.length) { 
            let bedrijf = data.bedrijven[i].name.replace("'", "")
            if (i > 0) {
                mtop = 0
            }
            options.insertAdjacentHTML("beforeend", `<a class="choice" href="${"search.html?btw="+data.bedrijven[i].ondernemingsNummer}" style="margin-left: 0px;min-width: 90%;margin-top: ${mtop}px;margin-bottom: 10px;">
            <div id="chdiv" style="min-width: 90%;margin-top: 0px;margin-bottom: 0px;background: rgba(252,252,252,0.46);border-radius: 5px;">
                <p style="margin-bottom: 0px;margin-left: 5px;">${bedrijf}</p>
            </div>
        </a>`)
            i+=1}
          
          
        })
      .catch((error) => {
        console.log(error);
      });
  }

  /**gaat een suggestie geven wanneer je een naam ingeeft in de searchbar 
 * :par_naam: de naam van het bedrijf
 */
  function typeSugName(naam) {
    fetch(`http://localhost:8080/bedrijf/naam/${naam}`)
      .then((res) => res.json())
      .then((date) => {
        return date;
      })
      .then((data) => {
          let options = document.getElementById("options")
          console.log(data.bedrijven)
          options.innerHTML = ""
          let i = 0;
          let mtop = 10
          while (i < data.bedrijven.length) { 
            let bedrijf = data.bedrijven[i].name.replace("'", "")
            if (i > 0) {
                mtop = 0
            }
            options.insertAdjacentHTML("beforeend", `<a class="choice" href="${"search.html?btw="+data.bedrijven[i].ondernemingsNummer}" style="margin-left: 0px;min-width: 90%;margin-top: ${mtop}px;margin-bottom: 10px;">
            <div id="chdiv" style="min-width: 90%;margin-top: 0px;margin-bottom: 0px;background: rgba(252,252,252,0.46);border-radius: 5px;">
                <p style="margin-bottom: 0px;margin-left: 5px;">${bedrijf}</p>
            </div>
        </a>`)
            i+=1}
          
          
        })
      .catch((error) => {
        console.log(error);
      });
  }

  /** checkt of de ingegeven waarde in de searchbar een btw-nummer of een naam is */
  function getTypeSug() {
    let zoekwaarde = document.getElementById("searchbar").value
    try {
        if (zoekwaarde.startsWith("BE") || zoekwaarde.startsWith("be") || digits.includes(parseInt(zoekwaarde[2]))) {
            typeSugBTW(zoekwaarde);
        } else {
            typeSugName(zoekwaarde);
        }
    } catch (error) {}
  }

  /** het displayen van het suggestie-menu */
  function suggestOn() {
    document.getElementById("options").style.display = "flex";
    getTypeSug();

  }

  /** het verbergen van het suggestie-menu */
  function suggestOff() {
    document.getElementById("options").style.display = "none";
}

/** controleert of er in de local storage staat of de notificatie ooit al aangeklikt is */
function checkAlert() {
    const beta = localStorage.getItem('betaAlert');
    if (beta == null) {
        document.getElementById("alert").insertAdjacentHTML("afterbegin", `<span class="badge bg-danger badge-counter">1</span>`)
    }
}

/**Verwijdert de notificatiebadge wanneer er op gelklikt wordt en slaat die ook op in de local storage  */
function removeAlert() {
    const beta = localStorage.getItem('betaAlert');
    if (beta != "seen") {
        localStorage.setItem("betaAlert", "seen");
        document.getElementById("alert").innerHTML = `<i class="fas fa-bell fa-fw"></i>`
    } 
}

/** Suggesties uitzetten en alerts checken
 * zoeken bij enter of bij een klik op de gepaste knop
 * zet een listner op je toetsenbord en detecteerd het intypen van letters of een enter
 */
function init() {
    suggestOff();
    try{
      const vars = getUrlVars();
      if(vars.btw != undefined){
        document.getElementById("searchbar").value = vars.btw;
        zoek();
      }
    } catch{}
    document.getElementById("searchsection").onclick = function() {suggestOff();}
    document.getElementById("options").style.display = "none";
    digits = [0,1,2,3,4,5,6,7,8,9]
    document.getElementById("searchbtn").onclick = function() {zoek()}
    document.getElementById("searchbar").addEventListener("keyup", function(){
        if (event.keyCode === 13) {
        event.preventDefault();
        suggestOff();
          zoek();

       } else{
         if (document.getElementById("searchbar").value == '') {
           console.log("leeg")
           suggestOff();
         } else {
          suggestOn();
         }
       }
    })
}

window.onload = init;