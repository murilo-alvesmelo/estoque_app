from django.contrib import admin
from ..models.models import Produto

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'valor_unitario', 'valor_venda', 'qtd_estoque', 'valor_estoque', 'data_entrada', 'data_validade')