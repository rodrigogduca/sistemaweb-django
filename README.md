# Sistema Web Django – Gerenciamento de Membros e Tarefas

Sistema web feito com Django para cadastrar, listar, editar e remover membros e suas tarefas. Utiliza Class-Based Views (POO), Tailwind CSS e autenticacao com login.

## Funcionalidades
- Tela de login com autenticacao do Django
- Controle de acesso: admin (superusuario) ve tudo, membro ve apenas suas tarefas
- Cadastro, listagem, edicao e remocao de membros (apenas admin)
- Cadastro, edicao e remocao de tarefas para cada membro
- Cada membro possui login proprio (usuario e senha)
- Interface com Tailwind CSS (via CDN)
- Views em Class-Based Views (POO) sem forms.py — inputs manuais no HTML

## Tecnologias
- Python 3.14
- Django 4.2 LTS
- MySQL Server 8.0
- Tailwind CSS (CDN)
- python-dotenv (variaveis de ambiente)

## Como rodar o projeto

1. **Clone o repositorio:**
	```
	git clone https://github.com/rodrigogduca/sistemaweb-django.git
	cd sistemaweb-django
	```

2. **Crie e ative o ambiente virtual:**
	```
	python -m venv venv
	.\venv\Scripts\activate
	```

3. **Instale as dependencias:**
	```
	pip install -r requirements.txt
	```

4. **Configure as variaveis de ambiente:**
	- Crie um arquivo `.env` na raiz do projeto com:
	```
	SECRET_KEY=sua_chave_secreta
	DEBUG=True
	PASSWORD=sua_senha_mysql
	```

5. **Crie o banco de dados no MySQL:**
	```sql
	CREATE DATABASE sistemaweb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
	```

6. **Aplique as migracoes:**
	```
	python manage.py migrate
	```

7. **Crie um superusuario para login:**
	```
	python manage.py createsuperuser
	```

8. **Rode o servidor:**
	```
	python manage.py runserver
	```

9. **Acesse no navegador:**
	- [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
	- Voce sera redirecionado para a tela de login.

## Estrutura do Projeto
```
sistemaweb-django/
├── setup/                          # Pacote de configuracao do Django
│   ├── settings.py                 # Configuracoes (banco, apps, templates)
│   ├── urls.py                     # Rotas raiz (inclui as URLs do app)
│   ├── wsgi.py                     # Ponto de entrada WSGI (producao)
│   └── asgi.py                     # Ponto de entrada ASGI (async)
├── sistemaweb/                     # App principal
│   ├── models.py                   # Modelos de dados (Membro, Tarefa)
│   ├── views.py                    # Logica das paginas (10 Class-Based Views)
│   ├── urls.py                     # Rotas do app (login, membros, tarefas)
│   ├── apps.py                     # Configuracao do app
│   ├── admin.py                    # Admin do Django (desabilitado)
│   ├── migrations/                 # Migracoes do banco de dados
│   └── static/sistemaweb/css/      # CSS personalizado
├── templates/sistemaweb/           # Templates HTML com Tailwind CSS
│   ├── base.html                   # Template base (navbar + layout)
│   ├── login.html                  # Tela de login
│   ├── index.html                  # Pagina inicial (admin)
│   ├── listar_membros.html         # Lista de membros (admin)
│   ├── cadastrar_membro.html       # Formulario de cadastro
│   ├── editar_membro.html          # Formulario de edicao
│   ├── detalhes_membro.html        # Detalhes + tarefas do membro
│   ├── remover_membro.html         # Confirmacao de remocao
│   ├── editar_tarefa.html          # Edicao de tarefa
│   └── remover_tarefa.html         # Confirmacao de remocao de tarefa
├── manage.py                       # Utilitario de linha de comando do Django
├── requirements.txt                # Dependencias do projeto
├── .env                            # Variaveis de ambiente (nao versionado)
├── .gitignore                      # Arquivos ignorados pelo Git
└── LICENSE                         # Licenca MIT
```

## Observacoes
- O projeto utiliza autenticacao com login/logout.
- Todas as paginas sao protegidas — so usuarios logados acessam o sistema.
- Nao utiliza forms.py — os inputs sao escritos direto no HTML e tratados na view.
- O painel administrativo do Django esta desabilitado.

---
Feito para fins didaticos.
