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


// функция получения информация о всех товарах
// также размещает информацию о товарах на страницу и формирует все функции, связанные с товарами
async function getProducts(dataAboutProduct){
    var infoProducts = JSON.parse(dataAboutProduct)
    console.log(infoProducts)

    insertINtoProducts(infoProducts)

    // вставка данных о товаре на страницу
    function insertINtoProducts(infoProducts){
        var container = document.getElementById('products')
        console.log(infoProducts)
        if(infoProducts[0].productsFound){
            for(let i = 1; i < infoProducts.length; i++){
                console.log(infoProducts[i])
                var textProduct = `<div class="containerProduct">
                <button class='deleteProduct'>&times;</button>
                <div class="textProduct">
                    ${infoProducts[i].category} <br> 
                    ${infoProducts[i].details} <br> 
                    ${infoProducts[i].costForOne } рублей <br> 
                    Количество: ${infoProducts[i].amount}
                </div>
            </div>  <div class="containerForProduct" style="background-color: rgba(0,0,0,0.0); height: 30px; bottom: 0; width: 1px;"></div>`
                container.innerHTML += textProduct
            }
        }
    }


    var deleteLesson = document.getElementsByClassName("deleteProduct");
    for(let i = 0; i < deleteLesson.length; i++){
        //слушатель на событие нажатия кнопки удаления товара
        deleteLesson[i].addEventListener('click',  function(e) {
            var parent = e.target.closest(".containerProduct")
            var text = parent.querySelector('.textProduct').innerHTML.split('<br>').slice(0,2).map(el => el.trim())
            async function deleteProduct(){
                let response = await fetch('/deleteProduct', {
                    method: 'POST',
                    body: JSON.stringify(text),
                    headers: {
                        'Accept' : 'application/json',
                        'Content-Type' : 'appliction/json'
                    }
                }) 
                let result = await response.json()

                if(result.deletedFlag == true){
                    parent.closest('.containerProduct').remove();
                } else alert('Что-то пошло нет так...')
            }
            deleteProduct()
        }, false)
    }

    let btnAdd = document.querySelector('.addPr')
    let formAddProduct = document.getElementById('formAdd')

    // нажатие на открытие формы для заполнения данных о новом товаре и его добавление
    btnAdd.addEventListener('click', () => {
        formAddProduct.classList.add('open');
    });

    let closeAddProduct = document.querySelector('.closeAddProduct')
    closeAddProduct.addEventListener('click', () => {
        formAddProduct.classList.remove('open');
    })


    let btnAddProduct = document.querySelector('.btnAddProductToDB') 
    //добавление нового товара, отправка данных на сервер
    btnAddProduct.addEventListener('click', () => {
        let categorAddProduct = document.getElementById('categorAddProduct').value
        let detailsAddProduct = document.getElementById('detailsAddProduct').value
        let costAddProduct = document.getElementById('costAddProduct').value
        let countAddProduct = document.getElementById('countAddProduct').value
        let info = [categorAddProduct, detailsAddProduct, costAddProduct, countAddProduct]
        async function addProduct(){
            if(info === []){
                alert('Пустые поля, введите данные!')
            }
            let response = await fetch('/addProduct', {
                method: 'POST',
                body: JSON.stringify(info),
                headers: {
                    'Accept' : 'application/json',
                    'Content-Type' : 'appliction/json'
                }
            }) 
            let result = await response.json()

            if(result.addedFlag == true){
                formAddProduct.style.display = 'none'
                alert('Товар успешно добавлен!')
                info = []
                setTimeout(() => {
                    window.location.href = '/pages/managerStorage.html'
                }, 1000)
            } else{
                formAddProduct.style.display = 'none'
                alert('Что-то пошло нет так...')
                info = []
            } 
        }
        addProduct()
    })


}

request.send()