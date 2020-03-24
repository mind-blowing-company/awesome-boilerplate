import React from "react";
import App from "next/app";
import {Provider} from "react-redux";
import withRedux from "next-redux-wrapper";

import {appWithTranslation} from "../i18n";
import initStore from "../redux/store";
import "../public/App.css";
import {userActionTypes} from "../redux/user/actions";

class MyApp extends App {
    componentDidMount() {
        this.props.store.dispatch({
            "type": userActionTypes.LOAD_USER,
            "user": JSON.parse(localStorage.getItem("user")) || null
        });
    }

    render() {
        const {Component, pageProps, store} = this.props;

        return (
            <Provider store={store}>
                <Component {...pageProps} />
            </Provider>
        );
    }
}

export default withRedux(initStore)(appWithTranslation(MyApp));
