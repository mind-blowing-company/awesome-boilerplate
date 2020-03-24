// This is to use CSS imports instead of serving stylesheets by URL.
// Read more: https://github.com/zeit/next-plugins/tree/master/packages/next-css
const withCSS = require("@zeit/next-css");
require("./config/dotenv");
const Dotenv = require("dotenv-webpack");
const path = require("path");

module.exports = withCSS({
    pageExtensions: ["jsx", "tsx"],
    webpack: (config) => {
        config.plugins = [
            ...config.plugins,
            new Dotenv({
                path: path.join(__dirname, ".env"),
                systemvars: true
            })
        ];
        config.node = {
            fs: "empty"
        };
        return config;
    }
});
