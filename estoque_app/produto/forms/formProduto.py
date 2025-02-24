from django import forms
from ..models.models import Produto, Retirada, Entrada

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'valor_unitario', 'qtd_estoque_inicial', 'data_entrada']
        widgets = {
            'data_entrada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_validade': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'nome': 'Nome',
            'valor_unitario': 'Valor Unitário',
            'qtd_estoque_inicial': 'Quantidade em Estoque',
            'data_entrada': 'Data de Entrada',
            'data_validade': 'Data de Validade',
        }

class RetiradaForm(forms.ModelForm):
    class Meta:
        model = Retirada
        fields = ['produto', 'quantidade']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class EntradaForm(forms.ModelForm):
    class Meta:
        model = Entrada
        fields = ['produto', 'quantidade']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
        }