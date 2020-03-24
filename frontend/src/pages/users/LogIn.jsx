import React, {useState} from "react";
import Link from "next/link";
import {connect} from "react-redux";

import {loginUser} from "../../api";
import {userActionTypes} from "../../redux/user/actions";
import {withTranslation} from "../../i18n";

const LogIn = (props) => {
    const [state, setState] = useState({username: "", password: ""});
    const {t} = props;

    const handleChange = e => {
        e.persist();
        setState(prevState => ({
            ...prevState,
            [e.target.name]: e.target.value
        }));
    };

    const handleFormSubmit = e => {
        e.preventDefault();
        loginUser(state.username, state.password).then(result => {
            const user = result.user;

            localStorage.setItem("token", result.token);
            localStorage.setItem("user", JSON.stringify(user));
            props.onFormSubmit(user);
        }).catch(error => {
            // TODO: Handle error.
            console.log(error);
        });
    };

    return (
            <div className="center-children">
                <div className="form-container">
                    <form onSubmit={e => handleFormSubmit(e)}>
                        <div className="input-group">
                            <input name="username"
                                   onChange={e => handleChange(e)}
                                   placeholder={t("username")}
                                   type="text"
                                   value={state.username}/>
                        </div>
                        <div className="input-group">
                            <input name="password"
                                   onChange={e => handleChange(e)}
                                   placeholder={t("password")}
                                   type="password"
                                   value={state.password}/>
                        </div>
                        <button type="submit">
                            {t("submit")}
                        </button>
                    </form>
                </div>
                <div className="social-container">
                    <Link href={"/linkedin/callback"}>
                        <a>
                            {t("linkedin")}
                        </a>
                    </Link>
                </div>
            </div>
    );
};

LogIn.getInitialProps = async () => ({
    namespacesRequired: ["common"]
});

const mapStateToProps = state => ({...state.user});

const mapDispatchToProps = dispatch => ({
    onFormSubmit: user => {
        dispatch({type: userActionTypes.LOG_IN, user});
    }
});

export default connect(mapStateToProps, mapDispatchToProps)(withTranslation("common")(LogIn));
