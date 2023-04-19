const requset = new XMLHttpRequest()
var btn = document.querySelector('.buttonLogIn')

class User {
    constructor(options){
        this.login = options.login,
        this.password = options.password
    }

    async authorization(){
        let response = await fetch("/signIn", {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(user)
        });
        let result = await response.json()
    

        if (result.user_found == true){
            alert('Вы вошли!')
            if(result.status == "клиент"){
                client = new Client({id: result.id})
                sessionStorage.setItem('clientID', client.id)
                window.location.href = '/pages/clientOrders.html'
            } else if(result.status == "менеджер"){
                manager = new Manager({id: result.id})
                sessionStorage.setItem('managerID', manager.id)
                window.location.href = '/pages/managerStorage.html'
            }
        } else alert('Что-то не так, не удается войти в систему!')
    }
}

class Manager {
    constructor(options){
        // super(options)
        this.id = options.id
    }
}

class Client {
    constructor(options){
        // super(options)
        this.id = options.id
    }
}

var manager
var user
var client
const btnClick = () => {
    const log = document.querySelector('#email').value
    const pas = document.querySelector('#password').value
    user = new User({login: log, password: pas})
    user.authorization()
}

module.exports = User