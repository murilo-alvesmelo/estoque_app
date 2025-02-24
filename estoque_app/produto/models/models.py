from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    qtd_estoque_inicial = models.IntegerField()
    valor_estoque = models.DecimalField(max_digits=10, decimal_places=2)
    data_entrada = models.DateField()
    
    def save(self, *args, **kwargs):
        self.valor_estoque = self.qtd_estoque_inicial * self.valor_unitario
        super(Produto, self).save(*args, **kwargs)

    def __str__(self):
        return self.nome

class Retirada(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='retiradas')
    quantidade = models.PositiveIntegerField()
    data_retirada = models.DateTimeField(auto_now_add=True) 
    tipo = models.CharField(max_length=255, default='retirada')

    def __str__(self):
        return f"{self.quantidade} unidades de {self.produto.nome}"

    def save(self, *args, **kwargs):
        # Atualiza o estoque ao registrar uma retirada
        if self.pk is None:  # Apenas na criação
            if self.produto.qtd_estoque_inicial >= self.quantidade:
                self.produto.qtd_estoque_inicial -= self.quantidade
                self.produto.save()
            else:
                raise ValueError("Estoque insuficiente para essa retirada.")
        super().save(*args, **kwargs)

class Entrada(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='entradas')
    quantidade = models.PositiveIntegerField()
    data_entrada = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=255, default='entrada')

    def __str__(self):
        return f"{self.quantidade} unidades de {self.produto.nome}"

    def save(self, *args, **kwargs):
        # Atualiza o estoque ao registrar uma entrada
        if self.pk is None:  # Apenas na criação
            self.produto.qtd_estoque_inicial += self.quantidade
            self.produto.save()
        super().save(*args, **kwargs)