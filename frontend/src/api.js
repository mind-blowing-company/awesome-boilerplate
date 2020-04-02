const axios = require("axios").default;
const querystring = require("querystring");

const API = axios.create({
    baseURL: process.env.API_SERVER,
    timeout: 1000,
});

const processUserResponse = (response, callback) => {
    const token = response.data.access_token;
    const user = response.data.user;
    callback(token, user);
};

const registerUser = (username, password, callback) => {
    return API.post("/users/register", {
        username,
        password
    }).then(response => processUserResponse(response, callback));
};

const loginUser = (username, password, callback) => {
    return API.post("/users/token", querystring.stringify({
        username,
        password
    }), {
        headers: {"Content-Type": "application/x-www-form-urlencoded"}
    }).then(response => processUserResponse(response, callback));
};

const updateUser = (email, password, token) => {
    return API.put("/users/update", {
        email,
        password: password || null
    }, {
        headers: {
            "Accept": "application/json",
            "Authorization": `Bearer ${token}`
        }
    });
};

const authenticateLinkedin = (token, email) => {
    return API.post("/users/auth/linkedin", {
        email,
        token
    });
};

module.exports = {
    loginUser,
    registerUser,
    updateUser,
    authenticateLinkedin,
    default: API
};
