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

    let product = []

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
            let item = {
                id: idProduct,
                category: categoryProduct,
                pr: price,
                details: '',
                count: 1
            }
            listProduct.innerHTML += `<div class="containerForProduct">
            <button class='deleteLesson'>&times;</button>
        <div class="textForProduct">
            ${categoryProduct} <br>  Цена: ${price} рублей 
        </div>
    </div>`
            product.push(item)
        }
        else {
            let item = {
                id: idProduct,
                category: categoryProduct,
                pr: price,
                details: nameProduct,
                count: Number(countProduct)
            }

            let info = {
                productId: idProduct,
                productAmount: countProduct
            }

            async function checkProduct(info){
                let response = await fetch("/checkAmount", {
                    method: 'POST',
                    headers: {
                      'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(info)
                });
                let res = await response.json()
                return res
            }
            
            let result = checkProduct(info)
            result.then((info) => {
                if(info.enoughAmount){
                    listProduct.innerHTML += `<div class="containerForProduct">
                    <button class='deleteLesson'>&times;</button>
                <div class="textForProduct">
                    ${categoryProduct} <br> Детали: ${nameProduct} <br> Цена: ${price} рублей <br> Количество: ${countProduct}
                </div>
            </div>
            `
                    product.push(item)
                } else {
                    alert(`Столько товаров, к сожалению неть, осталось: ${info.amountInStorage}`)
                }
            }
            )
        }


        var deleteLesson = document.getElementsByClassName("deleteLesson");
        for(let i = 0; i < deleteLesson.length; i++){
            deleteLesson[i].addEventListener('click',  function(e) {
                var parent = e.target.closest(".containerForProduct")

                let br = parent.querySelectorAll('br')
                console.log(br)
                let text = parent.querySelector(".textForProduct").innerHTML
                console.log(text)
                if(br.length == 3){
                    let category = text.split('<br>')[0].trim()
                    let details = text.split('<br>')[1].split(':')[1].trim()
                    
                    for(let i = 0; i < product.length; i++){
                        if(product[i].category == category && product[i].details == details){
                            product.splice(i, 1)
                        }
                    }
                } else if(br.length == 1){
                    let category = text.split('<br>')[0].trim()

                    for(let i = 0; i < product.length; i++){
                        if(product[i].category == category){
                            product.splice(i, 1)
                        }
                    }
                }

                parent.closest(".containerForProduct").remove();
            }, false)
        }
    })

    
    document.querySelector('.arrange').addEventListener('click', (listProduct) => {
        let nameDeceased = document.getElementById('nameDeceased').value
        let dateOfDeath = document.getElementById('dateOfDeath').value
        let dataPassport = document.getElementById('dataPassport').value
        let clientName = document.getElementById('clientName').value
        let phoneClient = document.getElementById('phoneClient').value
        let address = document.getElementById('address').value

        let masInfo = [nameDeceased, dateOfDeath, dataPassport, clientName, phoneClient, address]
        if(masInfo.every(element => element !== '')){
            let manID = JSON.parse(sessionStorage.getItem('managerID'))
            let masInfo = {"nameDeceased": nameDeceased, "dateOfDeath": dateOfDeath, "dataPassport": dataPassport, "clientName": clientName, "phoneClient": phoneClient, "address": address, "managerID": manID}
            sessionStorage.setItem('info', JSON.stringify(masInfo))
            sessionStorage.setItem('product', JSON.stringify(product))
            window.location.href = '/pages/managerEstimate.html'
        } else alert('Заполните все поля!')
    })

}

request.send()