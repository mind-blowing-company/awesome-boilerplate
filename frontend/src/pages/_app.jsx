import React from "react";
import App from "next/app";
import {Provider} from "react-redux";
import withRedux from "next-redux-wrapper";
import {PersistGate} from "redux-persist/integration/react";
import {persistStore} from "redux-persist";

import {appWithTranslation} from "../i18n";
import initStore from "../redux/store";
import "../public/App.css";

class MyApp extends App {
    static async getInitialProps({Component, ctx}) {
        let pageProps;

        if (Component.getInitialProps) {
            pageProps = await Component.getInitialProps(ctx);
        }

        return {pageProps};
    }

    render() {
        const {Component, pageProps, store} = this.props;

        return (
            <Provider store={store}>
                <PersistGate loading={<Component {...pageProps}/>} persistor={persistStore(store)}>
                    <Component {...pageProps}/>
                </PersistGate>
            </Provider>
        );
    }
}

export default withRedux(initStore)(appWithTranslation(MyApp));
