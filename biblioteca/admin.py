from django.contrib import admin

from biblioteca.models import TbLeitor, TbEmprestimo,TbLivro
# Register your models here.

admin.site.register(TbLeitor)
admin.site.register(TbEmprestimo)
admin.site.register(TbLivro)