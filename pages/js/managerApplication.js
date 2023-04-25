var request = new XMLHttpRequest()

request.open('POST', '/allProducts', true)

const p = new Promise((res, rej) => {
    request.onload = () => {
        var dataAboutProduct = request.responseText
        res(dataAboutProduct)
    }
}).then(dataAboutProduct => {
    getStuff(dataAboutProduct)
})

async function getStuff(dataStuff){
    var infoStuff = JSON.parse(dataStuff)
    console.log(infoStuff)

    // console.log(sessionStorage.getItem('managerID'))

    insertIntoStuffInCategory(infoStuff)

    function insertIntoStuffInCategory(infoStuff){
        var container = document.getElementById('category')
        if(infoStuff[0].itemsFound){
            for(let i = 0; i < infoStuff[1].products.length; i++){
                var textProduct = `<option value="${infoStuff[1].products[i]}">${infoStuff[1].products[i]}</option>`
                container.innerHTML += textProduct
            }
        }
    }

    document.getElementById('category').addEventListener('change', function(){
        let productChange = document.getElementById('product')
        productChange.innerHTML = '<option value=""></option>'
        let type = this.value

        var productType = infoStuff.filter(obj => obj.category === type)
        for(let pos of productType){
            if(pos.description === null){
                continue
            } else {
                productChange.innerHTML += `<option value="${pos.details}">${pos.details}</option>`
            }
        }
    })

    document.querySelector('.addProduct').addEventListener('click', function(){
        var nameProduct = document.getElementById('product').value
        var categoryProduct = document.getElementById('category').value
        var countProduct = document.getElementById('count').value
        var btnOF = document.querySelector('.arrange')
        var price
        var idProduct

        console.log(categoryProduct, nameProduct)

        for (let i=2; i < infoStuff.length; i++){
            if(infoStuff[i].category === categoryProduct && infoStuff[i].details === nameProduct){
                idProduct = infoStuff[i].id
                if(infoStuff[i].type == 'товар'){
                    console.log(infoStuff[i].costForOne)
                    price = infoStuff[i].costForOne * Number(countProduct)
                } 
            } else if(infoStuff[i].category === categoryProduct && infoStuff[i].details === null){
                idProduct = infoStuff[i].id
                if(infoStuff[i].type == 'услуга'){
                    console.log(infoStuff[i].costForOne)
                    price = infoStuff[i].costForOne
                } 
            }
        }

        
        var listProduct = document.querySelector('.listOfProducts')
        if (nameProduct == 'null'){
            listProduct.innerHTML += `<div class="containerForProduct">
        <div class="textForProduct">
            ${categoryProduct} <br>  Цена: ${price} рублей 
        </div>
    </div>`
        }
        else {
            listProduct.innerHTML += `<div class="containerForProduct">
        <div class="textForProduct">
            ${categoryProduct} <br> Детали: ${nameProduct} <br> Цена: ${price} рублей <br> Количество: ${countProduct}
        </div>
    </div>
    `
        }
    // <div class="containerForProduct" style="background-color: rgba(0,0,0,0.0); height: 30px; bottom: 0;"></div>`
    }) 
}

request.send()