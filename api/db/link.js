const knex = require("./knex");
const crypto = require("crypto"),
  hash = crypto.getHashes();

/** Retourneert alle bedrijven */
function getAll() {
  return knex("kmo").select("*");
}

/** Retourneert een rij uit de tabel "KMO" waar "ondernemingsNummer" overeenkomt met het meegegeven ondernemingsnummer. */
function getKmoByOndernemingsnummer(ondernemingsnummer) {
  return knex("kmo")
    .select("*")
    .where("ondernemingsNummer", "like", `%${ondernemingsnummer}%`)
    .orderBy([{ column: "ondernemingsNummer", order: "asc" }]);
}

/** Retourneert een rij uit de tabel "KMO" waar "name" overeenkomt met de meegegeven naam. */
function getKmoNaam(name) {
  let realname = unescape(name);
  let result = knex("kmo")
    .select("*")
    .where("name", "like", `%${realname.toUpperCase()}%`);
  result.limit(5);
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

function getCategories() {
  let result = knex("durability_category").select("*");
  return result;
}

function getSubCategories(category) {
  let result = knex("durability_term")
    .select("*")
    .where("durability_category", "like", `${category}`);
  return result;
}

function getSearchTerms(subcategory) {
  let result = knex("durability_keyword")
    .select("*")
    .where("durability_term", "like", `${subcategory}`);
  return result;
}  

function deleteSearchTerm(id) {
  let result = knex("durability_keyword")
    .where("ID", id)
    .del();
  return result;
}

function getSearchTerm(word, subcategory) {
  let result = knex("durability_keyword")
    .select("*")
    .where("name", word)
    .where("durability_term", subcategory);
  return result;
}

function addSearchTerm(word, subcategory) {
  let result = knex("durability_keyword")
    .insert({ name: word, durability_term: subcategory })
    .returning("ID");
  return result;
}

function getLocalTime(localTime) {
  return localTime.getHours() + ":" + localTime.getMinutes() + ":" + localTime.getSeconds();
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
};
