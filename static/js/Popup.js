
    function fecharPopup() {
        document.getElementById("popup-box").style.display = "none";
    }

    // Adicione um evento de clique ao botão "Salvar"
    document.getElementById("botaoSalvar").addEventListener("click", function(event) {
        // Impedir o envio padrão do formulário
        event.preventDefault();
        
        // Exiba o popup
        document.getElementById("popup-box").style.display = "flex";
    });

