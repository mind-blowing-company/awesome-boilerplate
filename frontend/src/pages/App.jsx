import React from "react";
import {connect} from "react-redux";

import {withTranslation} from "../i18n";

// This component actually can be called whatever the developer
// would like to call it. However, to show how the routes are working
// it's called `App`.
// See `src/routes.js`.
const App = (props) => {
        const {t} = props;
        return (
            <div className="full-height center-children">
                Hi!
            </div>
        );
};

App.getInitialProps = async () => ({
    namespacesRequired: ["common"]
});

const mapStateToProps = state => ({
    ...state.user
});

export default connect(mapStateToProps, {})(withTranslation("common")(App));
