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

        // for (let product = 2; product < infoStuff.length; product++){
        //     if(infoStuff[product].category == categoryProduct && infoStuff[product].type == nameProduct){
        //         console.log(infoStuff[product].costForOne)
        //         price = infoStuff[product].costForOne * Number(countProduct)
        //     }
        // }

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