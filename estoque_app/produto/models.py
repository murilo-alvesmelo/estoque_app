from django.db import models

class Produto(models.Model):
    CATEGORIAS_CHOICES = [
        ('bebida', 'Bebida'),
        ('comida', 'Comida'),
        ('outros', 'Outros')
    ]

    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS_CHOICES, default='outros')
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estoque = models.PositiveIntegerField()
    fornecedor = models.CharField(max_length=100, blank=True, null=True)
    data_entrada = models.DateTimeField(auto_now_add=True)

    @property
    def valor_total(self):
        """Calcula o valor total do estoque dinamicamente"""
        return self.preco_venda * self.estoque

    def __str__(self):
        return f"{self.nome} - {self.estoque} unidades"
