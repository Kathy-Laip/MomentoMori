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


// функция получения информация о всех услугах
// также размещает информацию об услугах на страницу и формирует все функции, связанные с услугами
async function getProducts(dataAboutServices){
    var infoServices = JSON.parse(dataAboutServices)
    console.log(infoServices)

    insertINtoProducts(infoServices)


    // вставка данных об услугах на страницу с услугами
    function insertINtoProducts(infoServices){
        var container = document.getElementById('services')
        if(infoServices[0].servicesFound){
            for(let i = 1; i < infoServices.length; i++){
                var textServices = `<div class="containerServices">
                <div class="textServices">
                ${infoServices[i].category} <br> ${infoServices[i].costForOne} рублей
                </div>
            </div>  <div class="containerForProduct" style="background-color: rgba(0,0,0,0.0); height: 30px; bottom: 0;"></div>`
                container.innerHTML += textServices
            }
        }
    }
}

request.send()