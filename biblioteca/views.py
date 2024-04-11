from django.shortcuts import render, get_object_or_404, HttpResponse
from django.core.paginator import Paginator
from biblioteca.models import TbLeitor, TbLivro, TbEmprestimo
import datetime as dt
from django.shortcuts import render
from reportlab.pdfgen import canvas
import pandas as pd
from django.views.decorators.csrf import csrf_exempt

def credito(request):
    return render(request, 'biblioteca/wp53_credito.html')

def index(request):
    return render(request, 'biblioteca/wp1_login.html')

@csrf_exempt
def inicio(request):
    qty_livro = TbLivro.objects.filter(visivel=True)
    emprestimo = TbEmprestimo.objects.all()
    qty_emprestado = emprestimo.filter(data_devolucao = None).count()
    qty_emprestimo_total = emprestimo.count()
    leitor = TbLeitor.objects.all().filter(visivel=True)
    qty_leitor = leitor.count()

    df_emprestimo = pd.DataFrame(TbEmprestimo.objects.all().values())
    try:
        qty_leitor_emprestimo = df_emprestimo["leitor_id"].unique().size
    except:
        qty_leitor_emprestimo = 0
    
    if qty_emprestimo_total == 0:
        display_dashboard = None
    else:
        display_dashboard = True

    return render(request,'biblioteca/wp2_inicio.html',{"qty_livro": qty_livro.count(), 
                                                        "qty_emprestado": qty_emprestado,
                                                        "qty_disponivel": qty_livro.count() - qty_emprestado,
                                                        "qty_leitor": qty_leitor,
                                                        "qty_leitor_emprestimo": qty_leitor_emprestimo,
                                                        "qty_emprestimo_total": qty_emprestimo_total,
                                                        "display_dashboard": display_dashboard})

@csrf_exempt
def leitor_geral(request):
    leitor = TbLeitor.objects.filter(visivel = True)
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
    paginator = Paginator(leitor, 100)  # Show 5 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'biblioteca/wp31_leitor-geral.html',
                  {"leitor": page_obj, "id":id,"nome":nome,"telefone":telefone})

@csrf_exempt
def generate_pdf_leitor(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="leitor.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Define the width and height of each row in the table
    row_height = 20
    column_width = 80

    # Define the data to be printed in the table
    data = [
        ['ID','Name', 'telefone','Bairro'],
    ]
    for obj in TbLeitor.objects.all().filter(visivel=True).order_by('nome'):
        data.append([obj.leitor_id, obj.nome, obj.telefone, obj.bairro])

    # Draw the table
    x = 50
    y = 800
    for row in data:
        item_num = 1
        for item in row:
            if item_num == 1:
                column_width = 50
            elif item_num == 2:
                column_width = 200
            else:
                column_width = 80
            p.drawString(x, y, str(item)[0:30])
            item_num += 1
            x += column_width
        x = 50
        y -= row_height
        if y <= 50: # add another page
            y = 750
            p.showPage()

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    return response


@csrf_exempt
def cadastro_leitor(request):
    if request.method == "POST":
        cadastro = TbLeitor()
        cadastro.nome = request.POST["nome"]
        cadastro.cep = request.POST["cep"]
        cadastro.endereco = request.POST["endereco"]
        cadastro.numero = request.POST["numero"]
        cadastro.bairro = request.POST["bairro"]
        cadastro.cidade = request.POST["cidade"]
        cadastro.estado = request.POST["uf"]
        cadastro.ddd = request.POST["ddd"]
        cadastro.telefone = request.POST["telefone"]
        cadastro.ativo = request.POST["ativo"]
        cadastro.save()
        return render(request, 'biblioteca/wp32_novo-leitor.html')
    else:
        return render(request, 'biblioteca/wp32_novo-leitor.html')

@csrf_exempt
def update_leitor(request,id):
    if request.method == "POST":
        leitor = TbLeitor.objects.get(pk=id)
        leitor.nome = request.POST["nome"]
        leitor.cep = request.POST["cep"]
        leitor.endereco = request.POST["endereco"]
        leitor.numero = request.POST["numero"]
        leitor.bairro = request.POST["bairro"]
        leitor.cidade = request.POST["cidade"]
        leitor.estado = request.POST["uf"]
        leitor.ddd = request.POST["ddd"]
        leitor.telefone = request.POST["telefone"]
        leitor.ativo = request.POST["ativo"]
        leitor.save()
        return render(request, 'biblioteca/wp33_update-leitor.html',{"leitor":leitor})
    else:
        leitor = TbLeitor.objects.all()
        leitor = get_object_or_404(leitor, pk=id)
        return render(request, 'biblioteca/wp33_update-leitor.html',{"leitor":leitor})

@csrf_exempt
def remove_visility_leitor(request,id):
    leitor = TbLeitor.objects.filter(leitor_id=id).get()
    leitor.visivel = False
    leitor.save()
    return leitor_geral(request)

@csrf_exempt
def acervo_geral(request):
    livro = TbLivro.objects.filter(visivel=True)
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
    paginator = Paginator(livro, 100)  # Show 5 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'biblioteca/wp41_acervo-geral.html',
                  {"livro":page_obj,"tombo":tombo,"nome": titulo, "autor": autor,"classificacao": classificacao})


@csrf_exempt
def cadastro_acervo(request):
    if request.method == "POST":
        livro = TbLivro()
        #livro.tombo = request.POST["tombo"] #alterar informação para inserir id no mesmo lugar do tombo
        livro.titulo = request.POST["titulo"]
        livro.autor = request.POST["autor"]
        livro.classificacao = request.POST["classificacao"]
        livro.na = request.POST["na"]
        livro.save()
        return render(request, 'biblioteca/wp42_novo-livro.html')
    else:
        return render(request, 'biblioteca/wp42_novo-livro.html')

@csrf_exempt
def update_acervo(request,id):
    if request.method == "POST":
        livro = TbLivro.objects.get(pk=id)
        #livro.tombo = request.POST["tombo"]
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

@csrf_exempt
def remove_visility_acervo(request,id):
    leitor = TbLivro.objects.get(pk=id)
    leitor.visivel = False
    leitor.save()
    return inicio(request)

@csrf_exempt
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
        if entrega != "":
            for x in emprestimo:
                if x.status != entrega:
                    emprestimo = emprestimo.exclude(id=x.id)
        #if entrega == "Ativo":
        #    emprestimo = emprestimo.exclude(data_devolucao=None)
        #elif entrega == "Desativo":
        #    emprestimo = emprestimo.filter(data_devolucao=None).order_by("data_emprestimo")

    paginator = Paginator(emprestimo, 100)  # Show 5 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'biblioteca/wp51_status-geral.html',
                  {"emprestimo": page_obj,
                   "leitor_id":leitor_id,
                   "tombo": tombo,
                   "data_emprestimo":data_emprestimo,
                   "entrega":entrega} )

@csrf_exempt
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
        livro = TbLivro.objects.all().order_by("titulo")
        return render(request, 'biblioteca/wp52_novo-emprestimo.html',{"leitor":leitor, "livro":livro})

@csrf_exempt
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
    

    
