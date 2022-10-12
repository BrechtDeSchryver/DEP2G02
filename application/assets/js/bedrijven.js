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
  fetch(`http://www.vichogent.be:40021/btw/${btw}`)
    .then((res) => res.json())
    .then((date) => {
      return date;
    })
    .then((data) => {
      if (data.bedrijf.length == 0) {
          document.getElementById("resultset").style.display = "none";
      } else{
      document.getElementById("sector").innerHTML = data.bedrijf[0].Ibid_omschrijving
      document.getElementById("resultset").style.display = "block";
      let mapsadress = data.bedrijf[0].Adres.replace(" ", "+")
      console.log(data.bedrijf[0].Naam);
      document.getElementById("naam").innerHTML = data.bedrijf[0].Naam
      document.getElementById("btwnum").innerHTML = data.bedrijf[0].BvD_ID_nummer
      document.getElementById("werknemers").innerHTML = data.bedrijf[0].Personeelsbestand_Laatste_jaar_Laatst_beschikb_jr
      document.getElementById("pdflink").href = `https://consult.cbso.nbb.be/api/external/broker/public/deposits/pdf/${data.bedrijf[0].nbbid}`
      let websiteicon = document.getElementById("websitelink");
      let website = data.bedrijf[0].Web_adres
      if (website != null){
        if (!website.toLowerCase().startsWith("https") && !website.toLowerCase().startsWith("http")) {
          website = `https://${website}`
          websiteicon.href = website
        } else if (website.toLowerCase().startsWith("https") || website.toLowerCase().startsWith("http")) {
          websiteicon.href = website
        }else{websiteicon.style.display = "none"}
      }
      if (data.bedrijf[0].Omzet_EUR_Laatst_beschikb_jr.toLowerCase().startsWith("n.b")) {
          document.getElementById("omzet").innerHTML = `€ ${formatNumber(data.bedrijf[0].Omzet_EUR_Laatst_beschikb_jr)}`
      } else {
          document.getElementById("omzet").innerHTML = `€ ${formatNumber(data.bedrijf[0].Omzet_EUR_Laatst_beschikb_jr)}`
      }
      document.getElementById("locatie").innerHTML = `<a href="https://www.google.com/maps/place/${mapsadress},+${data.bedrijf[0].Postcode}+${data.bedrijf[0].Gemeente}" target="_blank">${data.bedrijf[0].Gemeente}</a>`
      getKMOdata(data.bedrijf[0].Ondernemingsnummer);
      console.log(data.bedrijf[0].Telefoon)
      if (data.bedrijf[0].Telefoon != null){
        document.getElementById("phone").href = `tel:${data.bedrijf[0].Telefoon}`
        document.getElementById("phone").title = data.bedrijf[0].Telefoon
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
  fetch(`http://www.vichogent.be:40021/bedrijf/${naam}`)
    .then((res) => res.json())
    .then((date) => {
      return date;
    })
    .then((data) => {
      if (data.bedrijf.length == 0) {
          document.getElementById("resultset").style.display = "none";
      } else{
      document.getElementById("sector").innerHTML = data.bedrijf[0].Ibid_omschrijving
      document.getElementById("resultset").style.display = "block";
      let mapsadress = data.bedrijf[0].Adres.replace(" ", "+")
      console.log(data.bedrijf[0].Naam);
      document.getElementById("naam").innerHTML = data.bedrijf[0].Naam
      document.getElementById("sector").innerHTML = data.bedrijf[0].Ibid_omschrijving
      document.getElementById("btwnum").innerHTML = data.bedrijf[0].BvD_ID_nummer
      document.getElementById("werknemers").innerHTML = data.bedrijf[0].Personeelsbestand_Laatste_jaar_Laatst_beschikb_jr
      let websiteicon = document.getElementById("websitelink");
      let website = data.bedrijf[0].Web_adres
      if (website != null){
        if (!website.toLowerCase().startsWith("https") && !website.toLowerCase().startsWith("http")) {
          website = `https://${website}`
          websiteicon.href = website
        } else {websiteicon.style.display = "none"}
      }
      if (data.bedrijf[0].Omzet_EUR_Laatst_beschikb_jr.toLowerCase().startsWith("n.b")) {
          document.getElementById("omzet").innerHTML = `€ ${formatNumber(data.bedrijf[0].Omzet_EUR_Laatst_beschikb_jr)}`
      } else {
          document.getElementById("omzet").innerHTML = `€ ${formatNumber(data.bedrijf[0].Omzet_EUR_Laatst_beschikb_jr)}`
      }
      document.getElementById("locatie").innerHTML = `<a href="https://www.google.com/maps/place/${mapsadress},+${data.bedrijf[0].Postcode}+${data.bedrijf[0].Gemeente}" target="_blank">${data.bedrijf[0].Gemeente}</a>`
      getKMOdata(data.bedrijf[0].Ondernemingsnummer);
      if (data.bedrijf[0].Telefoon != null){
        document.getElementById("phone").href = `tel:${data.bedrijf[0].Telefoon}`
        document.getElementById("phone").title = data.bedrijf[0].Telefoon
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
  fetch(`http://www.vichogent.be:40021/btw/${btw}`)
    .then((res) => res.json())
    .then((date) => {
      return date;
    })
    .then((data) => {

        let options = document.getElementById("options")
        console.log(data.bedrijf)
        options.innerHTML = ""
        let i = 0;
        let mtop = 10
        while (i < data.bedrijf.length) { 
          let bedrijf = data.bedrijf[i].Naam.replace("'", "")
          if (i > 0) {
              mtop = 0
          }
          options.insertAdjacentHTML("beforeend", `<a class="choice" href="${"search.html?btw="+data.bedrijf[i].BvD_ID_nummer}" style="margin-left: 0px;min-width: 90%;margin-top: ${mtop}px;margin-bottom: 10px;">
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
  fetch(`http://www.vichogent.be:40021/bedrijf/${naam}`)
    .then((res) => res.json())
    .then((date) => {
      return date;
    })
    .then((data) => {
        let options = document.getElementById("options")
        console.log(data.bedrijf)
        options.innerHTML = ""
        let i = 0;
        let mtop = 10
        while (i < data.bedrijf.length) { 
          let bedrijf = data.bedrijf[i].Naam
          if (i > 0) {
              mtop = 0
          }
          options.insertAdjacentHTML("beforeend", `<a class="choice" href="${"search.html?btw="+data.bedrijf[i].BvD_ID_nummer}" style="margin-left: 0px;min-width: 90%;margin-top: ${mtop}px;margin-bottom: 10px;">
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
/** Alle data uit tabel 'codingTree' fetchen 
 * plaatst de data op het dashboard
 * gaat de kleur aanpassen naargelang de score
 * vertaalt de locatiescore naar de html-icoontjes 
 */
function getCodingTree(btw) {
  newbtw = btw.toLowerCase().replace("be", "")
  fetch(`http://www.vichogent.be:40021/codingTree/${newbtw}`)
  .then((data) => data.json())
  .then((data) => {
    const codingTree = data.codingTree[0]

    document.getElementById("score").innerHTML = codingTree.score_duurzaamheid;
    document.getElementById("scorebox").setAttribute("data-bs-original-title", codingTree.percentagescore)
    let scoretitle = document.getElementById("scoretitle")
    if (codingTree.score_duurzaamheid == "D") {scoretitle.style.color = "red"}
    if (codingTree.score_duurzaamheid == "C") {scoretitle.style.color = "orange"}
    if (codingTree.score_duurzaamheid == "B") {scoretitle.style.color = "yellow"}
    if (codingTree.score_duurzaamheid == "A") {scoretitle.style.color = "rgb(28, 200, 138)"}

    let energiebrnloc = codingTree.energiebronnen_LS
    let waterbrnloc = codingTree.waterbronnen_LS
    let broeikasloc = codingTree.broeikasgassen_LS
    let uitstootloc = codingTree.uitstoot_LS
    let milimpactloc = codingTree.milieu_impact_LS
    let gezonveilloc = codingTree.impact_GenV_LS
    let eisondloc = codingTree.verdere_eisen_LS
    let milbelloc = codingTree.milieu_beleid_LS
    let sdgnloc = codingTree.sdgn_LS

    let energiebrn = codingTree.GEBRUIK_VAN_ENERGIEBRONNEN > 0 ? `<p style="font-size: 15px;font-weight: bold;color: rgb(28, 200, 138);margin-bottom: 10px;">Aanwezig&nbsp;<span class="badge bg-primary" style="background: rgb(28, 200, 138) !important;">${codingTree.GEBRUIK_VAN_ENERGIEBRONNEN}</span>${getIcons(energiebrnloc)}</p>` : `<p style="font-size: 13px;font-weight: bold;color: rgb(203,12,0);margin-bottom: 10px;">Afwezig&nbsp;</p>`;
    let waterbrn = codingTree.GEBRUIK_VAN_WATERBRONNEN > 0 ? `<p style="font-size: 15px;font-weight: bold;color: rgb(28, 200, 138);margin-bottom: 10px;">Aanwezig&nbsp;<span class="badge bg-primary" style="background: rgb(28, 200, 138) !important;">${codingTree.GEBRUIK_VAN_WATERBRONNEN}</span>${getIcons(waterbrnloc)}</p>` : `<p style="font-size: 13px;font-weight: bold;color: rgb(203,12,0);margin-bottom: 10px;">Afwezig&nbsp;</p>`;
    let broeikas = codingTree.EMISSIES_VAN_BROEIKASGASSEN > 0 ? `<p style="font-size: 15px;font-weight: bold;color: rgb(28, 200, 138);margin-bottom: 10px;">Aanwezig&nbsp;<span class="badge bg-primary" style="background: rgb(28, 200, 138) !important;">${codingTree.EMISSIES_VAN_BROEIKASGASSEN}</span>${getIcons(broeikasloc)}</p>` : `<p style="font-size: 13px;font-weight: bold;color: rgb(203,12,0);margin-bottom: 10px;">Afwezig&nbsp;</p>`;
    let uitstoot = codingTree.VERVUILENDE_UITSTOOT > 0 ? `<p style="font-size: 15px;font-weight: bold;color: rgb(28, 200, 138);margin-bottom: 10px;">Aanwezig&nbsp;<span class="badge bg-primary" style="background: rgb(28, 200, 138) !important;">${codingTree.VERVUILENDE_UITSTOOT}</span>${getIcons(uitstootloc)}</p>` : `<p style="font-size: 13px;font-weight: bold;color: rgb(203,12,0);margin-bottom: 10px;">Afwezig&nbsp;</p>`;
    let milimpact = codingTree.MILIEU_IMPACT > 0 ? `<p style="font-size: 15px;font-weight: bold;color: rgb(28, 200, 138);margin-bottom: 10px;">Aanwezig&nbsp;<span class="badge bg-primary" style="background: rgb(28, 200, 138) !important;">${codingTree.MILIEU_IMPACT}</span>${getIcons(milimpactloc)}</p>` : `<p style="font-size: 13px;font-weight: bold;color: rgb(203,12,0);margin-bottom: 10px;">Afwezig&nbsp;</p>`;
    let gezonveil = codingTree.IMPACT_OP_GEZONDHEID_EN_VEILIGHEID > 0 ? `<p style="font-size: 15px;font-weight: bold;color: rgb(28, 200, 138);margin-bottom: 10px;">Aanwezig&nbsp;<span class="badge bg-primary" style="background: rgb(28, 200, 138) !important;">${codingTree.IMPACT_OP_GEZONDHEID_EN_VEILIGHEID}</span>${getIcons(gezonveilloc)}</p>` : `<p style="font-size: 13px;font-weight: bold;color: rgb(203,12,0);margin-bottom: 10px;">Afwezig&nbsp;</p>`;
    let eisond = codingTree.VERDERE_EISEN_OVER_BEPAALDE_ONDERWERPEN > 0 ? `<p style="font-size: 15px;font-weight: bold;color: rgb(28, 200, 138);margin-bottom: 10px;">Aanwezig&nbsp;<span class="badge bg-primary" style="background: rgb(28, 200, 138) !important;">${codingTree.VERDERE_EISEN_OVER_BEPAALDE_ONDERWERPEN}</span>${getIcons(eisondloc)}</p>` : `<p style="font-size: 13px;font-weight: bold;color: rgb(203,12,0);margin-bottom: 10px;">Afwezig&nbsp;</p>`;
    let milbel = codingTree.MILIEU_BELEID > 0 ? `<p style="font-size: 15px;font-weight: bold;color: rgb(28, 200, 138);margin-bottom: 10px;">Aanwezig&nbsp;<span class="badge bg-primary" style="background: rgb(28, 200, 138) !important;">${codingTree.MILIEU_BELEID}</span>${getIcons(milbelloc)}</p>` : `<p style="font-size: 13px;font-weight: bold;color: rgb(203,12,0);margin-bottom: 10px;">Afwezig&nbsp;</p>`;
    let sdgn = codingTree.SDG_N > 0 ? `<p style="font-size: 15px;font-weight: bold;color: rgb(28, 200, 138);margin-bottom: 10px;">Aanwezig&nbsp;<span class="badge bg-primary" style="background: rgb(28, 200, 138) !important;">${codingTree.SDG_N}</span>${getIcons(sdgnloc)}</p>` : `<p style="font-size: 13px;font-weight: bold;color: rgb(203,12,0);margin-bottom: 10px;">Afwezig&nbsp;</p>`;



    let nkrow = document.getElementById("nkrow")

    nkrow.insertAdjacentHTML("beforeend", `
    <div class="col">
                                            <h3 class="small fw-bold">Gebruik van energiebronnen</h4>
                                            ${energiebrn}
                                            <h3 class="small fw-bold">Gebruik van waterbronnen</h4>
                                            ${waterbrn}
                                            <h3 class="small fw-bold">Emissie van broeikasgassen</h4>
                                            ${broeikas}
                                            <h3 class="small fw-bold">Vervuilende uitstoot</h4>
                                            ${uitstoot}
                                            <h3 class="small fw-bold">Milieu-impact</h4>
                                            ${milimpact}
                                        </div>
    <div class="col">
                                        <h3 class="small fw-bold">Impact op gezondheid en veiligheid</h4>
                                        ${gezonveil}
                                        <h3 class="small fw-bold">Verdere eisen over bepaalde onderwerpen</h4>
                                        ${eisond}
                                        <h3 class="small fw-bold">Milieu beleid</h4>
                                        ${milbel}
                                        <h3 class="small fw-bold">SDGs</h4>
                                        ${sdgn}
                                    </div>
    `)

    let gendergloc = codingTree.gendergelijkheid_LS
    let impwerkloc = codingTree.iw_LS
    let socrelloc = codingTree.sociale_relaties_LS 
    let werkgelloc = codingTree.werkgelegenheid_LS
    let orgopwloc = codingTree.organisatie_werk_LS 
    let gezondheidenvloc = codingTree.gv_LS 
    let opleidingsbelloc = codingTree.opleidingsbeleid_LS 
    let sdghloc = codingTree.sdgh_LS 

    let genderg = codingTree.GENDERGELIJKHEID > 0 ? `<p style="font-size: 15px;font-weight: bold;color: rgb(28, 200, 138);margin-bottom: 10px;">Aanwezig&nbsp;<span class="badge bg-primary" style="background: rgb(28, 200, 138) !important;">${codingTree.GENDERGELIJKHEID}</span>${getIcons(gendergloc)}</p>` : `<p style="font-size: 13px;font-weight: bold;color: rgb(203,12,0);margin-bottom: 10px;">Afwezig&nbsp;</p>`;
    let impwerk = codingTree.IMPLEMENTATIE_WERKNEMERSRECHTEN > 0 ? `<p style="font-size: 15px;font-weight: bold;color: rgb(28, 200, 138);margin-bottom: 10px;">Aanwezig&nbsp;<span class="badge bg-primary" style="background: rgb(28, 200, 138) !important;">${codingTree.IMPLEMENTATIE_WERKNEMERSRECHTEN}</span>${getIcons(impwerkloc)}</p>` : `<p style="font-size: 13px;font-weight: bold;color: rgb(203,12,0);margin-bottom: 10px;">Afwezig&nbsp;</p>`;
    let socrel = codingTree.SOCIALE_RELATIES_OP_HET_WERK > 0 ? `<p style="font-size: 15px;font-weight: bold;color: rgb(28, 200, 138);margin-bottom: 10px;">Aanwezig&nbsp;<span class="badge bg-primary" style="background: rgb(28, 200, 138) !important;">${codingTree.SOCIALE_RELATIES_OP_HET_WERK}</span>${getIcons(socrelloc)}</p>` : `<p style="font-size: 13px;font-weight: bold;color: rgb(203,12,0);margin-bottom: 10px;">Afwezig&nbsp;</p>`;
    let werkgel = codingTree.WERKGELEGENHEID > 0 ? `<p style="font-size: 15px;font-weight: bold;color: rgb(28, 200, 138);margin-bottom: 10px;">Aanwezig&nbsp;<span class="badge bg-primary" style="background: rgb(28, 200, 138) !important;">${codingTree.WERKGELEGENHEID}</span>${getIcons(werkgelloc)}</p>` : `<p style="font-size: 13px;font-weight: bold;color: rgb(203,12,0);margin-bottom: 10px;">Afwezig&nbsp;</p>`;
    let orgopw = codingTree.ORGANISATIE_OP_HET_WERK > 0 ? `<p style="font-size: 15px;font-weight: bold;color: rgb(28, 200, 138);margin-bottom: 10px;">Aanwezig&nbsp;<span class="badge bg-primary" style="background: rgb(28, 200, 138) !important;">${codingTree.ORGANISATIE_OP_HET_WERK}</span>${getIcons(orgopwloc)}</p>` : `<p style="font-size: 13px;font-weight: bold;color: rgb(203,12,0);margin-bottom: 10px;">Afwezig&nbsp;</p>`;
    let gezondheidenv = codingTree.GEZONDHEID_EN_VEILIGHEID > 0 ? `<p style="font-size: 15px;font-weight: bold;color: rgb(28, 200, 138);margin-bottom: 10px;">Aanwezig&nbsp;<span class="badge bg-primary" style="background: rgb(28, 200, 138) !important;">${codingTree.GEZONDHEID_EN_VEILIGHEID}</span>${getIcons(gezondheidenvloc)}</p>` : `<p style="font-size: 13px;font-weight: bold;color: rgb(203,12,0);margin-bottom: 10px;">Afwezig&nbsp;</p>`;
    let opleidingsbel = codingTree.OPLEIDINGSBELEID > 0 ? `<p style="font-size: 15px;font-weight: bold;color: rgb(28, 200, 138);margin-bottom: 10px;">Aanwezig&nbsp;<span class="badge bg-primary" style="background: rgb(28, 200, 138) !important;">${codingTree.OPLEIDINGSBELEID}</span>${getIcons(opleidingsbelloc)}</p>` : `<p style="font-size: 13px;font-weight: bold;color: rgb(203,12,0);margin-bottom: 10px;">Afwezig&nbsp;</p>`;
    let sdgh = codingTree.SDG_H > 0 ? `<p style="font-size: 15px;font-weight: bold;color: rgb(28, 200, 138);margin-bottom: 10px;">Aanwezig&nbsp;<span class="badge bg-primary" style="background: rgb(28, 200, 138) !important;">${codingTree.SDG_H}</span>${getIcons(sdghloc)}</p>` : `<p style="font-size: 13px;font-weight: bold;color: rgb(203,12,0);margin-bottom: 10px;">Afwezig&nbsp;</p>`;


    hkrow.insertAdjacentHTML("beforeend", `
    <div class="col">
                                            <h3 class="small fw-bold">Gendergelijkheid</h4>
                                            ${genderg}
                                            <h3 class="small fw-bold">Implementatie van (inter)nationale werknemersrechten</h4>
                                            ${impwerk}
                                            <h3 class="small fw-bold">Sociale relaties op het werk</h4>
                                            ${socrel}
                                            <h3 class="small fw-bold">Werkgelegenheid</h4>
                                            ${werkgel}
                                        </div>
    <div class="col">
                                        <h3 class="small fw-bold">Organisatie op het werk</h4>
                                        ${orgopw}
                                        <h3 class="small fw-bold">Gezondheid en veiligheid</h4>
                                        ${gezondheidenv}
                                        <h3 class="small fw-bold">Opleidingsbeleid</h4>
                                        ${opleidingsbel}
                                        <h3 class="small fw-bold">SDG</h4>
                                        ${sdgh}
                                    </div>
    `)

    if (codingTree.score_zoektermen == 2 || codingTree.score_zoektermen == 0) {document.getElementById("zoektermwebsite").style.display = "none"}
    if (codingTree.score_duurzaamheid == 1 || codingTree.score_zoektermen == 0) {document.getElementById("zoektermpdf").style.display = "none"}
  })
}
/** Al de statische data (AantalWerknemers, OmzetCijfer, Balanstotaal, Framework, Businessmodel) op het dashboard zetten
 * Duurzaamheidsscore en gemiddelde op het dashboard zetten
 * :par_btw: het btw nummer van het bedrijf
  */
function getKMOdata(btw) {
  newbtw = btw.toLowerCase().replace("be", "")
  fetch(`http://www.vichogent.be:40021/kmodata/${newbtw}`)
  .then((data) => data.json())
  .then((data) => {
    const kmodata = data.kmodata[0]
    console.log(kmodata)
    document.getElementById("werknemers").innerHTML = `${kmodata.AantalWerknemers}`
    document.getElementById("omzet").innerHTML = `€ ${numberWithCommas(kmodata.OmzetCijfer)}`
    document.getElementById("balans").innerHTML = `€ ${numberWithCommas(kmodata.Balanstotaal)}`
    kmodata.Framework != null ? document.getElementById("framework").innerHTML = `Framework: <b>${kmodata.Framework}</b>` : "bababoey"

    let zoektermenpf = kmodata.ZoektermenPDF
    let zoektermenwebsite = kmodata.ZoektermenWebsite
    let avgpdf = kmodata.AvgPDF
    let avgwebsite = kmodata.AvgWebsite
    let pdfdom = document.getElementById("zoektermenpdf")
    let pdfavgdom = document.getElementById("avgpdf")
    let websitedom = document.getElementById("zoektermenwebsite")
    let websiteavgdom = document.getElementById("avgwebsite")
    if (zoektermenpf == 0 && zoektermenwebsite == 0) {
      pdfdom.innerHTML = zoektermenpf
      pdfavgdom.innerHTML = ``
      websitedom.innerHTML = zoektermenwebsite
      websiteavgdom.innerHTML = ``
    } else if (zoektermenpf == null || zoektermenwebsite == null) {
      pdfdom.innerHTML = "Geen info"
      websitedom.innerHTML = "Geen info"
      pdfavgdom.innerHTML = ""
      websiteavgdom.innerHTML = ""
    } else if (zoektermenpf == 0){
      pdfdom.innerHTML = zoektermenpf
      pdfavgdom.innerHTML = ``
      websitedom.innerHTML = zoektermenwebsite
      websiteavgdom.innerHTML = `Gemiddelde afstand: <b style="font-size:20px">${avgwebsite}</b>`
    } else if (zoektermenwebsite == 0) {
      pdfdom.innerHTML = zoektermenpf
      pdfavgdom.innerHTML = `Gemiddelde afstand: <b style="font-size:20px">${avgpdf}</b>`
      websitedom.innerHTML = zoektermenwebsite
      websiteavgdom.innerHTML = ``
    } else {
      pdfdom.innerHTML = zoektermenpf
      pdfavgdom.innerHTML = `Gemiddelde afstand: <b style="font-size:20px">${avgpdf}</b>`
      websitedom.innerHTML = zoektermenwebsite
      websiteavgdom.innerHTML = `Gemiddelde afstand: <b style="font-size:20px">${avgwebsite}</b>`
    }

  })
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
suggestOff();
checkAlert();
document.getElementById("alert").onclick = function() {removeAlert()};
  try{
    const vars = getUrlVars();
    if(vars.btw != undefined){
      document.getElementById("searchbar").value = vars.btw;
      zoek();
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
  getCodingTree(document.getElementById("searchbar").value);
  
}

window.onload = init;