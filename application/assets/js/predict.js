

function inputlistner() {
    let omzet = document.getElementById("omzet");
    let personeel = document.getElementById("personeel");
    let postcode = document.getElementById("postcode");
    let sector = document.getElementById("nacebel");
    let jaarrekeningval = false;
    let beursval = false;
    let websiteval = false;

        document.getElementById("jaarrekening").addEventListener("click", function () {
            jaarrekeningval = !jaarrekeningval;
            console.log([omzetval, personeelval, postcodeval, sectorval, jaarrekeningval, beursval, websiteval]);
        });
        document.getElementById("beurs").addEventListener("click", function () {
            beursval =!beursval;
            console.log([omzetval, personeelval, postcodeval, sectorval, jaarrekeningval, beursval, websiteval]);
        });
        document.getElementById("website").addEventListener("click", function () {
            websiteval =!websiteval;
            console.log([omzetval, personeelval, postcodeval, sectorval, jaarrekeningval, beursval, websiteval]);
        });


        let omzetval;
        let personeelval;
        let postcodeval = 0;
        let sectorval;

        omzet.addEventListener("keyup", function () {
            omzetval = this.value;
            console.log([omzetval, personeelval, postcodeval, sectorval, jaarrekeningval, beursval, websiteval]);
            checksubmit();
        });
        personeel.addEventListener("keyup", function () {
            personeelval = this.value;
            console.log([omzetval, personeelval, postcodeval, sectorval, jaarrekeningval, beursval, websiteval]);
            checksubmit();
        });
        postcode.addEventListener("keyup", function () {
            postcodeval = this.value;
            console.log(postcodeval.length);
            console.log([omzetval, personeelval, postcodeval, sectorval, jaarrekeningval, beursval, websiteval]);
            checksubmit();
        });
        sector.addEventListener("keyup", function () {
            sectorval = this.value;
            console.log([omzetval, personeelval, postcodeval, sectorval, jaarrekeningval, beursval, websiteval]);
            checksubmit();
        });

        function checksubmit() {
            if (omzetval && personeelval && postcodeval.length == 4 && sectorval) {
                document.getElementById("submitbtn").disabled = false;
                document.getElementById("submitbtn").onclick = function () {
                    document.getElementById("loadingscreen").style.display = "block";
                    doc
                   predict([omzetval, personeelval, postcodeval, sectorval, jaarrekeningval, beursval, websiteval]);
                }
            } else {
                document.getElementById("submitbtn").disabled = true;
                document.getElementById("submitbtn").onclick = null;
                document.getElementById("loadingscreen").style.display = "none";
            }
        }



}

function predict(array) {
    let button = document.getElementById("submitbtn");
    let loadingscreen = document.getElementById("loadingscreen");
    let result = document.getElementById("result");
    let score = document.getElementById("score");
    button.innerHTML = "Predicting...";
    button.disabled = true;
    fetch(`http://vichogent.be:40046/api/predict/Omzet=${array[0]}&personeel=${array[1]}&postcode=${array[2]}&sector=${array[3]}&jr=${array[4]}&beurs=${array[5]}&website=${array[6]}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            button.innerHTML = "Predict";
            button.disabled = false;
            loadingscreen.style.display = "none";
            score.innerHTML = data.score;
            result.style.display = "block";

        })
}




function init() {
    inputlistner();
    document.getElementById("submitbtn").disabled = true;
    document.getElementById("result").style.display = "none";
}

window.onload = init;