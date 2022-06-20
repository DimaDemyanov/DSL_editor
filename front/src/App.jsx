import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Login from './components/views/Login';
import Register from './components/views/Register';
import Forgot from './components/views/Forgot';
import DSLEditor from './components/views/DSLEditor';
import ProjectsExplorer from './components/views/ProjectsExplorer';
import MenuAppBar from './components/views/MenuAppBar';

function WithMenuContainer() {
  return (
    <div className="default-container">
      <MenuAppBar />
      <Route path="/projects-explorer" component={ProjectsExplorer} />
      <Route path="/editor" component={DSLEditor} />
    </div>
  );
}

function App() {

  return (
    <Router>
      <Switch>
        <Route exact path="/" component={Login} />
        <Route exact path="/login" component={Login} />
        <Route path="/register" component={Register} />
        <Route path="/forgot-password" component={Forgot} />
        <Route component={WithMenuContainer} />
      </Switch>
    </Router>
  );
}

export default App;
