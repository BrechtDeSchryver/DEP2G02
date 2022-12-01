let btwnums = "046565"

function insertBedrijf() {
    let content = document.getElementById("kmorow");
    content.innerHTML = "";
    let btwlist = getcompareitems();
    btwlist.forEach(btw => {

        fetch(`http://localhost:8080/bedrijf/btw/${btw}`)
    .then((res) => res.json())
    .then((data) => {
        console.log(data);
        data.bedrijven.forEach(bedrijf => {
            content.insertAdjacentHTML("beforeend", `
        <div class="col">
    <div class="card">
        <div class="card-header">
            <ul class="nav nav-tabs card-header-tabs">
                <li class="nav-item"><a class="nav-link active" href="#" style="color: rgb(89,182,195) !important;">Algemeen</a></li>
                <li class="nav-item"><a class="nav-link" href="#" style="color: rgb(89,182,195) !important;" onclick="getgegevens()">Gegevens</a></li>
                <li class="nav-item"><a class="nav-link" href="#" style="color: rgb(89,182,195) !important;">Scores</a></li>
            </ul>
        </div>
        <div class="card-body">
            <h5 id="name" style="color: rgb(58,59,69);font-weight: bold;margin-bottom: 5px;">${bedrijf.name}</h5>
            <p id="btw" style="font-size: 13px;">${bedrijf.ondernemingsNummer}</p>
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
        console.log(data);
        data.bedrijven.forEach(bedrijf => {
            let website = `<a href="${bedrijf.website}" style="margin-right: 10px;"><i class="fas fa-globe-europe" style="color: rgb(89,182,195);font-size: 20px;" title="Website"></i></a>`;
            let pdf = `<a href="https://consult.cbso.nbb.be/api/external/broker/public/deposits/pdf/${bedrijf.nbbID}" style="margin-left: 0px;margin-right: 10px;"><i class="far fa-file-pdf" style="color: rgb(89,182,195);font-size: 20px;" title="Jaarrekening"></i></a>`;
            content.insertAdjacentHTML("beforeend", `
        <div class="col">
    <div class="card">
        <div class="card-header">
            <ul class="nav nav-tabs card-header-tabs">
                <li class="nav-item"><a class="nav-link" href="#" style="color: rgb(89,182,195) !important;" onclick="insertBedrijf('${getcompareitems()}')">Algemeen</a></li>
                <li class="nav-item"><a class="nav-link active" href="#" style="color: rgb(89,182,195) !important;">Gegevens</a></li>
                <li class="nav-item"><a class="nav-link" href="#" style="color: rgb(89,182,195) !important;">Scores</a></li>
            </ul>
        </div>
        <div class="card-body">
            <h5 id="name" style="color: rgb(58,59,69);font-weight: bold;margin-bottom: 5px;">${bedrijf.name}</h5>
            <p style="font-size: 13px;">${bedrijf.ondernemingsNummer}</p>
            <h6 style="color: rgb(58,59,69);font-weight: bold;margin-bottom: 5px;">Adres:</h6>
            <p style="font-size: 16px; margin-bottom:3px;">${bedrijf.street}</p>
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


function getcompareitems(){
    let compare = localStorage.getItem("compare");
    let comparearray = compare.split(",");
    console.log(comparearray);
    if (comparearray.length < 2 || compare == null || compare == ""){
        history.back();
    } else{
        return comparearray;
    }
}


function init(){
    insertBedrijf();

}

window.onload = init;