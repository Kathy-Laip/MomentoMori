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
                <Img nameClass="roseTwo"/>
                <Img nameClass="roseThree"/>
                <Img nameClass="roseFour"/>
                <Img nameClass="roseFive"/>
                <Img nameClass="roseSix"/>
                <Img nameClass="roseSeven"/>
                <Img nameClass="roseEight"/>
                <Img nameClass="roseNine"/>
                <Img nameClass="roseTen"/>
            </div>
        )
    }
}

export default LogIn