import React, {useState} from "react";
import Link from "next/link";
import Router from "next/router";
import Cookies from "js-cookie";

import {loginUser, registerUser} from "../../api/users";
import {withTranslation} from "../../i18n";

const getInitialState = () => ({
    username: "",
    password: "",
    passwordConfirmation: ""
});

const AuthPage = () => {
    const [state, setState] = useState(getInitialState);

    const handleFormChange = e => {
        e.persist();
        setState(prevState => ({
            ...prevState,
            [e.target.name]: e.target.value
        }));
    };

    const saveUserSession = (token) => {
        Cookies.set("token", JSON.stringify(token));
        Router.push("/");
    };

    const handleFormSubmit = (e) => {
        e.preventDefault();
        if (!state.passwordConfirmation) {
            loginUser(state.username, state.password, saveUserSession)
                // TODO: Handle these errors. Tell that password is wrong et c.
                .catch(error => console.log(error));
        } else {
            registerUser(state.username, state.password, saveUserSession)
                // TODO: Handle errors. Show that user exists et c.
                .catch(error => console.log(error));
        }
    };

    return (
        <div className="center-children">
            <div className="form-container">
                <form onSubmit={e => handleFormSubmit(e)}>
                    <div>
                        <input name="username"
                               onChange={e => handleFormChange(e)}
                               placeholder="Username"
                               required={true}
                               type="text"
                               value={state.username}/>
                    </div>
                    <div>
                        <input name="password"
                               onChange={e => handleFormChange(e)}
                               placeholder="Password"
                               required={true}
                               type="password"
                               value={state.password}/>
                    </div>
                    <div>
                        <input name="passwordConfirmation"
                               onChange={e => handleFormChange(e)}
                               placeholder="Password Confirmation"
                               type="password"
                               value={state.passwordConfirmation}/>
                    </div>
                    <div>
                        <button disabled={!state.password || !state.username}
                                type="submit">
                            Submit
                        </button>
                    </div>
                </form>
            </div>
            <div className="social-container">
                <Link href={"/auth/linkedin"}>
                    <a>
                        LinkedIn
                    </a>
                </Link>
                <Link href={"/auth/google"}>
                    <a>
                        Google
                    </a>
                </Link>
                <Link href={"/auth/facebook"}>
                    <a>
                        Facebook
                    </a>
                </Link>
            </div>
        </div>
    );
};

AuthPage.getInitialProps = async () => {
    return {namespacesRequired: ["common"]};
};

export default withTranslation("common")(AuthPage);
