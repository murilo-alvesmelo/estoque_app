from django.shortcuts import render
from produto.models.models import Produto, Retirada

def dashboard(request):
    produtos = Produto.objects.all()
    movimentacoes = Retirada.objects.all().order_by('-data_retirada')[:10]

    context = {
        'produtos': produtos,
        'movimentacoes': movimentacoes
    }
    return render(request, 'inicio/dashboard.html', context)