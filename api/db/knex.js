
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

module.exports = connectedKnex;
