const express = require("express");

const router = express.Router();
const passport = require("../passport/index").default;

router.get("/auth/linkedin",
    passport.authenticate("linkedin", {
        state: true,
        session: false
    }),
    (req, res) => res.redirect("/")
);

router.get("/auth/linkedin/callback", (req, res) => {
    passport.authenticate("linkedin", (data) => {
        // TODO: Handle LinkedIn auth.
        console.log(data);
        return res.redirect("/");
    })(req, res);
});

module.exports = {
    default: router
};
