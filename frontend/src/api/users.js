const querystring = require("querystring");

const API = require("./index").default;

const processUserResponse = (response, callback) => {
    const token = response.data.access_token;
    callback(token);
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

const updateUser = (user, token) => {
    return API.put("/users/update", {
        username: user.username,
        password: user.password,
        email: user.email
    }, {
        headers: {
            "Accept": "application/json",
            "Authorization": `Bearer ${JSON.parse(token)}`
        }
    });
};

const getCurrentUser = (token) => {
    return API.get("/users/me", {
        headers: {
            "Authorization": `Bearer ${JSON.parse(token)}`
        }
    });
};

const authenticateLinkedin = (token, email=null) => {
    return API.post("/users/auth/linkedin", {
        token,
        email
    });
};

const authenticateGoogle = (token, email=null) => {
    return API.post("/users/auth/google", {
        token,
        email
    });
};

const authenticateFacebook = (token, email = null) => {
    return API.post("/users/auth/facebook", {
        token,
        email
    });
};

module.exports = {
    loginUser,
    registerUser,
    updateUser,
    getCurrentUser,
    authenticateLinkedin,
    authenticateGoogle,
    authenticateFacebook,
};
