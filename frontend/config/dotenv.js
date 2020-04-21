const path = require("path");
const env = require("dotenv").config({
    path: path.join(__dirname, "..", ".env")
});

exports.default = env;
