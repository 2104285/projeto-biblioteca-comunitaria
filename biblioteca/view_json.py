from django.forms.models import model_to_dict
from django.http import JsonResponse
from biblioteca.models import TbLeitor, TbLivro, TbEmprestimo

def json_leitor(request,id):
    try:
        leitor = TbLeitor.objects.get(pk=id)
        return JsonResponse({"Data":model_to_dict(leitor)})
    except:
        return JsonResponse({"Data": None})
    
def json_get_emprestimo_by_leitorId(request,id):
    try:
        data = []
        emprestimo = TbEmprestimo.objects.filter(leitor=id)
        for emp in emprestimo:
            data.append(model_to_dict(emp))
        return JsonResponse({"Data": data})
    except:
        return JsonResponse({"Data": None})

def json_get_livro_status_by_id(request,id):
    try:
        livro = TbLivro.objects.get(pk=id)
        
        return JsonResponse({"Data":livro.status})
    except:
        return JsonResponse({"Data": None})

def json_get_livros_dispoiveis(request):
    qty_livro = TbLivro.objects.filter(visivel=True)
    qty_livro_disponivel_number = 0
    for livro in qty_livro:
        if livro.status == "Disponível":
            qty_livro_disponivel_number += 1
    return JsonResponse({"Data": qty_livro_disponivel_number})