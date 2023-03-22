import React from "react";

class App extends React.Component{
  // constructor(props){
  //   super(props)
  // }

  render(){
    return (
      <div className="entranceBox">
        <div className="entranceBoxName">Вход</div>
        <input type="email" id="email" placeholder="Логин"></input>
        <input type="password" id="password" placeholder="Пароль"></input>
        <button className="buttonLogIn">Войти</button>
      </div>
    );
  }
}

export default App;
