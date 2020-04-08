const axios = require("axios").default;

const API = axios.create({
    baseURL: process.env.API_SERVER,
    timeout: 3000,
});

module.exports = {
    default: API,

};
