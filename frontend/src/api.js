import axios from "axios";
import querystring from "querystring";

const API = axios.create({
    baseURL: process.env.API_SERVER,
    timeout: 1000,
});

const processUserResponse = (response, callback) => {
    const token = response.data.access_token;
    const user = response.data.user;
    callback(token, user);
};

export const registerUser = (username, password, callback) => {
    return API.post("/users/register", {
        username,
        password
    }).then(response => processUserResponse(response, callback));
};

export const loginUser = (username, password, callback) => {
    return API.post("/users/token", querystring.stringify({
        username,
        password
    }), {
        headers: {"Content-Type": "application/x-www-form-urlencoded"}
    }).then(response => processUserResponse(response, callback));
};
