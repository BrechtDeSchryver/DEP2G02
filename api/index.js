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
  console.log(`[${new Date().toLocaleString()}] - ${req.socket.remoteAddress} - Status`);
});

/** Vraagt alle kmo's op */
/*  app.get("/bedrijven/all", async (req, res) => {
  const bedrijven = await db.getAll();
  res.status(200).json({ bedrijven });
});*/

/** Geeft een KMO terug in json formaat na het ontvangen van een btw nummer. */
app.get("/bedrijf/btw/:nummer", async (req, res) => {
  let bedrijven = await db.getKmoByOndernemingsnummer(req.params.nummer, req.body);
  
  res.status(200).json({ bedrijven });
  console.log(`[${db.getLocalTime(new Date())}] ${req.socket.remoteAddress} heeft ${req.params.nummer} opgevraagd`);
});

/** Geeft een KMO terug in json formaat na het ontvangen van een naam. */
app.get("/bedrijf/naam/:naam", async (req, res) => {
  let bedrijven = await db.getKmoNaam(req.params.naam, req.body);
  console.log(bedrijven);
  /*
  kmo = bedrijf[0];
  let adress = await db.getAdressByNumber(kmo.ondernemingsNummer, req.body);
  adress = adress[0];
  // check if adress is undefined
  if (!adress === undefined) {
    delete adress.ondernemingsNummer;
  }*/
  res.status(200).json({ bedrijven });
  // get local time hh:mm:ss
  console.log(`[${db.getLocalTime(new Date())}] IP: ${req.socket.remoteAddress} | Naam: ${req.params.naam}`);
});

/** Geeft de hash waarde terug van de ontvangen waarde. */
app.get("/gethash/:waarde", async (req, res) => {
  let hash = db.getHash(req.params.waarde);
  res.status(200).json({ hash });
  console.log(`[${db.getLocalTime(new Date())}] Hash: ${hash} from ${req.socket.remoteAddress}`);
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
  console.log("[" + db.getLocalTime(new Date())+ "] " + "User logged in: " + username + " from ip: " + req.socket.remoteAddress);
  } else {
    res.status(200).json({ session : "false" });
    console.log("[" + db.getLocalTime(new Date())+ "] " + "User failed to log in: " + username + " from ip: " + req.socket.remoteAddress);
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
  console.log(`[${db.getLocalTime(new Date())}] Session ${session} from ${req.socket.remoteAddress} was checked successfully`);
  } else {
    res.status(200).json({ check : "false" });
    console.log(`[${db.getLocalTime(new Date())}] Session ${password} from ${req.socket.remoteAddress} was checked but not found in database`);
  }
});

/** Geeft alle categories weer */
app.get("/categories", async (req, res) => {
  let all = await db.getCategories();
  let categories = [];
  all.forEach(element => { categories.push(element.name) });
  res.status(200).json({ categories });
  console.log("["+ db.getLocalTime(new Date()) + "] " + "Returned categories to " + req.socket.remoteAddress);
});

/** Toont de subcategory met meegegeven naam */
app.get("/subcategories/:category", async (req, res) => {
  let all = await db.getSubCategories(req.params.category);
  let categories = [];
  all.forEach(element => { categories.push(element.name) });
  res.status(200).json({ categories });
  console.log(`[${db.getLocalTime(new Date())}] Returned subcategories of ${req.params.category} to ` + req.socket.remoteAddress);
});

/** Toont de subcategory met meegegeven naam */
app.get("/searchterms/:subcategory", async (req, res) => {
  let all = await db.getSearchTerms(req.params.subcategory);
  let searchterms = [];
  all.forEach(element => { searchterms.push(element.name) });
  res.status(200).json({ all });
  console.log(`[${db.getLocalTime(new Date())}] Returned searchterms of category ${req.params.subcategory} to ${req.socket.remoteAddress}` );
});

/** Verwijdert de searchterm van de subcategory die beide megegeven zijn */
app.get("/delete/searchterms", async (req, res) => {
  let session = await db.checksession(req.query.session);
  if (session.length == 1) {
  await db.deleteSearchTerm(req.query.id);
  res.status(200).json({ status : "deleted" });
  console.log(`[${db.getLocalTime(new Date())}] ${req.socket.remoteAddress} deleted term with id ${req.query.id}`);
  
  } else {
    res.status(200).json({ status : "denied" });
    console.log("[" + db.getLocalTime(new Date()) + "] " +"Denied delete request becourse of invalid session from " + req.socket.remoteAddress);
  }
});

/** Voegt de searchterm toe van de subcategory die beide megegeven zijn */
app.get("/add/searchterms", async (req, res) => {
  let session = await db.checksession(req.query.session);
  if (session.length == 1) {
    let zoekterm = await db.getSearchTerm(req.query.term, req.query.subcategory);
    if (zoekterm.length == 0) {
      let id = await db.addSearchTerm(req.query.term, req.query.subcategory);
      console.log(`[${db.getLocalTime(new Date())}] Added '${req.query.term}' to subcategory '${req.query.subcategory}'`);
      res.status(200).json({ status : id[0] });
    } else {
      res.status(200).json({ status : "failed" });
      console.log(`[${db.getLocalTime(new Date())}] ${req.socket.remoteAddress} tried to add ${req.query.term} but it was already in ${req.query.subcategory}`);
    }
  } else {
    res.status(200).json({ status : "denied" });
    console.log(`[${db.getLocalTime(new Date())}] ${req.socket.remoteAddress} tried to add a term but authentication failed`);	
  }
});

/** Geeft alle sectoren terug */
app.get("/sectors", async (req, res) => {
  let sorting = "desc";
  if (req.query.sorting == "asc") {
    sorting = "asc";}
  let sectors = await db.getSectors(sorting);
  res.status(200).json({ sectors });
  console.log("["+ db.getLocalTime(new Date()) + "] " + "Returned sectors to " + req.socket.remoteAddress);
});

/** Geeft een bepaalde sector terug */
app.get("/sector", async (req, res) => {
  let sortingkey = req.query.sortingkey == undefined ? "name" : req.query.sortingkey;
  let sorting = req.query.sorting == undefined ? "asc" : req.query.sorting;
  let bedrijven = await db.getSector(req.query.sector, sortingkey, sorting);
  let name = await db.getSectorName(req.query.sector);
  aantal = bedrijven.length;
  name = name[0].name;
  //rename the total key to aantal
  bedrijven = bedrijven.map(function (obj) {
    obj.personeel = obj.total;
    delete obj.total;
    return obj;
  });
  res.status(200).json({ "aantal":aantal,"naam":name,bedrijven });
  console.log("["+ db.getLocalTime(new Date()) + "] " + "Returned sectors to " + req.socket.remoteAddress);
});

/** Geef de gemiddelde score van een sector per subcategory */
app.get("/sector/average", async (req, res) => {
  let nacebelCode = req.query.sector;
  let subdomains = await db.getAverageScoreFromSector(nacebelCode);
  res.status(200).json({ subdomains });
  console.log("["+ db.getLocalTime(new Date()) + "] " + "Returned average scores of sector " + nacebelCode + " to " + req.socket.remoteAddress);
});

app.get("/bedrijf/scores/:nummer", async (req, res) => {
  let btw = req.params.nummer;
  let scores = await db.getScoreFromKmo(btw);
  res.status(200).json({ scores });
  console.log("["+ db.getLocalTime(new Date()) + "] " + "Returned scores of company " + btw + " to " + req.socket.remoteAddress);
  
});

app.get("/bedrijf/ranking/:nummer", async (req, res) => {
  let btw = req.params.nummer;
  let ranking = await db.getRanking(btw);
  ranking = ranking.rows[0];
  let total = await db.getTotalBedrijven();
  total = total[0].count
  res.status(200).json({ "rank" : ranking.positie, "total" : total });
  console.log("["+ db.getLocalTime(new Date()) + "] " + "Returned the rank of company " + btw + " to " + req.socket.remoteAddress);
  
});

app.get("/bedrijf/total", async (req, res) => {
  let total = await db.getTotalBedrijven();
  total = total[0].count
  console.log(total);
  res.status(200).json({ "total" : total });
  console.log("["+ db.getLocalTime(new Date()) + "] " + "Returned the number of companies to " + req.socket.remoteAddress);
  
});

app.get("/bedrijf/finance/:nummer", async (req, res) => {
  let total = await db.getFinnaceData(req.params.nummer);
  finance = total[0]
  res.status(200).json({ finance });
  console.log("["+ db.getLocalTime(new Date()) + "] " + "Returned the number of companies to " + req.socket.remoteAddress);
});

app.get("/heatmap/coords", async (req, res) => {
  let coords = await db.getLongLat();
  coords = coords.rows;
  res.status(200).json({ coords });
  console.log("["+ db.getLocalTime(new Date()) + "] " + "Returned the number of companies to " + req.socket.remoteAddress);
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
