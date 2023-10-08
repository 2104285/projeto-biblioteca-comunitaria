from django.urls import path
from biblioteca.views import *
from biblioteca.view_json import *

urlpatterns = [
    path('', inicio),
    path('inicio', inicio, name="inicio"),
    path('leitor-geral', leitor_geral, name='leitor-geral'),
    path('leitor-geral/get-pdf', generate_pdf_leitor, name='generate-pdf-leitor'),
    path('leitor-geral/<int:id>', update_leitor, name='leitor-geral'),
    path('leitor-geral/delete/<int:id>', remove_visility_leitor, name='leitor-geral'),
    path('cadastro-leitor/', cadastro_leitor, name='cadastro-leitor'),
    path('acervo-geral', acervo_geral, name='acervo-geral'),
    path('acervo-geral/get-pdf', generate_pdf_acervo, name='generate-pdf-acervo'),
    path('acervo-geral/<int:id>', update_acervo, name='acervo-geral'),
    path('acervo-geral/delete/<int:id>', remove_visility_acervo),
    path('cadastro-acervo/', cadastro_acervo, name='cadastro-acervo'),
    path('emprestimo', emprestimo, name='emprestimo'),
    path('emprestimo/<int:id>', emprestimo_edit, name='emprestimo'),
    path('cadastro-emprestimo', cadastro_emprestimo, name='cadastro-emprestimo'),
    path('json/leitor/<int:id>', json_leitor),
    path('json/getEmprestimoByLeitor/<int:id>', json_get_emprestimo_by_leitorId),
    path('json/getQtyLivroDisponivel', json_get_livros_dispoiveis),
    path('json/getLivroStatusByID/<int:id>', json_get_livro_status_by_id)
]
