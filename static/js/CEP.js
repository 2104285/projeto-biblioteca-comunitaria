//'use restrict'; //modo estrito - aumenta o rigor do código, deixando mais seguro e consistente 
window.onload = function () {
    var url = window.location.href
    if (url.includes("delete")){
        window.location.replace("http://127.0.0.1:8000/leitor-geral")
    }

    const limpaform = (endereco) =>{        //variavel limpa formulario se cep for incorreto
        document.getElementById('logradouro').value = '';  //zera o preenchimento dos campos
        document.getElementById('bairro').value = '';
        document.getElementById('localidade').value = '';
        document.getElementById('uf').value = '';
    }

    const preencherform = (endereco) =>{        //variavel recebe os dados do json
        document.getElementById('logradouro').value = endereco.logradouro;  //preenche cada campo específico
        document.getElementById('bairro').value = endereco.bairro;
        document.getElementById('localidade').value = endereco.localidade;
        document.getElementById('uf').value = endereco.uf;
    }

    const pesquisarCep = async() => {
        const cep = document.getElementById('cep').value;   //variavel pega o valor preenchido no campo cep
        const url = `https://viacep.com.br/ws/${cep}/json/`;

        const dados = await fetch(url);      //variavel aguarda o retorno da url
        const endereco = await dados.json(); //variavel aguarda o arquivo json com todas informações

        if (endereco.hasOwnProperty('erro')) {   //se o cep informado der erro na api
                alert("CEP não encontrado");         //retorna o alerta para o usuário
                limpaform(endereco);
        }

        else{       //senao prossegue normal o preenchimnento
                preencherform(endereco);
        } 
    }

    document.getElementById('cep')      //pegue o elemento do id "cep"
            .addEventListener('focusout', pesquisarCep); //quando sair do foco pesquiseCep
}