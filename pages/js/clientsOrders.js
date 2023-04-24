const requset = new XMLHttpRequest()
const client_id = sessionStorage.getItem('clientID')
console.log(client_id)
const boxOrders = document.getElementById('services')

class Order {
    constructor(options){
        this.id = options.id
        this.price = options.prices
        this.status = options.status
        this.address = options.address
        this.deadmans_name = options.deadmans_name
    }
}

const orders = []

async function sendClinetID(){
    let response = await fetch('/ordersOfClient', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(client_id)
    });
    let result = await response.json()
    console.log(typeof(result))

    if (result.orders !== []){
        for (let order of result.orders){
            orders.push(new Order(order))
            let boxOrdersText = `<div class="containerOrder">
                <div class="textOrder">
                    <strong>Заказ №${order.id} </strong>
                    <br> Цена: ${order.price} рублей <br> 
                    Адресс: ${order.address} <br>
                     ФИО покойного: ${order.deadmans_name} 
                     <br> статус: ${order.status}
                </div>
            </div> `
            boxOrders.innerHTML +=  boxOrdersText
        }
    }
}

sendClinetID()

// requset.send()