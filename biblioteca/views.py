from django.shortcuts import render

def index(request):
    return render(request, 'biblioteca/wp1_login.html')

def inicio(request):
    return render(request,'biblioteca/wp2_inicio.html')