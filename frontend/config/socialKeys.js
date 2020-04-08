const env = process.env;

exports.default = {
    LINKEDIN: {
        id: env.LINKEDIN_KEY,
        secret: env.LINKEDIN_SECRET
    },
    GOOGLE: {
        id: env.GOOGLE_KEY,
        secret: env.GOOGLE_SECRET
    },
    FACEBOOK: {
        id: env.FACEBOOK_KEY,
        secret: env.FACEBOOK_SECRET
    }
};
