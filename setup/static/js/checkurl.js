window.onload = function () {
    var url = window.location.href
    if (url.includes("delete")){
        window.location.replace("http://127.0.0.1:8000/leitor-geral")
    }
}