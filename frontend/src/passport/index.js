const passport = require("passport");
const LinkedInStrategy = require("passport-linkedin-oauth2").Strategy;

const keys = require("../../config/socialKeys").default;

passport.use("linkedin", new LinkedInStrategy({
    clientID: keys.LINKEDIN.id,
    clientSecret: keys.LINKEDIN.secret,
    // TODO: Add valid URL.
    callbackURL: "http://localhost:3000/auth/linkedin/callback",
    scope: ["r_emailaddress", "r_liteprofile"]
}, (accessToken, refreshToken, profile, cb) => {
    return cb({
        token: accessToken,
        profile: profile
    });
}));

exports.default = passport;
