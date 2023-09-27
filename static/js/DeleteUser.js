var abriu = false;
window.onload = function() {
    document.addEventListener('click', function(event) {
        console.log("Clicou!")
        var container = document.getElementById('deleteuser'); // Replace with your actual container ID
    
        if (event.target !== container) {
            if(container.style.display === 'block' && abriu === false){
                container.style.display = 'none'
            }else{
                abriu = false
            }
        }
    });
}

function confirmDelete() {
    var id = document.getElementById("id").value;
    window.location.replace("http://127.0.0.1:8000/leitor-geral/delete/" + id); // Replace with the actual delete link
};

function openFormExclude(){
    console.log("abrir form!")
    var form = document.getElementById("deleteuser");
    form.style.display = "block";
    console.log("abrir form concluido!")
    abriu = true
};

function closeFormExclude(){
    console.log("Forms fechado!")
    var form = document.getElementById("deleteuser");
    form.style.display = "none";
};
