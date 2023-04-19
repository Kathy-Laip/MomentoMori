var request = new XMLHttpRequest()
request.open('POST', '/ordersForManager', true)

const p = new Promise((res, rej) => {
    request.onload = () => {
        var dataAboutProduct = request.responseText
        res(dataAboutProduct)
    }
}).then(dataAboutProduct => {
    getProducts(dataAboutProduct)
})

async function getProducts(dataAboutProduct){
    var infoProducts = JSON.parse(dataAboutProduct)
    console.log(infoProducts)

    insertINtoProducts(infoProducts)

    function insertINtoProducts(infoProducts){
        var container = document.getElementById('products')
        if(infoProducts[0]["ordersFound"]){
            for(let i = 1; i < infoProducts.length; i++){
                var textProduct = `
                <div class="containerOrder">
                    <div class="textOrder">
                        <strong>Заказ №${infoProducts[i].id} </strong> 
                        <br> <strong> ФИО заявителя: </strong> ${infoProducts[i].clientsFio} 
                        <br> <strong> Адрес: </strong> ${infoProducts[i].address} 
                        <br> <strong> ФИО покойного: </strong> ${infoProducts[i].deadmansName}
                        <br> <strong> Общая цена: </strong> ${infoProducts[i].price} рублей
                        <br> <strong> статус: </strong> ${infoProducts[i].status}
                    </div>
                </div> 
                `
                container.innerHTML += textProduct
            }
        }
    }
}

request.send()