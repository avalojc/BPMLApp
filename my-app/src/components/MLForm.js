import React, { Component } from 'react'
import axios from 'axios'

export class MainMLForm extends Component {
    // create state for test values and input validations.
    state = {
        testPrediction: null,
        testHR: null,
        testHRRegularity: null,
        testCuffSize: null,
        inputHR:null,
        inputHRRegularity: null,
        inputCuff: null,
        stateReady: 0,
        responseValue: null,
    }
    //validation
    cuffValidation = () => {
        switch(this.state.inputCuff){
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
    //validation
    HRRegularityValidation = () => {
        switch(this.state.inputHRRegularity){
            case "true":
            case "t":
                this.setState({testHRRegularity: 1})
                break;
            case "false":
            case "f":
                this.setState({testHRRegularity: 2})
                break;
            default:
                alert('Your input must be Regular(true) or Irregular(false)')
                break;
        }
    }
    // set heart rate
    onNewHRAdd = (event) => {
        const hR = event.target.value;
        this.setState({inputHR: hR})
    }
    //set heart rate regularity
    onNewHRRegularityAdd = (event) => {
        const hRReg = event.target.value.toLowerCase();
        this.setState({inputHRRegularity: hRReg})
    }
    // set cuff size
    onNewCuffSizeAdd = (event) => {
        const cuff = event.target.value;
        this.setState({inputCuff: cuff})
    }
    // run all input validations and set states
    inputValidation = (event) => {
        event.preventDefault()
        this.cuffValidation()   
        this.HRRegularityValidation()
        this.setState({testHR: parseInt(this.state.inputHR,10)})
        this.createPredictionObj()
    }
    // create prediction object to send to back end.
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
        if(this.state.stateReady === 1){
            this.predict(this.state.testPrediction)
        }
    }
        // send prediction object return prediction.
    predict = (objectToPost) => {
        (axios.post('/predict',objectToPost))
        .then(function(response){
            if(response.data.prediction[1]==1){
                document.getElementById('predict').innerHTML = 'The patient is at risk'
            } else{
                document.getElementById('predict').innerHTML = 'The patient is not at risk'
            }
        })
        .catch(function(error){
            console.log(error)
        })            // WIP in progress for a connection to gcp ml model
        //nhanes-bp-ml //nhanesbp_20200521085117
        // axios.post('https://ml.googleapis.com/v1/projects/nhanes-bp-ml/models/nhanesbp_20200521085117:predict', objectToPost)
        // .then(function(response){
        //     console.log(response)
        // })
        // .catch(function(error){
        //     console.log(error)
        // })
   }
        // render form
    render() {
        return (
            <form>
                <div className='rightForm'>
                    <p className='formBlurb'>Required*</p>
                    <input
                        type="string"
                        name="HR"
                        placeholder="Heart Rate (BPM)"
                        required="required"
                        onChange={this.onNewHRAdd}
                        value={this.state.newTestHR}
                    />
                    <p className='formBlurb'>Required* (true for regular, false for irregular heart beats)</p>
                    <input
                        type="string"
                        name="HRReg"
                        placeholder="Is the heart rate regular? True or false."
                        required="required"
                        onChange={this.onNewHRRegularityAdd}
                        value={this.state.newTestHRReg}
                    /> 
                    <p className='formBlurb'>
                        Required*    
                        <a className='tooltip' href=''>
                            &ensp; Hover here for more information on cuff sizes
                            <span>
                            </span>
                        </a>
                    </p>
                    <input
                        type="string"
                        name="CuffSize"
                        placeholder="Cuff Size"
                        required="required"
                        onChange={this.onNewCuffSizeAdd}
                        value={this.state.newCuffSize}
                    /> 
                </div>
                <button className='button' onClick={this.inputValidation}><span>Submit</span></button>
            </form>
        )
    }
}

export default MainMLForm
