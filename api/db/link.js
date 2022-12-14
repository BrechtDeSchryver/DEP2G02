const knex = require("./knex");
const crypto = require("crypto"),
  hash = crypto.getHashes();

/** Retourneert alle bedrijven */
function getAll() {
  return knex("kmo").select("*");
}

/** Retourneert een rij uit de tabel "KMO" waar "ondernemingsNummer" overeenkomt met het meegegeven ondernemingsnummer. */
function getKmoByOndernemingsnummer(ondernemingsnummer) {
  let result = knex("kmo")
    .select(
      "k.ondernemingsNummer",
      "k.name",
      "k.email",
      "k.telephone",
      "k.website",
      "k.nbbID",
      "k.nacebelCode",
      "k.score",
      "a.street",
      "a.zipcode",
      "m.name as city",
      "m.stedelijkheidsklasse",
      "ks.sector_ID as sector",
      "e.total as employees"

    )
    .from("kmo as k")
    .join("adress as a", "a.ondernemingsNummer", "k.ondernemingsNummer")
    .join("municipality as m", "m.zipcode", "a.zipcode")
    .join("kmo_sector as ks", "ks.ondernemingsNummer", "k.ondernemingsNummer")
    .join("employees as e", "e.ondernemingsNummer", "k.ondernemingsNummer")
    .where("k.ondernemingsNummer", "like", `${ondernemingsnummer}%`)
    .orderBy([{ column: "k.name", order: "asc" }])
    .limit(5);
  return result;
}

/** Retourneert een rij uit de tabel "KMO" waar "name" overeenkomt met de meegegeven naam. */
function getKmoNaam(name) {
  let realname = unescape(name);
  /*let result = knex("kmo")
    .select("*")
    .where("name", "like", `${realname.toUpperCase()}%`);
  result.limit(5);
  return result;*/
  //select k."ondernemingsNummer", k."name", k.email, k.telephone, k.website, k."nbbID", k."nacebelCode", k.score, a.street, a.zipcode, m."name" as 'city', m.stedelijkheidsklasse from kmo k join adress a ON a."ondernemingsNummer" = k."ondernemingsNummer" join municipality m ON m.zipcode = a.zipcode
  let result = knex("kmo")
    .select(
      "k.ondernemingsNummer",
      "k.name",
      "k.email",
      "k.telephone",
      "k.website",
      "k.nbbID",
      "k.nacebelCode",
      "k.score",
      "a.street",
      "a.zipcode",
      "m.name as city",
      "m.stedelijkheidsklasse",
      "ks.sector_ID as sector",
      "e.total as employees"
    )
    .from("kmo as k")
    .join("adress as a", "a.ondernemingsNummer", "k.ondernemingsNummer")
    .join("municipality as m", "m.zipcode", "a.zipcode")
    .join("kmo_sector as ks", "ks.ondernemingsNummer", "k.ondernemingsNummer")
    .join("employees as e", "e.ondernemingsNummer", "k.ondernemingsNummer")
    .where("k.name", "like", `${realname.toUpperCase()}%`)
    .orderBy([{ column: "k.name", order: "asc" }])
    .limit(5);
  return result;

}

/** Retourneert een rij uit de tabel "adress" waar "ondernemingsNummer" overeenkomt met het meegegeven ondernemingsnummer. */
function getAdressByNumber(ondernemingsnummer) {
  let result = knex("adress")
    .select("*")
    .where("ondernemingsNummer", "like", `%${ondernemingsnummer}%`)
    .orderBy([{ column: "ondernemingsNummer", order: "asc" }]);
  result.limit(5);
  return result;
}

/** Berekent de hashwaarde van de input string. */
function getHash(input_str) {
  hashPwd = crypto.createHash("sha256").update(input_str).digest("hex");
  return hashPwd;
}

/** Zoekt de combinatie username en gehasht password in de database  */
function getuser(username, password) {
  password = getHash(password);
  let result = knex("credentials")
    .select("passwordHash")
    .where("username", "like", `${username}`)
    .where("passwordHash", "like", `${password}`);
  result.limit(1);
  return result;
}

/** Zoekt een session token in de database en geeft deze terug. */
function checksession(password) {
  let result = knex("credentials")
    .select("passwordHash")
    .where("passwordHash", "like", `${password}`);
  result.limit(1);
  return result;
}

/** Zoekt alle durablility categories en geeft deze terug */
function getCategories() {
  let result = knex("durability_category").select("*");
  return result;
}


/** Zoekt alle subcategories en geeft deze terug */
function getSubCategories(category) {
  let result = knex("durability_term")
    .select("*")
    .where("durability_category", "like", `${category}`);
  return result;
}

/** Zoekt alle searchterms en geeft deze terug */
function getSearchTerms(subcategory) {
  let result = knex("durability_keyword")
    .select("*")
    .where("durability_term", "like", `${subcategory}`);
  return result;
}  

/** Verwijdert het zoekwoord met de meegegeven id uit de databank */
function deleteSearchTerm(id) {
  let result = knex("durability_keyword")
    .where("ID", id)
    .del();
  return result;
}

/** Geeft een meegegeven keyword van de meegegeven subcategory terug */
function getSearchTerm(word, subcategory) {
  let result = knex("durability_keyword")
    .select("*")
    .where("name", word)
    .where("durability_term", subcategory);
  return result;
}

/** Voegt een meegegeven zoekterm toe aan een de meegegeven subcategory */
function addSearchTerm(word, subcategory) {
  let result = knex("durability_keyword")
    .insert({ name: word, durability_term: subcategory })
    .returning("ID");
  return result;
}

/** Retourneert de lokale tijd */
function getLocalTime(localTime) {
  return localTime.getHours() + ":" + localTime.getMinutes() + ":" + localTime.getSeconds();
}

/** Reourneert alle sectoren gesorteerd volgens de meegegeven sorteer volgorde */
function getSectors(sorting) {
  // select s."name", count(s."name"), s.nacebelcode from kmo k join kmo_sector ks on ks."ondernemingsNummer" = k."ondernemingsNummer" join sector s on s."name" = ks."sector_ID" group by s."name" order by 2 desc
  let result = knex("kmo_sector")
    .select("sector_ID", "nacebelcode")
    .join("sector", "sector.name", "=", "kmo_sector.sector_ID")
    .count("sector_ID")
    .groupBy("nacebelcode", "sector_ID")
    .orderBy("count", sorting)
    .orderBy("sector_ID", "asc");
  return result;
  
}

/** Zoekt een sector en geeft deze terug */
function getSector(nacebelcode, sortingkey, sorting) {
  // select * from finance join kmo ON kmo."ondernemingsNummer" = finance."ondernemingsNummer" where kmo."nacebelCode" = '45113'
  let result = knex("kmo")
    .select("*")
    .join("finance", "finance.ondernemingsNummer", "=", "kmo.ondernemingsNummer")
    .join("employees", "employees.ondernemingsNummer", "=", "kmo.ondernemingsNummer")
    .where("kmo.nacebelCode", nacebelcode)
    .orderBy(sortingkey, sorting);
  return result;
}

function getSectorName(nacebelcode) {
  let result = knex("sector")
    .select("*")
    .where("nacebelcode", nacebelcode);
  return result;
}

function getAverageScoreFromSector(nacebelcode) {
  // select avg(kmo.score) as "Gemiddelde", kmo."nacebelCode", s.subdomain from subdomain_score s join kmo ON kmo."ondernemingsNummer" = s."ondernemingsNummer" where kmo."nacebelCode" = '47112'group by kmo."nacebelCode", s.subdomain
  let result = knex("subdomain_score")
    .select("subdomain")
    .join("kmo", "kmo.ondernemingsNummer", "=", "subdomain_score.ondernemingsNummer")
    .avg("kmo.score")
    .where("kmo.nacebelCode", nacebelcode)
    .groupBy("kmo.nacebelCode", "subdomain");
  return result;
}

module.exports = {
  getAll,
  getKmoByOndernemingsnummer,
  getKmoNaam,
  getAdressByNumber,
  getHash,
  getuser,
  checksession,
  getCategories,
  getSubCategories,
  getSearchTerms,
  deleteSearchTerm,
  getSearchTerm,
  addSearchTerm,
  getLocalTime,
  getSectors,
  getSector,
  getSectorName,
  getAverageScoreFromSector

};
