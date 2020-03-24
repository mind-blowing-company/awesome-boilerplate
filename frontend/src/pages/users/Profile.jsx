import React from "react";
import {connect} from "react-redux";

import {withTranslation} from "../../i18n";

const Profile = props => {
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
            <button type="button">
                Log Out
            </button>
        </div>
    );
};

Profile.getInitialProps = async () => ({
    namespacesRequired: ["common"]
});

const mapStateToProps = state => ({
    ...state.user
});

export default connect(mapStateToProps, {})(withTranslation("common")(Profile));
