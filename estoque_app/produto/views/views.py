from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from ..models.models import Produto, Retirada, Entrada
from ..forms.formProduto import ProdutoForm, RetiradaForm, EntradaForm

def dashboard(request):
    return render(request, 'produto/dashboard.html')

def listar_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'produto/listar_produtos.html', {'produtos': produtos})

def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')  # Redireciona para a lista de produtos após criar
    else:
        form = ProdutoForm()
    
    return render(request, 'produto/criar_produto.html', {'form': form})

def excluir_produto(request, id):
    produto = Produto.objects.get(id=id)
    produto.delete()
    return redirect('listar_produtos') 

def registrar_retirada(request):
    if request.method == 'POST':
        form = RetiradaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrar_retirada')  # Redireciona para a mesma página após registrar
    else:
        form = RetiradaForm()

    # Busca todas as retiradas e ordena por data
    retiradas_list = Retirada.objects.select_related('produto').order_by('-data_retirada')

    # Configura o Paginator (10 retiradas por página)
    paginator = Paginator(retiradas_list, 10)
    page_number = request.GET.get('page')  # Pega o número da página da URL
    retiradas = paginator.get_page(page_number)  # Obtém os objetos da página atual

    return render(request, 'produto/registrar_retirada.html', {
        'form': form,
        'retiradas': retiradas,
    })

def registrar_entrada(request):
    if request.method == 'POST':
        form = EntradaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Entrada registrada com sucesso!")
            return redirect('registrar_entrada')
        else:
            messages.error(request, "Erro ao registrar a entrada. Verifique os dados informados.")
    else:
        form = EntradaForm()

    # Consulta todas as entradas para exibir na tabela
    entradas = Entrada.objects.order_by('-data_entrada')
    paginator = Paginator(entradas, 10)  # Paginação: 10 entradas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'page_obj': page_obj,
    }
    return render(request, 'produto/registrar_entrada.html', context)