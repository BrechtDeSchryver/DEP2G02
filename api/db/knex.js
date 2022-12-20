// neem de getPassword functie uit het credentials.js module
const { getPassword } = require("./credentials");
// neem de getUsername functie uit het credentials.js module
const { getUsername } = require("./credentials");

/**Maakt de connectie met de databank door middel van knex */
const knex = require("knex");
connectedKnex = knex({
  client: "postgres",
  connection: {
    host: "vichogent.be",
    port: 40035,
    user: getUsername(),
    password: getPassword(),
    database: "dep",
  },
});

/**Exporteert de connectie */
module.exports = connectedKnex;
