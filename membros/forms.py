from django import forms
from .models import Membro, Tarefa

class MembroForm(forms.ModelForm):
    class Meta:
        model = Membro
        fields = ['nome', 'email']


class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['titulo', 'descricao', 'status']