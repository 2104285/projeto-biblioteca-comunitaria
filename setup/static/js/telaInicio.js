window.onload = function () {
    async function getData(){
        const cell = document.getElementById("qtyLivroDisponivel")
        const consult = await fetch("http://127.0.0.1:8000/json/getQtyLivroDisponivel");      //variavel aguarda o retorno da url
        const data = await consult.json(); //variavel aguarda o arquivo json com todas informações
        cell.innerText = data["Data"]
    }
    getData()
}