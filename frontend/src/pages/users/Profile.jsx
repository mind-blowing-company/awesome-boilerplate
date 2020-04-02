import React, {useState, useEffect} from "react";
import {connect} from "react-redux";
import Router from "next/router";
import Cookie from "js-cookie";

import {withTranslation} from "../../i18n";
import {userActionTypes} from "../../redux/user/actions";
import {updateUser} from "../../api";

const getInitialState = () => ({
    email: "",
    password: "",
    passwordConfirmation: ""
});

const Profile = props => {
    const [state, setState] = useState(getInitialState());
    const user = Cookie.get("user");
    const token = Cookie.get("token");

    useEffect(() => {
        if (!user || !token) {
            Router.push("/users/login");
        }
    }, [user, token]);

    const logOutUser = () => {
        Cookie.remove("token");
        Cookie.remove("user");
        props.onLogout();
    };

    const handleFormChange = e => {
        e.persist();
        setState(prevState => ({
            ...prevState,
            [e.target.name]: e.target.value
        }));
    };

    const handleFormSubmit = e => {
        e.preventDefault();
        updateUser(
            state.email,
            state.password,
            Cookie.get("token")
        ).then(response => console.log(response));
    };

    if (props.user) {
        return (
            <div className="center-children">
                <div>
                    <h3>Current user</h3>
                    <table>
                        <thead>
                        <tr>
                            <th>ID</th>
                            <th>Username</th>
                            <th>Password hash</th>
                            <th>Email</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr>
                            <td>{props.user.id}</td>
                            <td>{props.user.username}</td>
                            <td>{props.user.password}</td>
                            <td>{props.user.email}</td>
                        </tr>
                        </tbody>
                    </table>
                    <button onClick={() => logOutUser()} type="button">
                        Log Out
                    </button>
                </div>
                <div>
                    <h2>Edit User</h2>
                    <form onSubmit={e => handleFormSubmit(e)}>
                        <div>
                            <input name="email"
                                   onChange={e => handleFormChange(e)}
                                   placeholder="Email"
                                   type="text"
                                   value={state.email}/>
                        </div>
                        <div>
                            <input name="password"
                                   onChange={e => handleFormChange(e)}
                                   placeholder="New Password"
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
                        <button type="submit">
                            Submit
                        </button>
                    </form>
                </div>
            </div>
        );
    } else {
        return <h3>Redirecting to login.</h3>;
    }
};

Profile.getInitialProps = async () => {
    return {namespacesRequired: ["common"]};
};

const mapStateToProps = state => ({
    ...state.user
});

const mapDispatchToProps = dispatch => ({
    onLogout: () => dispatch({type: userActionTypes.LOG_OUT})
});

export default connect(mapStateToProps, mapDispatchToProps)(withTranslation("common")(Profile));
