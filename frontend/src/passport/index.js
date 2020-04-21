const passport = require("passport");
const LinkedInStrategy = require("passport-linkedin-oauth2").Strategy;
const GoogleStrategy = require("passport-google-oauth20").Strategy;
const FacebookStrategy = require("passport-facebook").Strategy;

const keys = require("../../config/socialKeys").default;

const processSocialCallback = (accessToken, refreshToken, profile, cb) => {
    return cb({
        token: accessToken,
        profile: profile
    });
};

passport.use("linkedin", new LinkedInStrategy({
    clientID: keys.LINKEDIN.id,
    clientSecret: keys.LINKEDIN.secret,
    callbackURL: process.env.LINKEDIN_CALLBACK_URL,
    scope: ["r_emailaddress", "r_liteprofile"]
}, processSocialCallback));

passport.use("google", new GoogleStrategy({
    clientID: keys.GOOGLE.id,
    clientSecret: keys.GOOGLE.secret,
    callbackURL: process.env.GOOGLE_CALLBACK_URL,
}, processSocialCallback));

passport.use("facebook", new FacebookStrategy({
    clientID: keys.FACEBOOK.id,
    clientSecret: keys.FACEBOOK.secret,
    callbackURL: process.env.FACEBOOK_CALLBACK_URL,
}, processSocialCallback));

exports.default = passport;
