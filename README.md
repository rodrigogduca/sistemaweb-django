# Sistema Web Django – Gerenciamento de Membros e Tarefas

Este é um projeto simples feito com Django, ideal para iniciantes, que permite cadastrar, listar, editar e remover membros, além de atribuir tarefas a cada membro.

## Funcionalidades
- Cadastro, listagem, edição e remoção de membros
- Cadastro, listagem, edição e remoção de tarefas para cada membro
- Visualização das tarefas de um membro ao clicar em seu nome
- Interface web simples e didática

## Como rodar o projeto

1. **Clone o repositório:**
	```
	git clone https://github.com/SEU_USUARIO/sistemaweb-django.git
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
	  ```

5. **Aplique as migrações:**
	```
	python manage.py migrate
	```

6. **Rode o servidor:**
	```
	python manage.py runserver
	```

7. **Acesse no navegador:**
	- [http://127.0.0.1:8000/membros/](http://127.0.0.1:8000/membros/)

## Estrutura do Projeto
- `membros/` – App responsável pelos membros e tarefas
- `templates/` – Páginas HTML do sistema
- `forms.py` – Formulários para cadastro e edição
- `models.py` – Modelos de dados (Membro, Tarefa)
- `views.py` – Lógica das páginas
- `urls.py` – Rotas do sistema

## Observações
- O projeto não utiliza painel administrativo nem autenticação.
- Ideal para aprendizado de Django e CRUD básico.

---

Feito para fins didáticos. Sinta-se à vontade para modificar e aprimorar!
# sistemaweb-django