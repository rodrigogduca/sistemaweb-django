"""
models.py - Definição dos modelos de dados do sistema.

Este arquivo define as tabelas do banco de dados usando o ORM do Django.
Cada classe representa uma tabela no MySQL. O Django converte automaticamente
esses modelos em tabelas com o prefixo 'sistemaweb_' (ex: sistemaweb_membro).

Conceitos usados:
- models.Model: Classe base do Django que transforma a classe Python em tabela SQL
- CharField: Campo de texto com tamanho máximo definido
- EmailField: Campo de email com validação automática
- DateTimeField: Campo de data/hora
- OneToOneField: Relação um-para-um entre tabelas
- ForeignKey: Relação muitos-para-um entre tabelas
"""

from django.db import models
from django.contrib.auth.models import User


class Membro(models.Model):
    """
    Modelo que representa um membro (pessoa) no sistema.

    Cada membro possui um nome, email único e data de criação automática.
    O campo 'user' conecta o membro a um usuário do Django (modelo User),
    permitindo que o membro faça login no sistema. Essa relação é OneToOne
    (um-para-um): cada usuário do Django pode estar vinculado a no máximo
    um membro, e cada membro a no máximo um usuário.

    Tabela no banco: sistemaweb_membro
    """

    # Relação um-para-um com o modelo User do Django (sistema de autenticação)
    # on_delete=CASCADE: se o User for deletado, o Membro também é deletado
    # null=True e blank=True permitem membros sem usuário vinculado
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    # Nome completo do membro (máximo 100 caracteres)
    nome = models.CharField(max_length=100)

    # Email do membro - unique=True garante que não pode repetir no banco
    email = models.EmailField(unique=True)

    # Data e hora em que o membro foi cadastrado (preenchido automaticamente)
    # auto_now_add=True: Django preenche com a data/hora atual ao criar o registro
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Retorna o nome do membro como representação em texto."""
        return self.nome


class Tarefa(models.Model):
    """
    Modelo que representa uma tarefa atribuída a um membro.

    Cada tarefa tem título, descrição, status (pendente ou concluída),
    data de criação e uma referência ao membro dono da tarefa.
    A relação ForeignKey (muitos-para-um) significa que um membro pode
    ter várias tarefas, mas cada tarefa pertence a apenas um membro.
    Ao deletar um membro, todas as suas tarefas são removidas (CASCADE).

    Tabela no banco: sistemaweb_tarefa
    """

    # Título da tarefa (máximo 200 caracteres)
    titulo = models.CharField(max_length=200)

    # Descrição detalhada da tarefa (blank=True: pode ficar em branco)
    descricao = models.TextField(blank=True)

    # Status da tarefa: 'pendente' (padrão) ou 'concluída'
    # choices define as opções válidas que aparecem no sistema
    status = models.CharField(
        max_length=20,
        choices=[('pendente', 'Pendente'), ('concluida', 'Concluída')],
        default='pendente'
    )

    # Data e hora de criação da tarefa (preenchido automaticamente)
    data_criacao = models.DateTimeField(auto_now_add=True)

    # Chave estrangeira (ForeignKey) - liga esta tarefa a um membro específico
    # on_delete=CASCADE: se o membro for deletado, suas tarefas também são
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE)

    def __str__(self):
        """Retorna o título da tarefa como representação em texto."""
        return self.titulo
