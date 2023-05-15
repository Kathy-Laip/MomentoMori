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
                <button class='deleteServices'>&times;</button>
                <div class="textServices">
                ${infoServices[i].category} <br> ${infoServices[i].costForOne} рублей
                </div>
            </div>  <div class="containerForProduct" style="background-color: rgba(0,0,0,0.0); height: 30px; bottom: 0;"></div>`
                container.innerHTML += textServices
            }
        }
    }


    let btnAddServices = document.querySelector('.addServices')
    let formAddServices = document.getElementById('formServices')

    // нажатие на открытие формы для заполнения данных о новой услуги и его добавление
    btnAddServices.addEventListener('click', () => {
        formAddServices.classList.add('open');
    });

    let closeAddServices = document.querySelector('.closeAddServices')
    closeAddServices.addEventListener('click', () => {
        formAddServices.classList.remove('open');
    })

    let btnAddProduct = document.querySelector('.btnAddServicesToDB') 
    //добавление новой услуги, отправка данных на сервер
    btnAddProduct.addEventListener('click', () => {
        let addServices = document.getElementById('addServices').value
        let addServicesCost = document.getElementById('addServicesCost').value
        let info = [addServices, addServicesCost]
        async function addServicesToDB(){
            if(info === []){
                alert('Пустые поля, введите данные!')
            }
            let response = await fetch('/addServices', {
                method: 'POST',
                body: JSON.stringify(info),
                headers: {
                    'Accept' : 'application/json',
                    'Content-Type' : 'appliction/json'
                }
            }) 
            let result = await response.json()

            if(result.addedFlag == true){
                formAddServices.style.display = 'none'
                alert('Товар успешно добавлен!')
                info = []
                setTimeout(() => {
                    window.location.href = '/pages/managerServices.html'
                }, 1000)
            } else{
                formAddServices.style.display = 'none'
                alert('Что-то пошло нет так...')
                info = []
            } 
        }
        addServicesToDB()
    })


    // <div class="containerServices">
    //             <button class='deleteServices'>&times;</button>
    //             <div class="textServices">
    //             ${infoServices[i].category} <br> ${infoServices[i].costForOne} рублей
    //             </div>
    //         </div>
    var deleteLesson = document.getElementsByClassName("deleteServices");
    for(let i = 0; i < deleteLesson.length; i++){
        //слушатель на событие нажатия кнопки удаления товара
        deleteLesson[i].addEventListener('click',  function(e) {
            var parent = e.target.closest(".containerServices")
            var text = parent.querySelector('.textServices').innerHTML.split(' <br>').map(el => el.trim())
            text[1] = text[1].split(' ')[0]
            async function deleteProduct(){
                let response = await fetch('/deleteServices', {
                    method: 'POST',
                    body: JSON.stringify(text),
                    headers: {
                        'Accept' : 'application/json',
                        'Content-Type' : 'appliction/json'
                    }
                }) 
                let result = await response.json()

                if(result.deletedFlag == true){
                    parent.closest('.containerServices').remove();
                } else alert('Что-то пошло нет так...')
            }
            deleteProduct()
        }, false)
    }
}

request.send()