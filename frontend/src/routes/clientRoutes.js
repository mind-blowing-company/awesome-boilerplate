const UrlPrettifier = require("next-url-prettifier").default;

const routes = [
    {
        page: "users/AuthPage",
        prettyUrl: "/users/login"
    },
    {
        page: "users/Profile",
        prettyUrl: "/"
    }
];

const router = new UrlPrettifier(routes);

exports.default = routes;
exports.Router = router;
