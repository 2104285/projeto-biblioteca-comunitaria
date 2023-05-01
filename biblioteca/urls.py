from django.urls import path
from biblioteca.views import *

urlpatterns = [
    path('', index),
    path('inicio', inicio, name="inicio"),
    path('leitor-geral', leitor_geral, name='leitor-geral'),
    path('leitor-geral/<int:id>', update_leitor, name='leitor-geral'),
    path('cadastro-leitor/', cadastro_leitor, name='cadastro-leitor'),
    path('acervo-geral/', acervo_geral, name='acervo-geral'),
    path('cadastro-acervo/', cadastro_acervo, name='cadastro-acervo'),
    path('emprestimo/', emprestimo, name='emprestimo'),
    path('cadastro-emprestimo', cadastro_emprestimo, name='cadastro-emprestimo')
]
