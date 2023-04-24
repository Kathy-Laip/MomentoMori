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
            for(let i = 1; i < infoStuff.length; i++){
                var textProduct = `<option value="${infoStuff[i].category}">${infoStuff[i].category}</option>`
                container.innerHTML += textProduct
            }
        }
    }

    document.getElementById('category').addEventListener('change', function(){
        let productChange = document.getElementById('product')
        productChange.innerHTML = '<option value=""></option>'
        let type = this.value

        var productType = infoStuff.stuff.filter(obj => obj.type === type)
        for(let pos of productType){
            if(pos.description === null){
                continue
            } else {
                productChange.innerHTML += `<option value="${pos.description}">${pos.description}</option>`
            }
        }
    })

    document.querySelector('.addProduct').addEventListener('click', function(){
        var nameProduct = document.getElementById('product').value
        var categoryProduct = document.getElementById('category').value
        var countProduct = document.getElementById('count').value
        var btnOF = document.querySelector('.arrange')
        var price

        for (let product of infoStuff.stuff){
            if(product.type == categoryProduct && product.description == nameProduct){
                price = product.cost * Number(countProduct)
            }
        }

        var listProduct = document.querySelector('.listOfProducts')
        listProduct.innerHTML += `<div class="containerForProduct">
        <div class="textForProduct">
            ${categoryProduct} <br> ${nameProduct} <br> Цена: ${price} рублей <br> Количество: ${countProduct}
        </div>
    </div>
        <div class="containerForProduct" style="background-color: rgba(0,0,0,0.0); height: 30px; bottom: 0;"></div>`
    }) 
}

request.send()