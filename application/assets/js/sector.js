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

  /** Haalt de data van een sector op en plaatst de data op het dashboard */
  function getSector() {
    fetch(`http://localhost:8080/sector?sector=${getUrlVars().sector}`)
      .then((res) => res.json())
      .then((date) => {
        return date;
      })
      .then((data) => {
        console.log(data)
        document.getElementById("naam").innerHTML = data.naam;
        document.getElementById("aantal").innerHTML = data.aantal;
        let totalturnover = 0;
        let totalemployees = 0;
        let totalscore = 0;
        let total = 0;
        data.bedrijven.forEach((bedrijf) => {
          totalturnover += parseFloat(bedrijf.turnover);
          totalscore += parseFloat(bedrijf.score);
          totalemployees += bedrijf.personeel;
        });
        console.log(totalturnover);
        console.log((data.aantal));
        document.getElementById("omzettot").innerHTML = "€ " + numberWithCommas(totalturnover);
        document.getElementById("omzetgem").innerHTML = "€ " + numberWithCommas(parseInt(totalturnover / data.aantal));
        document.getElementById("werknemerstot").innerHTML = totalemployees;
        document.getElementById("werknemersgem").innerHTML = parseInt(totalemployees / data.aantal);
        document.getElementById("nacebel").innerHTML = getUrlVars().sector;
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

/**Verwijdert de notificatiebadge wanneer er op gelklikt wordt en slaat die ook op in de local storage  */
function removeAlert() {
  const beta = localStorage.getItem('betaAlert');
  if (beta != "seen") {
      localStorage.setItem("betaAlert", "seen");
      document.getElementById("alert").innerHTML = `<i class="fas fa-bell fa-fw"></i>`
  } 
}

/** grote getallen leesbaar maken door een punt te zetten om de 3 cijfers */
function numberWithCommas(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

/** Roept alle functies aan en corigeert verkeerde namen  */
  function init() {
    //document.getElementById("charttttt").style.display = "none"
    getSector();
    /*getsectorzoektermen();*/
    document.getElementById("naam").innerHTML = unescape(getUrlVars().sector).replace("Ã«","ë");
    document.getElementById("bedrijvenbtn").href = "bedrijven.html?sector=" + getUrlVars().sector;
  }

window.onload = init;

/**/