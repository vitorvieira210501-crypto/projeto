from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome")
    description = models.TextField(verbose_name="Descrição", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    image = models.ImageField(upload_to='products/', verbose_name="Imagem", blank=True, null=True)
    stock = models.IntegerField(default=0, verbose_name="Estoque")
    is_featured = models.BooleanField(default=False, verbose_name="Destaque na Home?")
    active = models.BooleanField(default=True, verbose_name="Ativo")

    def __str__(self):
        return self.name