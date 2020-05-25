import React, { Component } from 'react'
// import {    Link  } from "react-router-dom";
//import axios from 'axios'
//import NearEarthObjects from './NearEarthObjects'
// import LastUpdate from './LastUpdate'

export class MainMLForm extends Component {
    state = {
        testPrediction: null,
        testHR: null,
        testHRRegularity: null,
        testCuffSize: null,
        HRInput:null,
        HRRegularityInput: null,
        cuffInput: null,
        stateReady: 0
    }
    cuffValidation = () => {
        // console.log(this.state.cuffInput)
        // console.log(2)
        // console.log("2")
        switch(this.state.cuffInput){
            case "2":
                this.setState({testCuffSize: 2})
                break;
            case "3":
                this.setState({testCuffSize: 3})
                break;
            case "4":
                this.setState({testCuffSize: 4})
                break;
            case "5":
                this.setState({testCuffSize: 5})
                break;
            default:
                alert('Your cuff size value must be 2-5')
                break;
        }
    }
    HRRegularityValidation = () => {
        switch(this.state.HRRegularityInput){
            case "0":
            // case 'R':
            // case 'Regular':
                this.setState({testHRRegularity: 0})
                break;
            case "1":
                this.setState({testHRRegularity: 1})
                break;
            // case 'I':
            //     this.setState({testHRRegularity: 1})
            //     break;
            // case 'Irregular':
            //     this.setState({testHRRegularity: 1})
            //     break;
            default:
                alert('Your input must be Regular(0) or Irregular(1)')
                break;
        }
    }
    onNewHRAdd = (event) => {
        const hR = event.target.value;
        this.setState({HRInput: hR})
    }
    onNewHRRegularityAdd = (event) => {
        const hRReg = event.target.value;
        this.setState({HRRegularityInput: hRReg})
    }
    onNewCuffSizeAdd = (event) => {
        const cuff = event.target.value;
        this.setState({cuffInput: cuff})
    }
    inputValidation = (event) => {
        event.preventDefault()
        this.cuffValidation()   
        this.HRRegularityValidation()
        this.setState({testHR: parseInt(this.state.HRInput,10)})
        this.createPredictionObj()
    }
    createPredictionObj=()=>{
        switch(this.state.testCuffSize){
            case 2:
                this.setState(
                    {
                        testPrediction:
                        [{
                            "BPACSZ2":1	,"BPACSZ3":0	,"BPACSZ4":0	,"BPACSZ5":0	,"BPXPLS":this.state.testHR	,"BPXPULS":this.state.testHRRegularity
                        }]
                    }
                )
                this.setState({stateReady: 1})
                break;
            case 3:
                this.setState(
                    {
                        testPrediction:
                        [{
                            "BPACSZ2":0	,"BPACSZ3":1	,"BPACSZ4":0	,"BPACSZ5":0	,"BPXPLS":this.state.testHR	,"BPXPULS":this.state.testHRRegularity
                        }]
                    }
                )
                this.setState({stateReady: 1})
                break;
            case 4:
                this.setState(
                    {
                        testPrediction:
                        [{
                            "BPACSZ2":0	,"BPACSZ3":0	,"BPACSZ4":1	,"BPACSZ5":0	,"BPXPLS":this.state.testHR	,"BPXPULS":this.state.testHRRegularity
                        }]
                    }
                )
                this.setState({stateReady: 1})
                break;
            case 5:
                this.setState(
                    {
                        testPrediction:
                        [{
                            "BPACSZ2":0	,"BPACSZ3":0	,"BPACSZ4":0	,"BPACSZ5":1	,"BPXPLS":this.state.testHR	,"BPXPULS":this.state.testHRRegularity
                        }]
                    }
                )
                this.setState({stateReady: 1})
                break;
            default:
                this.setState({testPrediction: "hello"})
        }
    }


    render() {
        return (
            <form>
                <div className='leftForm'>
                    Heart Rate (0-500): <br/>
                    Heart Rate Regularity (0-1): <br/>
                    Cuff Size (2-5):
                </div>
                <div className='rightForm'>
                    <input
                        type="string"
                        name="HR"
                        placeholder="Heart Rate"
                        required="required"
                        onChange={this.onNewHRAdd}
                        value={this.state.newTestHR}
                    /> <br/>
                    <input
                        type="string"
                        name="HRReg"
                        placeholder="Heart Rate Regularity"
                        required="required"
                        onChange={this.onNewHRRegularityAdd}
                        value={this.state.newTestHRReg}
                    /> <br/>
                    <input
                        type="string"
                        name="CuffSize"
                        placeholder="Cuff Size"
                        required="required"
                        onChange={this.onNewCuffSizeAdd}
                        value={this.state.newCuffSize}
                    /> 
                </div>
                <input 
                    type='submit'
                    onClick={this.inputValidation}
                />
            </form>
        )
    }
}

export default MainMLForm
