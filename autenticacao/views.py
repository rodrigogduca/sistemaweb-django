"""
views.py - Views de autenticação (Login e Logout).

Este arquivo contém as Views responsáveis pelo controle de acesso ao sistema.
A autenticação é o processo de verificar a identidade do usuário (quem ele é),
enquanto a autorização define o que ele pode fazer após estar autenticado.

Conceitos de Programação Orientada a Objetos (POO) usados aqui:

1. CLASSE (class): Um "molde" para criar objetos. Cada View é uma classe.
2. HERANÇA: LoginView e LogoutView herdam de View (classe base do Django).
   Isso significa que elas "ganham" as funcionalidades da classe pai (View),
   como o método dispatch() que roteia GET/POST automaticamente.
3. MÉTODO: Funções definidas dentro de uma classe (get, post).
   O primeiro parâmetro 'self' é uma referência ao próprio objeto.
4. ENCAPSULAMENTO: Cada classe cuida apenas da sua responsabilidade.
   LoginView cuida do login, LogoutView cuida do logout.

Fluxo de autenticação do Django:
1. authenticate(username, password) -> verifica credenciais no banco de dados
2. login(request, usuario)          -> cria uma sessão (cookie) para o usuário
3. logout(request)                  -> destrói a sessão do usuário

Princípios de programação aplicados:
- Responsabilidade Única: cada classe faz apenas uma coisa
- DRY (Don't Repeat Yourself): reutilizamos as funções do Django em vez de reescrever
- Separação de Interesses: autenticação fica isolada neste app, separada das regras de negócio
"""

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from sistemaweb.models import Membro


class LoginView(View):
    template_name = 'autenticacao/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')

        # render() combina o template HTML com os dados e retorna o HTML final
        return render(request, self.template_name)

    def post(self, request):
        """
        Método POST - Processa o formulário de login (autentica usuário e senha).

        Parâmetros:
            self: referência ao próprio objeto
            request: contém os dados enviados pelo formulário em request.POST

        request.POST é um dicionário com os dados do formulário HTML.
        O método .get('campo') busca o valor de forma segura (retorna None se não existir).
        """
        # Captura os dados enviados pelo formulário HTML
        username = request.POST.get('username')
        password = request.POST.get('password')

        usuario = authenticate(request, username=username, password=password)

        if usuario is not None:

            login(request, usuario)

            if usuario.is_superuser:
                return redirect('index')

            try:
                membro = Membro.objects.get(user=usuario)
                return redirect('detalhes_membro', membro_id=membro.id)
            
            except Membro.DoesNotExist:
                return redirect('index')

        return render(request, self.template_name, {
            'erro': 'Usuário ou senha inválidos.'
        })


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('login')
