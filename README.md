# Sistema Web Django – Gerenciamento de Membros e Tarefas

Sistema web feito com Django para cadastrar, listar, editar e remover membros e suas tarefas. Utiliza Class-Based Views (POO), Tailwind CSS e autenticacao com login.

## Funcionalidades
- Tela de login com autenticacao do Django
- Cadastro, listagem, edicao e remocao de membros
- Cadastro, listagem, edicao e remocao de tarefas para cada membro
- Visualizacao das tarefas de um membro ao clicar em seu nome
- Interface com Tailwind CSS (via CDN)
- Views em Class-Based Views (POO) sem forms.py — inputs manuais no HTML

## Tecnologias
- Python 3
- Django 4.2 LTS
- MySQL (MAMP ou MySQL Server 8.0)
- Tailwind CSS (CDN)

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
	  DB_PASSWORD=sua_senha_mysql
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

<<<<<<< HEAD
9. **Acesse no navegador:**
	- [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
	- Voce sera redirecionado para a tela de login.
=======
7. **Acesse no navegador:**
	- [http://127.0.0.1:8000](http://127.0.0.1:8000)
>>>>>>> 133b7b2a3e21d66cb51c74e1ddb078b7ab3fe53d

## Estrutura do Projeto
- `membros/` – App responsavel pelos membros e tarefas
- `templates/` – Paginas HTML com Tailwind CSS
- `models.py` – Modelos de dados (Membro, Tarefa)
- `views.py` – Logica das paginas em Class-Based Views (POO)
- `urls.py` – Rotas do sistema

<<<<<<< HEAD
## Observacoes
- O projeto utiliza autenticacao com login/logout.
- Todas as paginas sao protegidas — so usuarios logados acessam o sistema.
- Nao utiliza forms.py — os inputs sao escritos direto no HTML e tratados na view.
- O painel administrativo do Django esta desabilitado.

---

Feito para fins didaticos. Sinta-se a vontade para modificar e aprimorar!
=======
## Observações
- O projeto não utiliza painel administrativo nem autenticação.

---
>>>>>>> 133b7b2a3e21d66cb51c74e1ddb078b7ab3fe53d
