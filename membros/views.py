from django.shortcuts import render, redirect, get_object_or_404
from .models import Membro, Tarefa
from .forms import MembroForm, TarefaForm


# Página inicial do sistema
def index(request):
    return render(request, 'membros/index.html')


# CRUD Membros
def listar_membros(request):
    membros = Membro.objects.all()
    return render(request, 'membros/listar_membros.html', {'membros': membros})

# Cadastrar
def cadastrar_membro(request):
    if request.method == 'POST':
        form = MembroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_membros')
    else:
        form = MembroForm()
    return render(request, 'membros/cadastrar_membro.html', {'form': form})


# Editar
def editar_membro(request, membro_id):
    membro = get_object_or_404(Membro, id=membro_id)
    if request.method == 'POST':
        form = MembroForm(request.POST, instance=membro)
        if form.is_valid():
            form.save()
            return redirect('listar_membros')
    else:
        form = MembroForm(instance=membro)
    return render(request, 'membros/editar_membro.html', {'form': form, 'membro': membro})


# Remover
def remover_membro(request, membro_id):
    membro = get_object_or_404(Membro, id=membro_id)
    if request.method == 'POST':
        membro.delete()
        return redirect('listar_membros')
    return render(request, 'membros/remover_membro.html', {'membro': membro})


# CRUD Tarefas
# Exibir e Adicionar
def detalhes_membro(request, membro_id):
    membro = get_object_or_404(Membro, id=membro_id)
    tarefas = Tarefa.objects.filter(membro=membro)
    if request.method == 'POST':
        form = TarefaForm(request.POST)
        if form.is_valid():
            tarefa = form.save(commit=False)
            tarefa.membro = membro
            tarefa.save()
            return redirect('detalhes_membro', membro_id=membro.id)
    else:
        form = TarefaForm()
    return render(request, 'membros/detalhes_membro.html', {'membro': membro, 'tarefas': tarefas, 'form': form})


# Editar
def editar_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    if request.method == 'POST':
        form = TarefaForm(request.POST, instance=tarefa)
        if form.is_valid():
            form.save()
            return redirect('detalhes_membro', membro_id=tarefa.membro.id)
    else:
        form = TarefaForm(instance=tarefa)
    return render(request, 'membros/editar_tarefa.html', {'form': form, 'tarefa': tarefa})


# Remover
def remover_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    membro_id = tarefa.membro.id
    if request.method == 'POST':
        tarefa.delete()
        return redirect('detalhes_membro', membro_id=membro_id)
    return render(request, 'membros/remover_tarefa.html', {'tarefa': tarefa})