const axios = require("axios").default;

const baseURL = `${process.env.API_HOST}:${process.env.API_PORT}`;

const API = axios.create({
    baseURL,
    timeout: 3000,
});

module.exports = {
    default: API,
};
