from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from biblioteca.models import TbLeitor, TbLivro

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

def update_leitor(request,id):
    if request.method == "POST":
        leitor = TbLeitor.objects.get(pk=id)
        leitor.nome = request.POST["nome"]
        leitor.endereco = request.POST["endereco"]
        leitor.bairro = request.POST["bairro"]
        leitor.ddd = request.POST["ddd"]
        leitor.telefone = request.POST["telefone"]
        leitor.save()
        return render(request, 'biblioteca/wp33_update-leitor.html',{"leitor":leitor})
    else:
        leitor = TbLeitor.objects.all()
        leitor = get_object_or_404(leitor, pk=id)
        return render(request, 'biblioteca/wp33_update-leitor.html',{"leitor":leitor})

def acervo_geral(request):
    livro = TbLivro.objects.all()
    #filtros
    titulo = ""
    autor = ""
    classificacao = ""
    tombo = ""
    if "tombo" in request.GET:
        tombo = request.GET['tombo']
        if tombo:
            livro = livro.filter(tombo__icontains=tombo)
    if "titulo" in request.GET:
        titulo = request.GET['titulo']
        if titulo:
            livro = livro.filter(titulo__icontains=titulo)
    if "autor" in request.GET:
        autor = request.GET['autor']
        if autor:
            livro = livro.filter(autor__icontains=autor)
    if "classificacao" in request.GET:
        classificacao = request.GET['classificacao']
        if classificacao:
            livro = livro.filter(classificacao__icontains=classificacao)
    #paginação
    paginator = Paginator(livro, 5)  # Show 5 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'biblioteca/wp41_acervo-geral.html',
                  {"livro":page_obj,"tombo":tombo,"nome": titulo, "autor": autor,"classificacao": classificacao})

def cadastro_acervo(request):
    return render(request, 'biblioteca/wp42_novo-livro.html')

def emprestimo(request):
    return render(request, 'biblioteca/wp51_status-geral.html')

def cadastro_emprestimo(request):
    return render(request, 'biblioteca/wp52_novo-emprestimo.html')