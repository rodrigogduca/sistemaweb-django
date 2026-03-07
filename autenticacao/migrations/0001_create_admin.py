"""
0001_create_admin.py - Migração que cria o superusuário admin automaticamente.

Ao rodar 'python manage.py migrate', esta migração cria um superusuário
com login 'admin' e senha 'admin' para acesso imediato ao sistema.
Isso elimina a necessidade de rodar 'createsuperuser' manualmente.

Conceitos usados:
- Data Migration: migração que manipula DADOS (não estrutura de tabelas).
  Diferente das migrações normais que criam/alteram tabelas, esta insere
  registros no banco de dados.

- RunPython: operação que executa uma função Python durante a migração.
  Recebe duas funções: uma para aplicar e outra para reverter.

- apps.get_model(): busca o modelo (tabela) pelo nome do app e do modelo.
  Usado em vez de importar diretamente para funcionar em qualquer estado
  do banco de dados.

- make_password(): converte a senha em texto puro para um hash seguro.
  O Django NUNCA armazena senhas em texto puro — sempre usa hashing.

Credenciais padrão:
- Usuário: admin
- Senha: admin
- Email: admin@admin.com
"""

from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_superuser(apps, schema_editor):
    """
    Cria o superusuário admin se ele ainda não existir.

    Parâmetros:
        apps: registro de modelos disponíveis neste ponto da migração
        schema_editor: objeto para manipular o esquema do banco (não usado aqui)
    """
    User = apps.get_model('auth', 'User')
    if not User.objects.filter(username='admin').exists():
        User.objects.create(
            username='admin',
            email='admin@admin.com',
            password=make_password('admin'),
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )


def remove_superuser(apps, schema_editor):
    """
    Remove o superusuário admin (usado para reverter a migração).

    No Django, toda migração pode ser revertida. Esta função é o "desfazer"
    da create_superuser. É executada ao rodar: python manage.py migrate autenticacao zero
    """
    User = apps.get_model('auth', 'User')
    User.objects.filter(username='admin').delete()


class Migration(migrations.Migration):

    # Esta migração pertence ao app 'autenticacao' e depende apenas
    # da migração do app 'auth' que cria a tabela User
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        # RunPython executa a função create_superuser ao aplicar a migração
        # e remove_superuser ao reverter (migrate ... zero)
        migrations.RunPython(create_superuser, remove_superuser),
    ]
