import React, {useState, useEffect} from "react";
import {connect} from "react-redux";
import Router from "next/router";
import Cookies from "js-cookie";

import {withTranslation} from "../../i18n";
import {userActionTypes} from "../../redux/user/actions";
import {updateUser, getCurrentUser, refreshSession} from "../../api/users";

const getInitialState = () => ({
    username: "",
    email: "",
    password: "",
    passwordConfirmation: ""
});

const Profile = props => {
    const [state, setState] = useState(getInitialState());
    const token = Cookies.get("token");
    const refreshToken = Cookies.get("refreshToken");

    useEffect(() => {
        if (!token) {
            Router.push("/users/login");
        }

        getCurrentUser(token).then(response => {
            props.setUser(response.data.user);
        }).catch(error => {
            if (error.response && error.response.status === 401) {
                refreshSession(refreshToken).then(response => {
                    Cookies.set("token", JSON.stringify(response.data.access_token));
                    props.setUser(response.data.user);
                }).catch(() => {
                    Router.push("/users/login");
                });
            }
        });
    }, [token]);

    const logOutUser = () => {
        Cookies.remove("token");
        props.onLogout();
    };

    const handleFormChange = e => {
        e.persist();
        setState(prevState => ({
            ...prevState,
            [e.target.name]: e.target.value
        }));
    };

    const handleFormSubmit = () => {
        const updatedUser = {...props.user};
        updatedUser.username = state.username;
        updatedUser.email = state.email;
        updatedUser.password = state.password;

        updateUser(
            updatedUser,
            Cookies.get("token")
        )
            .then(response => {
                Cookies.set("token", JSON.stringify(response.data.access_token));
            })
            // TODO: Handle errors.
            .catch(error => console.log(error));
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
                    <form onSubmit={() => handleFormSubmit()}>
                        <div>
                            <input name="username"
                                   onChange={e => handleFormChange(e)}
                                   placeholder="Username"
                                   type="text"
                                   value={state.username}/>
                        </div>
                        <div>
                            <input name="email"
                                   onChange={e => handleFormChange(e)}
                                   placeholder="Email"
                                   type="email"
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
                        <button disabled={state.password !== state.passwordConfirmation} type="submit">
                            Submit
                        </button>
                    </form>
                </div>
            </div>
        );
    } else {
        return <h3>Loading...</h3>;
    }
};

Profile.getInitialProps = async () => {
    return {namespacesRequired: ["common"]};
};

const mapStateToProps = state => ({
    ...state.user
});

const mapDispatchToProps = dispatch => ({
    onLogout: () => dispatch({type: userActionTypes.LOG_OUT}),
    setUser: (user) => dispatch({type: userActionTypes.LOAD_USER, user})
});

export default connect(mapStateToProps, mapDispatchToProps)(withTranslation("common")(Profile));
