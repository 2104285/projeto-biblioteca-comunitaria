# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import datetime as dt


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TbEmprestimo(models.Model):
    id = models.AutoField(primary_key=True)
    leitor = models.ForeignKey('TbLeitor', models.DO_NOTHING, blank=True, null=True)
    livro = models.ForeignKey('TbLivro', models.DO_NOTHING, blank=True, null=True)
    data_emprestimo = models.DateField(blank=True, null=True)
    obs_emprestimo = models.CharField(max_length=255, blank=True, null=True)
    data_devolucao = models.DateField(blank=True, null=True)
    obs_devolucao = models.CharField(max_length=255, blank=True, null=True)
    data_devolucao_prevista = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tb_emprestimo'

    @property
    def status(self):
        if self.data_devolucao == None and self.data_devolucao_prevista >= dt.date.today():
            return "Não Entregue"
        elif self.data_devolucao == None and self.data_devolucao_prevista < dt.date.today():
            return "Atrasado"
        else:
            return "Entregue"


class TbLeitor(models.Model):
    leitor_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, blank=True, null=True)
    cep = models.CharField(max_length=9, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=6, blank=True, null=True)
    bairro = models.CharField(max_length=45, blank=True, null=True)
    cidade = models.CharField(max_length=45, blank=True, null=True)
    estado = models.CharField(max_length=45, blank=True, null=True)
    ddd = models.CharField(max_length=2, blank=True, null=True)
    telefone = models.CharField(max_length=9, blank=True, null=True)
    ativo = models.CharField(max_length=45, blank=True, null=True)
    visivel = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'tb_leitor'


class TbLivro(models.Model):
    livro_id = models.AutoField(primary_key=True)
    tombo = models.CharField(max_length=255, blank=True, null=True)
    titulo = models.CharField(max_length=255, blank=True, null=True)
    autor = models.CharField(max_length=255, blank=True, null=True)
    classificacao = models.CharField(max_length=255, blank=True, null=True)
    na = models.CharField(max_length=255, blank=True, null=True)  # Field name made lowercase.
    visivel = models.BooleanField(default=True)

    @property
    def status(self):
        #emprestimo = TbEmprestimo.objects.all().filter(livro__tombo = self.tombo)
        emprestimo = TbEmprestimo.objects.filter(livro__tombo = self.tombo)
        emprestado = False
        for livro in emprestimo:
            if livro.data_devolucao == None:
                emprestado = True
        if emprestado:
            return "Emprestado"
        else:
            return "Disponível"
        
    class Meta:
        managed = True
        db_table = 'tb_livro'

    
