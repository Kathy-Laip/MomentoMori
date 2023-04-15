const listProduct = document.getElementById('listOrderProduct')

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