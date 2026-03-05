"""
0002_create_admin.py - Migração que cria o superusuário admin automaticamente.

Ao rodar 'python manage.py migrate', esta migração cria um superusuário
com login 'admin' e senha 'admin' para acesso imediato ao sistema.
Isso elimina a necessidade de rodar 'createsuperuser' manualmente.

Credenciais padrão:
- Usuário: admin
- Senha: admin
- Email: admin@admin.com
"""

from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_superuser(apps, schema_editor):
    """Cria o superusuário admin se ele ainda não existir."""
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
    """Remove o superusuário admin (usado para reverter a migração)."""
    User = apps.get_model('auth', 'User')
    User.objects.filter(username='admin').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('sistemaweb', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(create_superuser, remove_superuser),
    ]
