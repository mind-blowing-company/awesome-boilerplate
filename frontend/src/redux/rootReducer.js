import {combineReducers} from "redux";

import user from "./user/reducer";

// Add new reducers here.
export const rootReducer = combineReducers({
    user
});
