/**Deze functie gaat de variabelen (?var=value) uitlezen  */
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

/**Deze functie gaat grote getallen duidelijk displayen  */
function formatNumber(num) {
  return num.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1.')
}

/** Deze functie gaat data van tabel 'bedrijven' ophalen via het btwnummer en op het dashboard plaatsen
 * :par_btw: het btw-nummer van het bedrijf
 */
function getFromBTW(btw) {
  fetch(`http://localhost:8080/bedrijf/btw/${btw}`)
    .then((res) => res.json())
    .then((date) => {
      return date;
    })
    .then((data) => {
      if (data.bedrijven.length == 0) {
          document.getElementById("resultset").style.display = "none";
      } else{
      document.getElementById("sector").innerHTML = data.bedrijven[0].sector
      document.getElementById("sectorlink").href = `sector.html?sector=${data.bedrijven[0].nacebelCode}`;
      //document.getElementById("resultset").style.display = "block";
      let mapsadress = data.bedrijven[0].street.replace(" ", "+")
      console.log(data.bedrijven[0].name);
      document.getElementById("naam").innerHTML = data.bedrijven[0].name
      document.getElementById("btwnum").innerHTML = data.bedrijven[0].ondernemingsNummer
      getFinanceData(data.bedrijven[0].ondernemingsNummer)
      localStorage.setItem("btwnum", data.bedrijven[0].ondernemingsNummer)
      document.getElementById("werknemers").innerHTML = data.bedrijven[0].employees
      document.getElementById("nacebel").innerHTML = data.bedrijven[0].nacebelCode
      localStorage.setItem("nacebel", data.bedrijven[0].nacebelCode)
      console.log(data.bedrijven[0].score);
      if (data.bedrijven[0].score!= null){
        loadscoregraph(data.bedrijven[0].score)}
      let score = data.bedrijven[0].score == null ? "Geen score" : data.bedrijven[0].score
      document.getElementById("score").innerHTML = `${parseFloat(score).toFixed(5).replace(".", ",")}%`
      document.getElementById("pdflink").href = `https://consult.cbso.nbb.be/api/external/broker/public/deposits/pdf/${data.bedrijven[0].nbbID}`
      let websiteicon = document.getElementById("websitelink");
      let website = data.bedrijven[0].website
      if (website != null){
        if (!website.toLowerCase().startsWith("https") && !website.toLowerCase().startsWith("http")) {
          website = `https://${website}`
          websiteicon.href = website
        } else if (website.toLowerCase().startsWith("https") || website.toLowerCase().startsWith("http")) {
          websiteicon.href = website
        }else{websiteicon.style.display = "none"}
      }
      document.getElementById("locatie").innerHTML = `<a href="https://www.google.com/maps/place/${mapsadress},+${data.bedrijven[0].zipcode}+${data.bedrijven[0].city}" target="_blank">${data.bedrijven[0].city}</a>`
      //getKMOdata(data.bedrijven[0].ondernemingsNummer);
      console.log(data.bedrijven[0].telephone);
      if (data.bedrijven[0].telephone != null){
        document.getElementById("phone").href = `tel:${data.bedrijven[0].telephone}`
        document.getElementById("phone").title = data.bedrijven[0].telephone
      } else {document.getElementById("phone").style.display = "none"}
      
    }
    })
    .catch((error) => {
      console.log(error);
    });
}
/**Deze functie gaat data van tabel 'bedrijven' ophalen via het btwnummer en op het dashboard plaatsen
 * :par_naam: de naam van het bedrijf
  */
function getFromNaam(naam) {
  fetch(`http://localhost:8080/bedrijf/naam/${naam}`)
    .then((res) => res.json())
    .then((date) => {
      return date;
    })
    .then((data) => {
      if (data.bedrijven.length == 0) {
          document.getElementById("resultset").style.display = "none";
      } else{
      document.getElementById("sector").innerHTML = data.bedrijven[0].sector
      document.getElementById("resultset").style.display = "block";
      let mapsadress = data.bedrijven[0].street.replace(" ", "+")
      console.log(data.bedrijven[0].name);
      document.getElementById("naam").innerHTML = data.bedrijven[0].name
      document.getElementById("nacebel").innerHTML = data.bedrijven[0].nacebelCode
      document.getElementById("sector").innerHTML = data.bedrijven[0].sector
      localStorage.setItem("nacebel", data.bedrijven[0].nacebelCode)
      localStorage.setItem("btwnum", data.bedrijven[0].ondernemingsNummer)
      document.getElementById("btwnum").innerHTML = data.bedrijven[0].ondernemingsNummer
      getFinanceData(data.bedrijven[0].ondernemingsNummer)
      document.getElementById("werknemers").innerHTML = data.bedrijven[0].employees
      console.log(data.bedrijven[0].score);
      if (data.bedrijven[0].score!= null){
        loadscoregraph(data.bedrijven[0].score)}
      let score = data.bedrijven[0].score == null ? "Geen score" : data.bedrijven[0].score
      document.getElementById("score").innerHTML = `${parseFloat(score).toFixed(5).replace(".", ",")}%`

      let websiteicon = document.getElementById("websitelink");
      let website = data.bedrijven[0].website
      if (website != null){
        if (!website.toLowerCase().startsWith("https") && !website.toLowerCase().startsWith("http")) {
          website = `https://${website}`
          websiteicon.href = website
        } else {websiteicon.style.display = "none"}
      }
      document.getElementById("locatie").innerHTML = `<a href="https://www.google.com/maps/place/${mapsadress},+${data.bedrijven[0].zipcode}+${data.bedrijven[0].city}" target="_blank">${data.bedrijven[0].city}</a>`
      //getKMOdata(data.bedrijf[0].Ondernemingsnummer);
      if (data.bedrijven[0].telephone != null){
        document.getElementById("phone").href = `tel:${data.bedrijven[0].telephone}`
        document.getElementById("phone").title = data.bedrijven[0].telephone
      } else {document.getElementById("phone").style.display = "none"}
      }
    })
    .catch((error) => {
      console.log(error);
    });
}

/**Neemt de waarde uit de searchbar en zoekt een bedrijf met deze waarde */
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
      console.log("fout: "+ error);
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
          let bedrijf = data.bedrijven[i].name
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





function loadscoregraph(score) {
  var ctxL = document.getElementById("lineChart").getContext('2d');
var myLineChart = new Chart(ctxL, {
  type: 'line',
  data: {
    labels: [2021],
    datasets: [
    {
      label: "Score",
      data: [score],
      backgroundColor: [
        'rgba(0, 137, 132, .2)',
      ],
      borderColor: [
        'rgb(89, 182, 195, .7)',
      ],
      borderWidth: 3
    }
    ]
  },
  options: {
    responsive: true
  }
});
}

function getFinanceData(btw) {
  fetch(`http://localhost:8080/bedrijf/finance/${btw}`)
   .then(response => response.json())
   .then(data => {
    data = data.finance
    console.log(data)
      let omzet = document.getElementById("omzet")
      omzet.innerHTML = data.turnover
      let balans = document.getElementById("balans")
      balans.innerHTML = data.total_assets
      let beurs = document.getElementById("beurs")
      beurs.innerHTML = data.beursgenoteerd ? `<i class="fas fa-chart-line" title="Beursgenoteerd"></i>` : `<i class="fas fa-times" title="Niet beursgenoteerd"></i>`
   })
}



/*function getJaarRekening(btw) {
  newbtw = btw.toLowerCase().replace("be", "")
  console.log(newbtw);
  fetch(`http://www.vichogent.be:40020/api/jaarrekening/${newbtw}`)
    .then((res) => res.json())
    .then((data) => {
        console.log(data);
        if (data.Werknemers != "") {
          document.getElementById("werknemers").innerHTML = Math.ceil(data.Werknemers)
        }
        if (data.Omzet != "") {
          document.getElementById("omzet").innerHTML = `€ ${data.Omzet}`
        }
        if (data.Balanstotaal != "") {
          document.getElementById("balans").innerHTML = `€ ${data.Balanstotaal}`
        }
      })
    .catch((error) => {
      console.log(error);
    });
}*/

/*function getSector(btw) {
  newbtw = btw.toLowerCase().replace("be", "")
  fetch(`http://www.vichogent.be:40020/api/pubsearch/${newbtw}`)
    .then((res) => res.json())
    .then((data) => {
        console.log(data);
        if (data.SectorAlgemeen != "") {
          document.getElementById("sector").innerHTML = data.SectorAlgemeen
        }
        if (data.SectorDetail != "") {
          document.getElementById("sectordetail").innerHTML = String(data.SectorDetail).replace(",", ", ")
        }
      })
    .catch((error) => {
      console.log(error);
    });
}*/
/** Vertaalt de locatiescore naar html-icons
 * :par_number: locatiescore 
  */
function getIcons(number) {
  if (number == 0) {
    return ""
  } else if (number == 1) {
    return `<i class="fas fa-globe-americas" id="zoektermwebsite" style="color: #dddfeb;padding-left:15px;font-size: 15px;" title="Website"></i>`
  } else if (number == 2) {
    return `<i class="fas fa-file-pdf" id="zoektermpdf" style="color: rgb(221,223,235);font-size: 15px;padding-left: 15px;padding-right: 10px;" title="Jaarrekening"></i>`
  } else {
    return `<i class="fas fa-file-pdf" id="zoektermpdf" style="color: rgb(221,223,235);font-size: 15px;padding-left: 15px;padding-right: 10px;" title="Jaarrekening"></i><i class="fas fa-globe-americas" id="zoektermwebsite" style="color: #dddfeb;font-size: 15px;" title="Website"></i>`
  }
}

/** grote getallen leesbaar maken door een punt te zetten om de 3 cijfers */
function numberWithCommas(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}
/** Suggesties uitzetten en alerts checken
 * zoeken bij enter of bij een klik op de gepaste knop
 * zet een listner op je toetsenbord en detecteerd het intypen van letters of een enter
 */
function init() {
suggestOff();  try{
    const vars = getUrlVars();
    if(vars.btw != undefined){

      document.getElementById("searchbar").value = vars.btw;
      getFromBTW(vars.btw);
      //zoek();
    } else {
      console.log("no vars");
    }
  } catch{}
  document.getElementById("resultset").onclick = function() {suggestOff();}
  document.getElementById("options").style.display = "none";
  digits = [0,1,2,3,4,5,6,7,8,9]
  document.getElementById("searchbtn").onclick = function() {zoek()}
  document.getElementById("searchbar").addEventListener("keyup", function(){
      if (event.keyCode === 13) {
      event.preventDefault();
      suggestOff();
        zoek();
      
     } else{
       if (document.getElementById("searchbar").value == "") {
         console.log("leeg")
         suggestOff();
       } else {
        suggestOn();
       }
     }
  })
  
  /*getSector(document.getElementById("searchbar").value);
  getJaarRekening(document.getElementById("searchbar").value);*/
  //getCodingTree(document.getElementById("searchbar").value);
}

window.onload = init;