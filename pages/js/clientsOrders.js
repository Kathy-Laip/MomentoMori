const requset = new XMLHttpRequest()
const client = sessionStorage.getItem('clientID')
console.log(client)
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


// функция получения информация о всех заказах клиента
// также размещает информацию о закаах на страницу и формирует все функции, связанные с заказами
async function sendClinetID(){
    let clientID = {
        clientId: client
    }
    let response = await fetch('/ordersOfClient', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(clientID)
    });
    let result = await response.json()

    if (result[0].ordersFound){
        for (let i = 1; i < result.length; i++){
            orders.push(new Order(result[i]))
            let boxOrdersText = `<div class="containerOrder">
                <div class="textOrder">
                    <strong>Заказ №${result[i].id} </strong>
                    <br> Цена: ${result[i].price} рублей <br> 
                    Адресс: ${result[i].address} <br>
                     ФИО покойного: ${result[i].deadmansName} 
                     <br> статус: ${result[i].status}
                </div>
            </div> `
            boxOrders.innerHTML +=  boxOrdersText
        }
    }
}

sendClinetID()

// requset.send()