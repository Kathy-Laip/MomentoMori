import React from "react";

class Img extends React.Component{
    constructor(props){
        super(props)
    }

    render(){
        return(
            <div className={`pill ${this.props.nameClass}`}></div>
        )
    }
}

export default Img