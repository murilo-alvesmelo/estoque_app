from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from produto.models import Produto  
from .models import Venda
from .form import VendaForm

@login_required
def registrar_venda(request):
    if request.method == 'POST':
        form = VendaForm(request.POST)
        if form.is_valid():
            venda = form.save(commit=False)
            venda.preco_unitario = venda.produto.preco_venda  # Captura o preço atual
            try:
                venda.save()
                return redirect('listar_vendas')
            except ValueError:
                form.add_error('quantidade', 'Estoque insuficiente!')

    else:
        form = VendaForm()

    return render(request, 'vendas/registrar_venda.html', {'form': form})

@login_required
def listar_vendas(request):
    if request.method == "POST":
        form = VendaForm(request.POST)
        if form.is_valid():
            venda = form.save(commit=False)
            venda.preco_unitario = venda.produto.preco_venda  # Captura o preço atual do produto
            try:
                venda.save()  # Agora já dá baixa no estoque!
                return redirect('listar_vendas')  # Redireciona para limpar o formulário e atualizar os produtos
            except ValueError as e:
                form.add_error(None, str(e))  # Exibe erro no template se o estoque for insuficiente

    else:
        form = VendaForm()

    vendas_list = Venda.objects.all().order_by('-data_venda')
    paginator = Paginator(vendas_list, 10)
    page_number = request.GET.get('page')
    vendas = paginator.get_page(page_number)

    produtos = Produto.objects.all()  # Carrega a lista de produtos atualizada

    return render(request, 'vendas/listar_vendas.html', {
        'form': form,
        'vendas': vendas,
        'produtos': produtos  # Agora enviamos os produtos atualizados para o template
    })