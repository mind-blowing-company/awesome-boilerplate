const express = require("express");

const router = express.Router();
const passport = require("../passport").default;
const usersApi = require("../api/users");

// Save user and it's JWT to cookies and then redirect.
const setSessionCookies = (apiData, res) => {
    res.cookie("token", JSON.stringify(apiData.data.access_token));
    res.cookie("refreshToken", JSON.stringify(apiData.data.refresh_token));
    res.redirect("/");
};

// LinkedIn
router.get("/auth/linkedin",
    passport.authenticate("linkedin", {
        state: true,
        session: false
    }),
    (req, res) => res.redirect("/")
);

router.get("/auth/linkedin/callback", (req, res) => {
    passport.authenticate("linkedin", data => {
        const token = data.token;
        const email = data.profile.emails && data.profile.emails.length ?
            data.profile.emails[0].value :
            null;

        usersApi.authenticateLinkedin(token, email).then(apiData => {
            setSessionCookies(apiData, res);
        })  // TODO: Handle errors.
            .catch(error => console.log(error));
    })(req, res);
});

// Google
router.get("/auth/google", passport.authenticate("google", {
    scope: ["profile", "email"]
}));

router.get("/auth/google/callback", (req, res) => {
    passport.authenticate("google", {
        failureRedirect: "/users/login"
    }, (data) => {
        const token = data.token;

        usersApi.authenticateGoogle(token).then(apiData => {
            setSessionCookies(apiData, res);
        })  //TODO: Handle errors.
            .catch(error => console.log(error));
    })(req, res);
});

// Facebook
router.get("/auth/facebook", passport.authenticate("facebook", {
    scope: ["email"]
}));

router.get("/auth/facebook/callback", (req, res) => {
    passport.authenticate("facebook", {
        failureRedirect: "/users/login",
    }, (data) => {
        const token = data.token;

        usersApi.authenticateFacebook(token).then(apiData => {
            setSessionCookies(apiData, res);
        })  // TODO: Handle errors.
            .catch(error => console.log(error));
    })(req, res);
});

module.exports = {
    default: router
};
