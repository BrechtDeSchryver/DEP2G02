
const express = require("express");
const app = express();
const bodyParser = require("body-parser");
const db = require("./db/link");
const cors = require("cors");
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
  console.log(kmo.ondernemingsNummer)
  let adress = await db.getAdressByNumber(kmo.ondernemingsNummer, req.body);
  adress = adress[0];
  delete adress.ondernemingsNummer;
  res.status(200).json({ kmo, adress });
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
let port = 40007

/**Start de API service. */
/*https.createServer(options,app)*/app.listen(port, () => console.log(`The API is running on port ${port}`));
