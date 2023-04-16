from django.shortcuts import render

def index(request):
    return render(request, 'biblioteca/wp1_login.html')

def inicio(request):
    return render(request,'biblioteca/wp2_inicio.html')

def leitor_geral(request):
    return render(request,'biblioteca/wp31_leitor-geral.html')

def cadastro_leitor(request):
    return render(request, 'biblioteca/wp32_novo-leitor.html')

def acervo_geral(request):
    return render(request, 'biblioteca/wp41_acervo-geral.html')

def cadastro_acervo(request):
    return render(request, 'biblioteca/wp42_novo-livro.html')

def emprestimo(request):
    return render(request, 'biblioteca/wp51_status-geral.html')

def cadastro_emprestimo(request):
    return render(request, 'biblioteca/wp52_novo-emprestimo.html')