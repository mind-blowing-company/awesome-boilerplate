import {applyMiddleware, createStore} from "redux";
import thunkMiddleware from "redux-thunk";
import {composeWithDevTools} from "redux-devtools-extension";
import {persistReducer} from "redux-persist";
import storage from "redux-persist/lib/storage";

import {rootReducer} from "./rootReducer";

const bindMiddleware = middleware => {
    if (process.env.NODE_ENV !== "production") {
        return (composeWithDevTools(applyMiddleware(...middleware)));
    }

    return applyMiddleware(...middleware);
};

const initStore = () => {
    let store;
    const isClient = typeof window !== "undefined";
    const middleware = bindMiddleware([thunkMiddleware]);

    if (isClient) {
        const persistConfig = {
            key: "root",
            storage,
            whitelist: "user"
        };

        store = createStore(
            persistReducer(persistConfig, rootReducer),
            middleware
        );
    } else {
        store = createStore(
            rootReducer,
            middleware
        );
    }

    return store;
};

export default initStore;
