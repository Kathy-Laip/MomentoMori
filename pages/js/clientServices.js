var request = new XMLHttpRequest()

request.open('POST', '/services', true)

const p = new Promise((res, rej) => {
    request.onload = () => {
        var dataAboutServices = request.responseText
        res(dataAboutServices)
    }
}).then(dataAboutServices => {
    getProducts(dataAboutServices)
})

async function getProducts(dataAboutServices){
    var infoServices = JSON.parse(dataAboutServices)
    console.log(infoServices)

    insertINtoProducts(infoServices)

    function insertINtoProducts(infoServices){
        var container = document.getElementById('services')
        if(infoServices[0].services_found){
            for(let i = 1; i < infoServices.length; i++){
                var textServices = `<div class="containerServices">
                <div class="textServices">
                ${infoServices[i].category} <br> ${infoServices[i].cost_for_one} рублей
                </div>
            </div>  <div class="containerForProduct" style="background-color: rgba(0,0,0,0.0); height: 30px; bottom: 0;"></div>`
                container.innerHTML += textServices
            }
        }
    }
}

request.send()