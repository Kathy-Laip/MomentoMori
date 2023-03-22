import React from "react";
import Img from "./Img";
import EntranceBox from "./EntranceBox"

class LogIn extends React.Component{
    constructor(props){
        super(props)
    }

    render(){
        return(
            <div>
                <Img nameClass="roseOne"/>
                <EntranceBox/>
            </div>
        )
    }
}

export default LogIn