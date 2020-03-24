import {userActionTypes} from "./actions";

const initialState = {
    user: {
        id: 0,
        username: "",
        password: ""
    }
};

export default (state = initialState, action) => {
    switch (action.type) {
        case userActionTypes.LOG_IN:
        case userActionTypes.SIGN_UP:
        case userActionTypes.LOAD_USER:
            return {
                ...state,
                user: action.user
            };
        case userActionTypes.LOG_OUT:
            return {
                ...state,
                user: null
            };
        default:
            return state;
    }
};
