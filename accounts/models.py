from django.db import models
from django.contrib.auth.models import User

class Endereco(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cep = models.CharField(max_length=9)
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=50, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)  # Ex: RJ, SP

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.cidade}"