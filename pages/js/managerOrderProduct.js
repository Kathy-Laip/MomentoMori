const listProduct = document.getElementById('listOrderProduct')


//добавление нового поля для заказа товара
function addLineForProduct(){
    const innerForOneInputs = `
    <div class="containerForProductInList">
            <input type="text" class="categoryInput">
            <input type="text" class="nameProduct">
            <input type="text" class="countProduct">
    </div>
    `
    listProduct.innerHTML += innerForOneInputs
}

const btnOrder = document.querySelector('.btnOrder')

let listProducts = []

//слушатель на нажатии заказа товаров, подготовка даннхы, отправка данных на сервер
btnOrder.addEventListener('click', function(){
    var list = listProduct.querySelectorAll('.containerForProductInList')
    for(let l of list){
        let item = {
            category: l.querySelector('.categoryInput').value,
            details: l.querySelector('.nameProduct').value,
            count: l.querySelector('.countProduct').value
        }
        listProducts.push(item)
    }


    //отправка данных о всех товара, которые будут заказывать
    async function sendProducts(){
        let sendInfo = {
            "info": listProducts,
        }
        let response = await fetch('/addNewProducts', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(sendInfo)
        });
        let result = await response.json()

        if (result.addedFlag == true){
            alert ('Заказ оформлен!')
            window.location.href = '/pages/managerStorage.html'
        } else alert('Ошибка отправки данных!')
    }

    // sendProducts()
})