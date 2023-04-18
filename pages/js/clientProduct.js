var request = new XMLHttpRequest()

request.open('POST', '/products', true)

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
        if(infoProducts[0]["products_found"]){
            for(let i = 1; i < infoProducts.length; i++){
                var textProduct = `<div class="containerProduct">
                <div class="textProduct">
                    ${infoProducts[i].category} <br> ${infoProducts[i].details} <br> ${infoProducts[i].cost_for_one } рублей 
                </div>
            </div>  <div class="containerForProduct" style="background-color: rgba(0,0,0,0.0); height: 30px; bottom: 0; width: 1px;"></div>`
                container.innerHTML += textProduct
            }
        }
    }
}

request.send()