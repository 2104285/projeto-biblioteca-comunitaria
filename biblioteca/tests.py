from django.test import TestCase, Client
from biblioteca.models import TbLivro, TbLeitor, TbEmprestimo
import os

#Vá na pasta setup/settings.py e altere os.environ['TESTING'] para 'True' para rodar os testes unitarios

class TbLivroTestCase(TestCase):
    def setUp(self) -> None:
        TbLivro.objects.create(tombo=1, titulo="Livro 1", autor="Autor 1", classificacao="Infantil", na=1)
        TbLeitor.objects.create(nome="Leitor 1", cep="00000-000", endereco="Rua 1", numero="1", bairro="Bairro 1", cidade="Cidade 1", estado="Estado 1", ddd="11", telefone="11111111", ativo="Sim")
        
    def test_status(self):
        livro = TbLivro.objects.get(tombo=1)
        self.assertEqual(livro.status, "Disponível")

    def test_status_emprestado(self):
        livro = TbLivro.objects.get(tombo=1)
        leitor = TbLeitor.objects.get(nome="Leitor 1")
        TbEmprestimo.objects.create(data_emprestimo="2021-01-01", data_devolucao_prevista="2021-01-15", livro=livro, leitor=leitor)
        self.assertEqual(livro.status, "Emprestado")

class Request(TestCase):
    def setUp(self) -> None:
        self.client = Client()
    
    def test_get_inicio(self):
        response = self.client.get('/leitor-geral')
        self.assertEqual(response.status_code, 200)