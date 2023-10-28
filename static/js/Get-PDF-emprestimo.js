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
        var container = document.getElementById('gerar-pdf'); // Replace with your actual container ID
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

function getChildNodes(element) {
    var list = []
    list.push(element);

    let child = element.firstChild;
    while (child) {
        if (child.nodeType === 1) {
            getChildNodes(child);
        }
        child = child.nextSibling;
    }
    return list
};

function openFormPDF(){
    console.log("abrir form!")
    //make each element of element opacity 1
    var form = document.getElementById("gerar-pdf");
    form.style.display = "block";
    console.log("abrir form concluido!")
    abriu = true
};

function closeFormPDF(){
    console.log("Forms fechado!")
    var form = document.getElementById("gerar-pdf");
    form.style.display = "none";
};
