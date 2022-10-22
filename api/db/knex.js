
/**Maakt de connectie met de databank door middel van knex */
const knex = require("knex");
connectedKnex = knex({
  client: "pg",
  connection: {
    host: "vichogent.be",
    port: 40035,
    user: "pyuser",
    password: "dikkeberta",
    database: "dep",
  },
});

/**Exporteert de connectie */
module.exports = connectedKnex;
