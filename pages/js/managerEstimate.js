let products = JSON.parse(sessionStorage.getItem('product'))
let table = document.querySelector('.estimate')
var total = products.map(obj => obj.pr).reduce((a,b) => a+b)
// .reduce((a,b) => a+b)

for(let i = 0; i < products.length; i++){
    let text = `
    <tr>
        <th>${products[i].category} ${products[i].details}</th>
        <th>${products[i].pr} рублей</th>
    </tr>
    `
    table.innerHTML += text
}

console.log(total)
let text = `
<tr>
    <th colspan="2" style="text-align: right; right: 5%; position: relative;">Итоговая цена: ${total} рублей</th>
</tr>
`
table.innerHTML += text