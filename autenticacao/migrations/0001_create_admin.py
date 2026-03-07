
from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_superuser(apps, schema_editor):
   
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
