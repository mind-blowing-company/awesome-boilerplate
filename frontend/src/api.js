import axios from "axios";
import querystring from "querystring";

const API = axios.create({
    baseURL: process.env.API_SERVER,
    timeout: 1000,
});

export const loginUser = (username, password) => {
    return API.post("/users/token", querystring.stringify({
        username,
        password
    }), {
        headers: {"Content-Type": "application/x-www-form-urlencoded"}
    }).then(response => {
        const token = response.data.access_token;
        const user = response.data.user;
        return {token, user};
    });
};

export default API;
