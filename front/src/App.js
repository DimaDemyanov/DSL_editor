import React from 'react';
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Login from "./components/views/Login";
import Register from "./components/views/Register";
import Forgot from "./components/views/Forgot";
import Editor from "./components/views/Editor";
import ProjectsExplorer from "./components/views/ProjectsExplorer";
import MenuAppBar from "./components/views/MenuAppBar";

const Auth = () => {
  return (
    <Router>
      <MenuAppBar/>
      <Switch>
        <Route path='/login' component={Login} />
        <Route path='/register' component={Register} />
        <Route path='/forgot-password' component={Forgot} />
        <Route path='/projects-explorer' component={ProjectsExplorer} />
        <Route path='/editor' component={Editor} />
        <Route path='/' component={Login} />
      </Switch>
    </Router>
  );
}

export default Auth;
