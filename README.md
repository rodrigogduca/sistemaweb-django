# Sistema Web Django – Gerenciamento de Membros e Tarefas

Sistema web feito com Django para cadastrar, listar, editar e remover membros e suas tarefas. Utiliza Class-Based Views (POO), Tailwind CSS e autenticação com login.

## Funcionalidades
- Tela de login com autenticação do Django
- Controle de acesso: admin (superusuário) vê tudo, membro vê apenas suas tarefas
- Cadastro, listagem, edição e remoção de membros (apenas admin)
- Cadastro, edição e remoção de tarefas para cada membro
- Cada membro possui login próprio (usuário e senha)
- Interface com Tailwind CSS (via CDN)
- Views em Class-Based Views (POO) sem forms.py — inputs manuais no HTML

## Tecnologias
- Python 3.14
- Django 3.2 LTS
- MySQL 5.7 (MAMP)
- Tailwind CSS (CDN)
- python-dotenv (variáveis de ambiente)

## Como rodar o projeto

1. **Clone o repositório:**
	```
	git clone https://github.com/rodrigogduca/sistemaweb-django.git
	cd sistemaweb-django
	```

2. **Crie e ative o ambiente virtual:**
	```
	python -m venv venv
	.\venv\Scripts\activate
	```

3. **Instale as dependências:**
	```
	pip install -r requirements.txt
	```

4. **Configure as variáveis de ambiente:**
	- Crie um arquivo `.env` na raiz do projeto com:
	```
	SECRET_KEY=sua_chave_secreta
	DEBUG=True
	DB_PASSWORD=root
	DB_PORT=3306
	```

5. **Inicie o MAMP e crie o banco de dados no phpMyAdmin:**
	```sql
	CREATE DATABASE sistemaweb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
	```

6. **Aplique as migrações:**
	```
	python manage.py migrate
	```

	> **Nota:** Ao executar `migrate`, um superusuário padrão é criado automaticamente:
	> - **Usuário:** admin
	> - **Senha:** admin
	> - **Email:** admin@admin.com

7. **Rode o servidor:**
	```
	python manage.py runserver
	```

8. **Acesse no navegador:**
	- [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
	- Você será redirecionado para a tela de login.

## Estrutura do Projeto
```
sistemaweb-django/
├── setup/                          # Pacote de configuração do Django
│   ├── settings.py                 # Configurações (banco, apps, templates)
│   ├── urls.py                     # Rotas raiz (inclui as URLs do app)
│   ├── wsgi.py                     # Ponto de entrada WSGI (produção)
│   └── asgi.py                     # Ponto de entrada ASGI (async)
├── sistemaweb/                     # App principal
│   ├── models.py                   # Modelos de dados (Membro, Tarefa)
│   ├── views.py                    # Lógica das páginas (10 Class-Based Views)
│   ├── urls.py                     # Rotas do app (login, membros, tarefas)
│   └── migrations/                 # Migrações do banco de dados
├── templates/sistemaweb/           # Templates HTML com Tailwind CSS
│   ├── base.html                   # Template base (navbar + layout)
│   ├── login.html                  # Tela de login
│   ├── index.html                  # Página inicial (admin)
│   ├── listar_membros.html         # Lista de membros (admin)
│   ├── cadastrar_membro.html       # Formulário de cadastro
│   ├── editar_membro.html          # Formulário de edição
│   ├── detalhes_membro.html        # Detalhes + tarefas do membro
│   ├── remover_membro.html         # Confirmação de remoção
│   ├── editar_tarefa.html          # Edição de tarefa
│   └── remover_tarefa.html         # Confirmação de remoção de tarefa
├── manage.py                       # Utilitário de linha de comando do Django
├── requirements.txt                # Dependências do projeto
├── .env                            # Variáveis de ambiente (não versionado)
├── .gitignore                      # Arquivos ignorados pelo Git
└── LICENSE                         # Licença MIT
```

## Observações
- O projeto utiliza autenticação com login/logout.
- Todas as páginas são protegidas — só usuários logados acessam o sistema.
- Não utiliza forms.py — os inputs são escritos direto no HTML e tratados na view.
- O painel administrativo do Django está desabilitado.
- Utiliza `legacy-cgi` para compatibilidade entre Django 3.2 e Python 3.14.

---
Feito para fins didáticos.
