function confirmDelete() {
    var id = document.getElementById("id").value;
    var result = confirm("Tem certeza que quer excluir o usuário?");
    if (result) {
        window.location.replace("http://127.0.0.1:8000/leitor-geral/delete/" + id); // Replace with the actual delete link
    } else {
        // User clicked "Cancel", do nothing or redirect back to the original page if desired
    }

}
