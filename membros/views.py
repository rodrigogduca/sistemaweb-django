from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Membro, Tarefa


# Login - inputs manuais no HTML, sem forms.py
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, 'membros/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('index')
        return render(request, 'membros/login.html', {'erro': 'Usuario ou senha invalidos.'})


# Logout
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


# Pagina inicial (protegida)
class IndexView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        return render(request, 'membros/index.html')


# Listar todos os membros (protegida)
class ListarMembrosView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        membros = Membro.objects.all()
        return render(request, 'membros/listar_membros.html', {'membros': membros})


# Cadastrar membro (protegida)
class CadastrarMembroView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        return render(request, 'membros/cadastrar_membro.html')

    def post(self, request):
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        if nome and email:
            Membro.objects.create(nome=nome, email=email)
            return redirect('listar_membros')
        return render(request, 'membros/cadastrar_membro.html')


# Editar membro (protegida)
class EditarMembroView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, membro_id):
        membro = get_object_or_404(Membro, id=membro_id)
        return render(request, 'membros/editar_membro.html', {'membro': membro})

    def post(self, request, membro_id):
        membro = get_object_or_404(Membro, id=membro_id)
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        if nome and email:
            membro.nome = nome
            membro.email = email
            membro.save()
            return redirect('listar_membros')
        return render(request, 'membros/editar_membro.html', {'membro': membro})


# Remover membro (protegida)
class RemoverMembroView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, membro_id):
        membro = get_object_or_404(Membro, id=membro_id)
        return render(request, 'membros/remover_membro.html', {'membro': membro})

    def post(self, request, membro_id):
        membro = get_object_or_404(Membro, id=membro_id)
        membro.delete()
        return redirect('listar_membros')


# Detalhes do membro + adicionar tarefa (protegida)
class DetalhesMembroView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, membro_id):
        membro = get_object_or_404(Membro, id=membro_id)
        tarefas = Tarefa.objects.filter(membro=membro)
        return render(request, 'membros/detalhes_membro.html', {'membro': membro, 'tarefas': tarefas})

    def post(self, request, membro_id):
        membro = get_object_or_404(Membro, id=membro_id)
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        if titulo and descricao:
            Tarefa.objects.create(membro=membro, titulo=titulo, descricao=descricao)
            return redirect('detalhes_membro', membro_id=membro.id)
        tarefas = Tarefa.objects.filter(membro=membro)
        return render(request, 'membros/detalhes_membro.html', {'membro': membro, 'tarefas': tarefas})


# Editar tarefa (protegida)
class EditarTarefaView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, tarefa_id):
        tarefa = get_object_or_404(Tarefa, id=tarefa_id)
        return render(request, 'membros/editar_tarefa.html', {'tarefa': tarefa})

    def post(self, request, tarefa_id):
        tarefa = get_object_or_404(Tarefa, id=tarefa_id)
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        if titulo and descricao:
            tarefa.titulo = titulo
            tarefa.descricao = descricao
            tarefa.save()
            return redirect('detalhes_membro', membro_id=tarefa.membro.id)
        return render(request, 'membros/editar_tarefa.html', {'tarefa': tarefa})


# Remover tarefa (protegida)
class RemoverTarefaView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, tarefa_id):
        tarefa = get_object_or_404(Tarefa, id=tarefa_id)
        return render(request, 'membros/remover_tarefa.html', {'tarefa': tarefa})

    def post(self, request, tarefa_id):
        tarefa = get_object_or_404(Tarefa, id=tarefa_id)
        membro_id = tarefa.membro.id
        tarefa.delete()
        return redirect('detalhes_membro', membro_id=membro_id)
