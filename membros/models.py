from django.db import models

class Membro(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
    

class Tarefa(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[('pendente', 'Pendente'), ('concluida', 'Concluída')], default='pendente')
    data_criacao = models.DateTimeField(auto_now_add=True)
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo


    
