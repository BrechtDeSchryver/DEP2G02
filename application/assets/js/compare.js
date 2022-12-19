let btwnums = "046565"

function insertBedrijf() {
    let content = document.getElementById("kmorow");
    content.innerHTML = "";
    let btwlist = getcompareitems();
    btwlist.forEach(btw => {

        fetch(`http://localhost:8080/bedrijf/btw/${btw}`)
    .then((res) => res.json())
    .then((data) => {
        data.bedrijven.forEach(bedrijf => {
            content.insertAdjacentHTML("beforeend", `
        <div class="col">
    <div class="card">
        <div class="card-header">
            <ul class="nav nav-tabs card-header-tabs">
                <li class="nav-item"><a class="nav-link active" href="#" style="color: rgb(89,182,195) !important;">Algemeen</a></li>
                <li class="nav-item"><a class="nav-link" href="#" style="color: rgb(89,182,195) !important;" onclick="getgegevens()">Gegevens</a></li>
                <li class="nav-item"><a class="nav-link" href="#" style="color: rgb(89,182,195) !important;" onclick="getscores()">Scores</a></li>
            </ul>
        </div>
        <div class="card-body">
            <h5 id="name" style="color: rgb(58,59,69);font-weight: bold;margin-bottom: 5px;">${bedrijf.name}</h5>
            <p id="btw" style="font-size: 13px;margin-bottom: 5px;">${bedrijf.ondernemingsNummer}</p>
            <p style="font-size: 15px;"><b>Score:</b> ${bedrijf.score == null ? "geen score" : parseFloat(bedrijf.score).toFixed(5).replace(".", ",") + "%"}</p>
        </div>
    </div>
</div>

                            `)
        });



        ;})

    });
    

}

function getgegevens() {
    let content = document.getElementById("kmorow");
    content.innerHTML = "";
    let btwlist = getcompareitems();
    btwlist.forEach(btw => {

        fetch(`http://localhost:8080/bedrijf/btw/${btw}`)
    .then((res) => res.json())
    .then((data) => {
        data.bedrijven.forEach(bedrijf => {
            let websiteurl = bedrijf.website;
            if (!websiteurl.toLowerCase().startsWith("https") && !websiteurl.toLowerCase().startsWith("http")) {
                websiteurl = `https://${websiteurl}`
              } else if (websiteurl.toLowerCase().startsWith("https") || websiteurl.toLowerCase().startsWith("http")) {
                websiteurl = websiteurl;
              }
            website = `<a href="${websiteurl}" style="margin-right: 10px;"><i class="fas fa-globe-europe" style="color: rgb(89,182,195);font-size: 20px;" title="Website"></i></a>`;
            let pdf = `<a href="https://consult.cbso.nbb.be/api/external/broker/public/deposits/pdf/${bedrijf.nbbID}" style="margin-left: 0px;margin-right: 10px;"><i class="far fa-file-pdf" style="color: rgb(89,182,195);font-size: 20px;" title="Jaarrekening"></i></a>`;
            content.insertAdjacentHTML("beforeend", `
        <div class="col">
    <div class="card">
        <div class="card-header">
            <ul class="nav nav-tabs card-header-tabs">
                <li class="nav-item"><a class="nav-link" href="#" style="color: rgb(89,182,195) !important;" onclick="insertBedrijf()">Algemeen</a></li>
                <li class="nav-item"><a class="nav-link active" href="#" style="color: rgb(89,182,195) !important;">Gegevens</a></li>
                <li class="nav-item"><a class="nav-link" href="#" style="color: rgb(89,182,195) !important;" onclick="getscores()">Scores</a></li>
            </ul>
        </div>
        <div class="card-body">
            <h5 id="name" style="color: rgb(58,59,69);font-weight: bold;margin-bottom: 5px;">${bedrijf.name}</h5>
            <p style="font-size: 13px;">${bedrijf.ondernemingsNummer}</p>
            <h6 style="color: rgb(58,59,69);font-weight: bold;margin-bottom: 5px;">Adres:</h6>
            <p style="font-size: 16px; margin-bottom:3px;">${bedrijf.street.replace("Ã«", "ë")}</p>
            <p style="font-size: 16px;">${bedrijf.zipcode + " " + bedrijf.city}</p>
            <div>${pdf + website}</div>
        </div>
    </div>
</div>
                            `)
        });
        




        ;})

    })

}

function getscores() {
    let content = document.getElementById("kmorow");
    //content.innerHTML = "";
    let btwlist = getcompareitems();
    content.innerHTML = "";
    let counter = 0;
    btwlist.forEach(btw => {
        fetch(`http://localhost:8080/bedrijf/scores/${btw}`)
    .then((res) => res.json())
    .then((data) => {
        console.log(data);


        content.insertAdjacentHTML("beforeend", `
        <div class="col">
    <div class="card">
        <div class="card-header">
            <ul class="nav nav-tabs card-header-tabs">
                <li class="nav-item"><a class="nav-link" href="#" style="color: rgb(89,182,195) !important;" onclick="insertBedrijf('${getcompareitems()}')">Algemeen</a></li>
                <li class="nav-item"><a class="nav-link " href="#" style="color: rgb(89,182,195) !important;" onclick="getgegevens()">Gegevens</a></li>
                <li class="nav-item"><a class="nav-link active" href="#" style="color: rgb(89,182,195) !important;">Scores</a></li>
            </ul>
        </div>
        <div class="card-body">
            <h5 id="name" style="color: rgb(58,59,69);font-weight: bold;margin-bottom: 5px;">BTW: ${getcompareitems()[counter]}</h5>
            <div>
    <canvas id="${btw}"></canvas>
  </div>
        </div>
    </div>
</div>
                            `)




                            const ctx = document.getElementById(btw);

                            let subdomains = [];
                            let scores = [];
                            let color = [];
                                data.scores.forEach(subdomain => {
                                    subdomains.push(subdomain.subdomain);
                                    scores.push(subdomain.score);
                                });
                                let graphscores = [];
                                let colors = [];
                                subdomains.forEach(score => {
                                    if (score < 0) {
                                        colors.push('rgba(255, 99, 132, 0.7)');
                                    } else {
                                        colors.push('rgba(75, 192, 192, 0.7)');
                                    }
                                });

                                subdomains = [...new Set(subdomains)];
                    
                                new Chart(ctx, {
                          type: 'bar',
                          data: {
                            labels: subdomains,
                            datasets: [{
                              label: 'Scores',
                              data: scores,
                              backgroundColor: colors,
                              borderWidth: 1
                            }]
                          },
                          options: {
                            scales: {
                              y: {
                                beginAtZero: true
                              }
                            }
                          }
                        });

        counter++;

    })

    })
}


function getcompareitems(){
    let compare = localStorage.getItem("compare");
    let comparearray = compare.split(",");
    if (comparearray.length < 2 || compare == null || compare == ""){
        history.back();
    } else{
        return comparearray.sort();
    }
}


function init(){
    insertBedrijf();

}

window.onload = init;