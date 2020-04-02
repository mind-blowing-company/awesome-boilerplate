import React from "react";
import App from "next/app";
import {Provider} from "react-redux";
import withRedux from "next-redux-wrapper";
import Cookie from "js-cookie";

import {appWithTranslation} from "../i18n";
import initStore from "../redux/store";
import "../public/App.css";
import {userActionTypes} from "../redux/user/actions";

class MyApp extends App {
    static async getInitialProps({Component, ctx}) {
        let pageProps;

        if (Component.getInitialProps) {
            pageProps = await Component.getInitialProps(ctx);
        }

        return {pageProps};
    }

    componentDidMount() {
        const user = Cookie.get("user");
        const token = Cookie.get("token");
        if (user && token) {
            this.props.store.dispatch({type: userActionTypes.LOAD_USER, user: JSON.parse(user)});
        }
    }

    render() {
        const {Component, pageProps, store} = this.props;

        return (
            <Provider store={store}>
                <Component {...pageProps}/>
            </Provider>
        );
    }
}

export default withRedux(initStore)(appWithTranslation(MyApp));
