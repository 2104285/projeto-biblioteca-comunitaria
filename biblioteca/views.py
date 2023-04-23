from django.shortcuts import render
from django.core.paginator import Paginator
from biblioteca.models import TbLeitor

def index(request):
    return render(request, 'biblioteca/wp1_login.html')

def inicio(request):
    return render(request,'biblioteca/wp2_inicio.html')

def leitor_geral(request):
    leitor = TbLeitor.objects.all()
    #filtros
    id = ""
    telefone = ""
    nome = ""
    if "id" in request.GET:
        id = request.GET['id']
        if id:
            leitor = leitor.filter(leitor_id__icontains=id)
    if "nome" in request.GET:
        nome = request.GET['nome']
        if nome:
            leitor = leitor.filter(nome__icontains=nome)
    if "telefone" in request.GET:
        telefone = request.GET['telefone']
        if telefone:
            leitor = leitor.filter(telefone__icontains=str(telefone))
    #paginação
    paginator = Paginator(leitor, 5)  # Show 5 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'biblioteca/wp31_leitor-geral.html',
                  {"leitor": page_obj, "id":id,"nome":nome,"telefone":telefone})

def cadastro_leitor(request):
    if request.method == "POST":
        cadastro = TbLeitor()
        cadastro.nome = request.POST["nome"]
        cadastro.endereco = request.POST["endereco"]
        cadastro.bairro = request.POST["bairro"]
        cadastro.ddd = request.POST["ddd"]
        cadastro.telefone = request.POST["telefone"]
        cadastro.save()
        return render(request, 'biblioteca/wp32_novo-leitor.html')
    else:
        return render(request, 'biblioteca/wp32_novo-leitor.html')

def acervo_geral(request):
    return render(request, 'biblioteca/wp41_acervo-geral.html')

def cadastro_acervo(request):
    return render(request, 'biblioteca/wp42_novo-livro.html')

def emprestimo(request):
    return render(request, 'biblioteca/wp51_status-geral.html')

def cadastro_emprestimo(request):
    return render(request, 'biblioteca/wp52_novo-emprestimo.html')