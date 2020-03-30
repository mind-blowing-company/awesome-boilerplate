import React from "react";
import {connect} from "react-redux";
import Router from "next/router";
import Cookies from "js-cookie";

import {withTranslation} from "../../i18n";
import {userActionTypes} from "../../redux/user/actions";

const Profile = props => {
        const logOutUser = () => {
            Cookies.remove("token");
            props.onLogout();
        };

        if (props.user) {
            return (
                <div className="profile-container">
                    <h3>Current user</h3>
                    <table>
                        <thead>
                        <tr>
                            <th>ID</th>
                            <th>Username</th>
                            <th>Password hash</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr>
                            <td>{props.user.id}</td>
                            <td>{props.user.username}</td>
                            <td>{props.user.password}</td>
                        </tr>
                        </tbody>
                    </table>
                    <button onClick={() => logOutUser()} type="button">
                        Log Out
                    </button>
                </div>
            );
        } else {
            Router.push("/users/login");
        }
    }
;

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
