// get the credentials from the .env file
const { DBUSER, DBPASSWD, DBHOST, DBPORT } = credentials.env;

const knex = require("knex");
connectedKnex = knex({
  client: "pg",
  connection: {
    host: DBHOST,
    port: parseInt(DBPORT),
    user: DBUSER,
    password: DBPASSWD,
    database: "DEP II",
  },
});

module.exports = connectedKnex;
