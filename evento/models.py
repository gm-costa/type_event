from django.db import models
from django.contrib.auth.models import User


class Evento(models.Model):
    choices_status = (
        ('I', 'Initializado'),
        ('F', 'Finalizado')
    )
    criador = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    data_inicio = models.DateField()
    data_termino = models.DateField()
    carga_horaria = models.IntegerField()
    logo = models.FileField(upload_to="logos")
    status = models.CharField(max_length=1, choices=choices_status, default='I')

    #paleta de cores
    cor_principal = models.CharField(max_length=7)
    cor_secundaria = models.CharField(max_length=7)
    cor_fundo = models.CharField(max_length=7)
    

    def __str__(self):
        return self.nome
