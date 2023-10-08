var abriu = false;
window.onload = function() {
    
    let elementsList = [];

    function getChildNodes(element) {
        elementsList.push(element);

        let child = element.firstChild;
        while (child) {
            if (child.nodeType === 1) {
                getChildNodes(child);
            }
            child = child.nextSibling;
        }
    };

    document.addEventListener('click', function(event) {
        console.log("Clicou!")
        var container = document.getElementById('deleteLivro'); // Replace with your actual container ID
        getChildNodes(container)
        //if (event.target !== container) {
        if (!elementsList.includes(event.target)) {
            if(container.style.display === 'block' && abriu === false){
                container.style.display = 'none'
            }else{
                abriu = false
            }
        }
        
    });
}

async function confirmDelete() {
    var id = document.getElementById("id").value;
    const consulta = await fetch("http://127.0.0.1:8000/json/getLivroStatusByID/" + id);      //variavel aguarda o retorno da url
    const dados = await consulta.json(); //variavel aguarda o arquivo json com todas informações
    console.log(dados)
    console.log(dados["Data"])
    if(dados["Data"] === "Disponível"){
        window.location.replace("http://127.0.0.1:8000/acervo-geral/delete/" + id);} // Replace with the actual delete link
    else{
        alert("O livro está emprestado, e portanto não pode ser excluído!");
    }
};

function openFormExclude(){
    console.log("abrir form!")
    var form = document.getElementById("deleteLivro");
    form.style.display = "block";
    console.log("abrir form concluido!")
    abriu = true
};

function closeFormExclude(){
    console.log("Forms fechado!")
    var form = document.getElementById("deleteLivro");
    form.style.display = "none";
};
