from biblioteca.models import *

teste = TbEmprestimo.objects.get(pk=2604)
print(teste.leitor)
