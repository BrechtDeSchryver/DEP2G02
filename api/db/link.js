const knex = require("./knex");


function getAll() {
  return knex("kmo").select("*");
}





module.exports = { getAll};
