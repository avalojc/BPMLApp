import React, { Component } from 'react'
// import {    Link  } from "react-router-dom";
//import axios from 'axios'
//import NearEarthObjects from './NearEarthObjects'
// import LastUpdate from './LastUpdate'

export class MainML extends Component {
    render() {
        return (
            <div className='headingDisclaimer' >
                <h1>Welcome to the Blood Pressure Risk Machine Learning AI</h1>
                <p>Below is a form that will predict your risk of high blood pressure using a machine learning algorithm. Please note, that this is just an exercise in machine learning and is not meant to replace the expertise of your physician. Do not draw conclusions on it for your health.</p>
            </div>
        )
    }
}

export default MainML


  