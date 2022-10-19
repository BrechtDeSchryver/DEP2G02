
const express = require("express");
const app = express();
const bodyParser = require("body-parser");
const db = require("./db/link");
const cors = require("cors");
app.use(cors());

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.get("/", (req, res) => {
  res.status(200).json({ status: "online" });
});

  app.get("/bedrijven/all", async (req, res) => {
  const bedrijven = await db.getAll();
  res.status(200).json({ bedrijven });
});



let port = 40007

/*https.createServer(options,app)*/app.listen(port, () => console.log(`server is running on port ${port}`));
