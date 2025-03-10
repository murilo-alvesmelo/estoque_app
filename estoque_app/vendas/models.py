from django.db import models
from produto.models import Produto

class Venda(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_venda = models.DateTimeField(auto_now_add=True)

    @property
    def total_venda(self):
        return self.quantidade * self.preco_unitario

    def save(self, *args, **kwargs):
        if not self.preco_unitario:
            self.preco_unitario = self.produto.preco_venda  # Captura o preço atual do produto

        # Verifica se tem estoque suficiente antes de vender
        if self.produto.estoque >= self.quantidade:
            self.produto.estoque -= self.quantidade  # Atualiza o estoque
            self.produto.save()  # Salva o produto com o novo estoque
            super().save(*args, **kwargs)  # Salva a venda
        else:
            raise ValueError("Estoque insuficiente para essa venda!")

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} - {self.data_venda.strftime('%d/%m/%Y %H:%M')}"