import React from 'react';
import './App.css';
import {BrowserRouter as Router, Route } from 'react-router-dom'
import MainML from './components/mainml'
import MainMLForm from './components/MLForm';
import MLResponse from './components/MLResponse';

function App() {
  return (
    <div className="App">
      <Router>
          <Route exact path='/' component={MainML}/>
          <Route exact path='/' component={MainMLForm}/>
          <Route exact path='/' component={MLResponse}/>
      </Router>
    </div>
  );
}

export default App;
