from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'categoria', 'preco_venda', 'preco_custo', 'estoque', 'fornecedor']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'preco_venda': forms.NumberInput(attrs={'class': 'form-control'}),
            'preco_custo': forms.NumberInput(attrs={'class': 'form-control'}),
            'estoque': forms.NumberInput(attrs={'class': 'form-control'}),
            'fornecedor': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'nome': 'Nome',
            'categoria': 'Categoria',
            'preco_venda': 'Preço de Venda',
            'preco_custo': 'Preço de Custo',
            'estoque': 'Estoque',
            'fornecedor': 'Fornecedor',
        }