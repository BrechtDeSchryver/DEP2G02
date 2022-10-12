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
    fetch(`http://vichogent.be:40021/getsectordata/${getUrlVars().sector}`)
      .then((res) => res.json())
      .then((date) => {
        return date;
      })
      .then((data) => {
        console.log(data)
        const sdata = data.sectordata[0][0]
        console.log(sdata)
        document.getElementById("werknemerstot").innerHTML = sdata.Personeel_totaal;
        document.getElementById("werknemersgem").innerHTML = Math.floor(sdata.Personeel_gem);
        document.getElementById("omzettot").innerHTML = `€ ${numberWithCommas(sdata.Omzet_totaal)}`;
        document.getElementById("omzetgem").innerHTML = `€ ${numberWithCommas(Math.floor(sdata.Omzet__gem))}`;
        document.getElementById("aantal").innerHTML = Math.floor(sdata.aantal);
    })
      .catch((error) => {
        console.log(error);
      });
}

  /** De duurzaamheidsscore van alle bedrijven binnen een bepaalde sector op het dashboard plaatsen */
  function getDuurzaamheid() {
    fetch(`http://www.vichogent.be:40021/getsectorduurzaamheid/${getUrlVars().sector}`)
      .then((res) => res.json())
      .then((date) => {
        return date;
      })
      .then((data) => {
        /*console.log(data)*/
        const duurz = data.sectorduurzaamheid[0];
        let i = 0;
        while (i < duurz.length) {
          document.getElementById("tbody").insertAdjacentHTML("beforeend", `
          <tr id="row">
            <td>${duurz[i].score_duurzaamheid}</td>
            <td>${duurz[i].aantal}</td>
          </tr>
          `)
          i +=1;
        }


    })
      .catch((error) => {
        console.log(error);
      });
}
/*
function getsectorzoektermen() {
  fetch(`http://www.vichogent.be:40021/getsectorzoektermen/${getUrlVars().sector}`)
  .then((data) => data.json())
  .then((data) => {
    const sdata = data.sectorzoektermen[0];
    console.log(sdata)
    let i = 0;
    while (i < sdata.length) {
      let globe = 'inline'
      let pdf = 'inline'
      if (sdata[i].score_zoektermen == 2 || sdata[i].score_zoektermen == 0) {globe = 'none'}
      if (sdata[i].score_zoektermen == 1 || sdata[i].score_zoektermen == 0) {pdf = 'none'}
      document.getElementById("tbodys").insertAdjacentHTML("beforeend", `
          <tr id="row">
          <td><i class="fas fa-file-pdf" style="margin-right: 10px;display:${pdf}"></i><i class="fas fa-globe-americas" style=display:${globe}></i></td>
            
            <td>${sdata[i].aantal}</td>
          </tr>
          `)
      i +=1
    }
  })
}*/

/** Maakt een grafiek voor het gemiddelde van HumanCapital en NaturalCapital voor een bepaalde sector */
function createChart() {
  fetch(`http://vichogent.be:40021/getAvgRaportering/${getUrlVars().sector}`)
      .then((res) => res.json())
      .then((date) => {
        return date;
      })
      .then((data) => {
        /*console.log(data.avgRaportering[0][0])*/
        const avgRaportering = data.avgRaportering[0][0]
        var ctxD = document.getElementById("pieChart").getContext('2d');
  var myLineChart = new Chart(ctxD, {
    type: 'doughnut',
    data: {
      labels: ["Gendergelijkheid", "Implementatie Werknemersrechten", "Sociale relaties op het werk", "Werkgelegenheid", "Organisatie op het werk", "Gezondheid & veiligheid", "Opleidingsbeleid", "SDG"],
      datasets: [{
        data: [avgRaportering.avgGENDERGELIJKHEID, avgRaportering.avgIMPLEMENTATIE_WERKNEMERSRECHTEN, avgRaportering.avgSOCIALE_RELATIES_OP_HET_WERK, avgRaportering.avgWERKGELEGENHEID, avgRaportering.avgORGANISATIE_OP_HET_WERK, avgRaportering.avgGEZONDHEID_EN_VEILIGHEID, avgRaportering.avgOPLEIDINGSBELEID, avgRaportering.avgSDG_H],
        backgroundColor: ["#4251f5", "#46BFBD", "#FDB45C", "#949FB1", "#4D5360", "#F7464A", "#00ff40", "#e300f7"],/*#F7464A, #FF5A5E*/
        hoverBackgroundColor: ["#656fe0", "#5AD3D1", "#FFC870", "#A8B3C5", "#616774", "#FF5A5E", "#41fa6f", "#ea88f2"]
      }]
    },
    options: {
      responsive: true
    }
  });

  var ctxD = document.getElementById("pieChartt").getContext('2d');
  var myLineChartt = new Chart(ctxD, {
    type: 'doughnut',
    data: {
      labels: ["Gebruik van energiebronnen", "Gebruik van waterbronnen", "Emissies van broeikasgassen", "Vervuilende uitstoot", "Milieu impact", "Impact op gezondheid & veiligheid", "Verdere eisen over bepaalde onderwerpen", "Milieu beleid", "SDG"],
      datasets: [{
        data: [avgRaportering.avgGEBRUIK_VAN_ENERGIEBRONNEN, avgRaportering.avgGEBRUIK_VAN_WATERBRONNEN, avgRaportering.avgEMISSIES_VAN_BROEIKASGASSEN, avgRaportering.avgVERVUILENDE_UITSTOOT, avgRaportering.avgMILIEU_IMPACT, avgRaportering.avgIMPACT_OP_GEZONDHEID_EN_VEILIGHEID, avgRaportering.avgVERDERE_EISEN_OVER_BEPAALDE_ONDERWERPEN, avgRaportering.avgMILIEU_BELEID, avgRaportering.avgSDG_N],
        backgroundColor: ["#F7464A", "#46BFBD", "#FDB45C", "#949FB1", "#4D5360", "#4251f5", "#00ff40", "#e300f7"],
        hoverBackgroundColor: ["#FF5A5E", "#5AD3D1", "#FFC870", "#A8B3C5", "#616774", "#656fe0", "#41fa6f", "#ea88f2"]
      }]
    },
    options: {
      responsive: true
    }
  });
        })
      .catch((error) => {
        console.log(error);
      });
  /*<div style="color: rgb(89,182,195) !important;"><div class="chartjs-size-monitor"><div class="chartjs-size-monitor-expand"><div class=""></div></div><div class="chartjs-size-monitor-shrink"><div class=""></div></div></div><canvas data-bss-chart="{&quot;type&quot;:&quot;pie&quot;,&quot;data&quot;:{&quot;labels&quot;:[&quot;January&quot;,&quot;February&quot;],&quot;datasets&quot;:[{&quot;label&quot;:&quot;Revenue&quot;,&quot;backgroundColor&quot;:[&quot;rgb(239,2,2)&quot;,&quot;rgb(255,138,0)&quot;],&quot;borderColor&quot;:[&quot;#4e73df&quot;,&quot;#4e73df&quot;],&quot;data&quot;:[&quot;4500&quot;,&quot;5300&quot;]}]},&quot;options&quot;:{&quot;maintainAspectRatio&quot;:true,&quot;legend&quot;:{&quot;display&quot;:false,&quot;labels&quot;:{&quot;fontStyle&quot;:&quot;normal&quot;,&quot;fontColor&quot;:&quot;rgb(89,182,195) !important&quot;}},&quot;title&quot;:{&quot;fontStyle&quot;:&quot;bold&quot;,&quot;text&quot;:&quot;&quot;}}}" style="display: block; width: 467px; height: 233px;" width="467" height="233" class="chartjs-render-monitor"></canvas></div>*/
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
    document.getElementById("charttttt").style.display = "none"
    checkAlert();
    document.getElementById("alert").onclick = function() {removeAlert()};
    getSector();
    getDuurzaamheid();
    createChart();
    /*getsectorzoektermen();*/
    document.getElementById("naam").innerHTML = unescape(getUrlVars().sector).replace("Ã«","ë");
  }

window.onload = init;

/**/