const express = require("express");

const router = express.Router();
const passport = require("../passport").default;
const api = require("../api");

router.get("/auth/linkedin",
    passport.authenticate("linkedin", {
        state: true,
        session: false
    }),
    (req, res) => res.redirect("/")
);

router.get("/auth/linkedin/callback", (req, res) => {
    passport.authenticate("linkedin", (data) => {
        const email = data.profile.emails.length ? data.profile.emails[0].value : null;
        const token = data.token;

        api.authenticateLinkedin(token, email).then(response => {
            res.cookie("token", JSON.stringify(response.data.access_token));
            res.cookie("user", JSON.stringify(response.data.user));
            return res.redirect("/");
        });
    })(req, res);
});

module.exports = {
    default: router
};
