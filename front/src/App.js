import React from 'react';
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Login from "./components/views/Login";
import Register from "./components/views/Register";
import Forgot from "./components/views/Forgot";
import Editor from "./components/views/Editor";
import ProjectsExplorer from "./components/views/ProjectsExplorer";

const Auth = () => {
  return (
    <Router>
      <Switch>
        <Route path='/login' component={Login} />
        <Route path='/register' component={Register} />
        <Route path='/forgot-password' component={Forgot} />
        <Route path='/projects-explorer' component={ProjectsExplorer} />
        <Route path='/' component={Editor} />
      </Switch>
    </Router>
  );
}

export default Auth;
