const passport = require("passport");
const LinkedInStrategy = require("passport-linkedin-oauth2").Strategy;
const GoogleStrategy = require("passport-google-oauth20").Strategy;
const FacebookStrategy = require("passport-facebook").Strategy;

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

passport.use("google", new GoogleStrategy({
    clientID: keys.GOOGLE.id,
    clientSecret: keys.GOOGLE.secret,
    callbackURL: "http://localhost:3000/auth/google/callback"
}, (accessToken, refreshToken, profile, cb) => {
        return cb({
            token: accessToken,
            profile: profile
        });
}));

passport.use("facebook", new FacebookStrategy({
    clientID: keys.FACEBOOK.id,
    clientSecret: keys.FACEBOOK.secret,
    callbackURL: "http://localhost:3000/auth/facebook/callback"
}, (accessToken, refreshToken, profile, cb) => {
    return cb({
        token: accessToken,
        profile: profile
    });
}));

exports.default = passport;
