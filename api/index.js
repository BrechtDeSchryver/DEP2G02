const express = require("express");
const app = express();
const bodyParser = require("body-parser");
const db = require("./db/link");
const cors = require("cors");
const crypto = require("crypto"),
  hash = crypto.getHashes();



app.use(cors());

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

/** Status pagina die op de homepage van de service draait. */
app.get("/", (req, res) => {
  res.status(200).json({ status: "online" });
});

/** Vraagt alle kmo's op */
/*  app.get("/bedrijven/all", async (req, res) => {
  const bedrijven = await db.getAll();
  res.status(200).json({ bedrijven });
});*/

/** Geeft een KMO terug in json formaat na het ontvangen van een btw nummer. */
app.get("/bedrijf/btw/:nummer", async (req, res) => {
  let kmo = await db.getKmoByOndernemingsnummer(req.params.nummer, req.body);
  kmo = kmo[0];
  let adress = await db.getAdressByNumber(req.params.nummer, req.body);
  delete adress[0].ondernemingsNummer;
  adress = adress[0];
  res.status(200).json({ kmo, adress });
});

/** Geeft een KMO terug in json formaat na het ontvangen van een naam. */
app.get("/bedrijf/naam/:naam", async (req, res) => {
  let bedrijf = await db.getKmoNaam(req.params.naam, req.body);
  kmo = bedrijf[0];
  console.log(kmo.ondernemingsNummer);
  let adress = await db.getAdressByNumber(kmo.ondernemingsNummer, req.body);
  adress = adress[0];
  // check if adress is undefined
  if (!adress === undefined) {
    delete adress.ondernemingsNummer;
  }
  res.status(200).json({ kmo, adress });
});

/** Geeft de hash waarde terug van de ontvangen waarde. */
app.get("/gethash/:waarde", async (req, res) => {
  let hash = db.getHash(req.params.waarde);
  res.status(200).json({ hash });
});

/** Checkt of de megegeven gebruikersnaam en het megegeven wachtwoord overeenkomt met die in de database en geeft een sessie terug als dit het geval is.  */
app.get("/getuser", async (req, res) => {
  let username = req.query.user;
  let password = req.query.pass;
  let user = await db.getuser(username, password);
  if (user.length == 1) {
  user = user[0];
  user = user.passwordHash
  res.status(200).json({ session : user });
  } else {
    res.status(200).json({ session : "false" });
  }
});

/** Checkt of de meegegeven sessie overeenkomt met de sessie in de database en geeft deze terug indien deze aanwezig is in de databank. */
app.get("/checksession", async (req, res) => {
  let password = req.query.pass;
  let session = await db.checksession(password);
  if (session.length == 1) {
  session = session[0];
  session = session.passwordHash
  res.status(200).json({ check : session });
  } else {
    res.status(200).json({ check : "false" });
  }
});


app.get("/categories", async (req, res) => {
  let all = await db.getCategories();
  let categories = [];
  all.forEach(element => { categories.push(element.name) });
  res.status(200).json({ categories });
});

app.get("/subcategories/:category", async (req, res) => {
  let all = await db.getSubCategories(req.params.category);
  let categories = [];
  all.forEach(element => { categories.push(element.name) });
  res.status(200).json({ categories });
});

app.get("/searchterms/:subcategory", async (req, res) => {
  let all = await db.getSearchTerms(req.params.subcategory);
  let searchterms = [];
  all.forEach(element => { searchterms.push(element.name) });
  res.status(200).json({ all });
});

app.get("/delete/searchterms", async (req, res) => {
  let session = await db.checksession(req.query.session);
  if (session.length == 1) {
  await db.deleteSearchTerm(req.query.id);
  res.status(200).json({ status : "deleted" });
  
  } else {
    res.status(200).json({ status : "denied" });
  }
});

app.get("/add/searchterms", async (req, res) => {
  let session = await db.checksession(req.query.session);
  if (session.length == 1) {
    let zoekterm = await db.getSearchTerm(req.query.term, req.query.subcategory);
    if (zoekterm.length == 0) {
      let id = await db.addSearchTerm(req.query.term, req.query.subcategory);
      console.log(id);
      res.status(200).json({ status : id[0] });
    } else {
      res.status(200).json({ status : "failed" });
    }
  } else {
    res.status(200).json({ status : "denied" });
  }
});

/** Geeft de jaarrekening, de website en eventueel een duurzaamheidsrapport terug in json formaat na het ontvangen van een btw nummer. */

/*
app.get("/bedrijf/rawdata/:nummer", async (req, res) => {
  let rawdata = await db.getRawDataByOndernemingsnummer(req.params.nummer, req.body);
  rawdata = rawdata[0];
  res.status(200).json({ rawdata });
});
*/

/**Bepaalt de poort waarop de API service draait. */
let port = 8080;

/**Start de API service. */

/*https.createServer(options,app)*/ app.listen(port, () =>
  console.log(`The API is running on http://localhost:${port}/`)
);
