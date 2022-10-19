const knex = require("./knex");


function getAll() {
  return knex("bedrijven").select("*");
}





module.exports = { getAll};
