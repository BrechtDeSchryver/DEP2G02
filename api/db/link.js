const knex = require("./knex");

/**Retourneert alle bedrijven */
function getAll() {
  return knex("kmo").select("*");
}

/**Retourneert een rij uit de tabel "KMO" waar "ondernemingsNummer" overeenkomt met het meegegeven ondernemingsnummer*/
function getKmoByOndernemingsnummer(ondernemingsnummer) {
  return knex("kmo")
    .select("*")
    .where("ondernemingsNummer", "like", `%${ondernemingsnummer}%`)
    .orderBy([{ column: "ondernemingsNummer", order: "asc" }]);
}

/**Retourneert een rij uit de tabel "KMO" waar "name" overeenkomt met de meegegeven naam*/
function getKmoNaam(name) {
  let realname = unescape(name)
  console.log(realname)
  let result = knex("kmo")
    .select("*")
    .where('name', 'like', `%${realname.toUpperCase()}%`)
  result.limit(5)
  return result;
}

/**Retourneert een rij uit de tabel "adress" waar "ondernemingsNummer" overeenkomt met het meegegeven ondernemingsnummer*/
function getAdressByNumber(ondernemingsnummer) {
  let result = knex("adress")
    .select("*")
    .where('ondernemingsNummer', 'like', `%${ondernemingsnummer}%`)
    .orderBy([{ column: "ondernemingsNummer", order: "asc" }]);
  result.limit(5)
  return result;
}

module.exports = { getAll, getKmoByOndernemingsnummer, getKmoNaam, getAdressByNumber };
