from django.shortcuts import render, get_object_or_404, HttpResponse
from django.core.paginator import Paginator
from biblioteca.models import TbLeitor, TbLivro, TbEmprestimo
import datetime as dt

def index(request):
    return render(request, 'biblioteca/wp1_login.html')

def inicio(request):
    qty_livro = TbLivro.objects.all().count()
    qty_emprestado = TbEmprestimo.objects.all().filter(data_devolucao = None).count()
    #qty_livro_emprestado = TbLivro.objects.all().filter(status="Emprestado").count()
    return render(request,'biblioteca/wp2_inicio.html',{"qty_livro": qty_livro, 
                                                        "qty_emprestado": qty_emprestado,
                                                        "qty_livro_emprestado": None})

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
        cadastro.ativo = request.POST["ativo"]
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
        leitor.ativo = request.POST["ativo"]
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
    if request.method == "POST":
        livro = TbLivro()
        livro.tombo = request.POST["tombo"]
        livro.titulo = request.POST["titulo"]
        livro.autor = request.POST["autor"]
        livro.classificacao = request.POST["classificacao"]
        livro.na = request.POST["na"]
        livro.save()
        return render(request, 'biblioteca/wp42_novo-livro.html')
    else:
        return render(request, 'biblioteca/wp42_novo-livro.html')

def update_acervo(request,id):
    if request.method == "POST":
        livro = TbLivro.objects.get(pk=id)
        livro.tombo = request.POST["tombo"]
        livro.titulo = request.POST["titulo"]
        livro.autor = request.POST["autor"]
        livro.classificacao = request.POST["classificacao"]
        livro.na = request.POST["na"]
        livro.save()
        return render(request, 'biblioteca/wp43_update_acervo.html',{"livro":livro})
    else:
        livro = TbLivro.objects.all()
        livro = get_object_or_404(livro, pk=id)
        return render(request, 'biblioteca/wp43_update_acervo.html',{"livro":livro})

def emprestimo(request):
    if request.method == "POST" and "add_14_days" in request.POST:
        emprestimo = TbEmprestimo.objects.get(pk = request.POST["id"])
        emprestimo.data_devolucao_prevista = emprestimo.data_devolucao_prevista + dt.timedelta(14)
        emprestimo.save()
    emprestimo = TbEmprestimo.objects.all()
    leitor_id = ""
    tombo = ""
    data_emprestimo = ""
    data_devolucao = ""
    entrega = ""
    if "leitor_id" in request.GET:
        leitor_id = request.GET["leitor_id"]
        if leitor_id != "":
            emprestimo = emprestimo.filter(leitor__leitor_id__icontains=leitor_id)
    if "tombo" in request.GET:
        tombo = request.GET["tombo"]
        if tombo != "":
           emprestimo =  emprestimo.filter(livro__tombo__icontains=tombo)
    if "data_emprestimo" in request.GET:
        data_emprestimo = request.GET["data_emprestimo"]
        if data_emprestimo != "":
            emprestimo = emprestimo.filter(data_emprestimo__icontains=data_emprestimo)
    if "data_devolucao" in request.GET:
        data_devolucao = request.GET["data_devolucao"]
        if data_devolucao != "":
            emprestimo = emprestimo.filter(data_devolucao__icontains=data_devolucao)
    if "entrega" in request.GET:
        entrega = request.GET["entrega"]
        if entrega == "Ativo":
            emprestimo = emprestimo.exclude(data_devolucao=None)
        elif entrega == "Desativo":
            emprestimo = emprestimo.filter(data_devolucao=None).order_by("data_emprestimo")

    paginator = Paginator(emprestimo, 5)  # Show 5 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'biblioteca/wp51_status-geral.html',
                  {"emprestimo": page_obj,
                   "leitor_id":leitor_id,
                   "tombo": tombo,
                   "data_emprestimo":data_emprestimo,
                   "entrega":entrega} )

def cadastro_emprestimo(request):
    if request.method == "POST":
        emprestimo = TbEmprestimo()
        leitor = TbLeitor(leitor_id = request.POST["leitor_id"])
        emprestimo.leitor = leitor
        try:
            livro = TbLivro.objects.get(tombo=int(request.POST["tombo"]))
        except:
            return HttpResponse("<p>Atenção! O tombo do livro não foi registrado!</p>")
        if livro.status == "Emprestado":
            return HttpResponse("<p>Atenção! o livro já está emprestado!</p>")
        else:
            emprestimo.livro = livro
            emprestimo.data_emprestimo = request.POST["data_emprestimo"]
            emprestimo.data_devolucao_prevista = request.POST["data_devolucao_prevista"]
            emprestimo.obs_emprestimo = request.POST["obs_emprestimo"]
            emprestimo.save()
            return render(request, 'biblioteca/wp52_novo-emprestimo.html')
    else:
        leitor = TbLeitor.objects.all().order_by("nome")
        return render(request, 'biblioteca/wp52_novo-emprestimo.html',{"leitor":leitor})
    
def emprestimo_edit(request,id):
    
    if request.method == "POST":
        emprestimo = TbEmprestimo.objects.all()
        emprestimo = get_object_or_404(emprestimo,pk=id)
        emprestimo.data_devolucao_prevista = request.POST["data_devolucao_prevista"]
        if request.POST["data_devolucao"] != "":
            emprestimo.data_devolucao = request.POST["data_devolucao"]
        else:
            emprestimo.data_devolucao = None
        emprestimo.obs_devolucao = request.POST["obs_devolucao"]
        emprestimo.save()
        emprestimo = TbEmprestimo.objects.all()
        emprestimo = get_object_or_404(emprestimo,pk=id)
        return render(request, 'biblioteca/wp52_edit-emprestimo.html', {"emprestimo":emprestimo})
    else:
        emprestimo = TbEmprestimo.objects.get(pk = id)
        return render(request, 'biblioteca/wp52_edit-emprestimo.html', {"emprestimo":emprestimo})