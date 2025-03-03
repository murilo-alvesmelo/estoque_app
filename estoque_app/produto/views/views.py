from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from ..models.models import Produto, Retirada, Entrada
from ..forms.formProduto import ProdutoForm, RetiradaForm, EntradaForm

def dashboard(request):
    return render(request, 'produto/dashboard.html')

@login_required
def listar_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'produto/listar_produtos.html', {'produtos': produtos})

@login_required
def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')  
    else:
        form = ProdutoForm()
    
    return render(request, 'produto/criar_produto.html', {'form': form})

@login_required
def excluir_produto(request, id):
    produto = Produto.objects.get(id=id)
    produto.delete()
    return redirect('listar_produtos') 

@login_required
def registrar_retirada(request):
    if request.method == 'POST':
        form = RetiradaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrar_retirada') 
        form = RetiradaForm()

    retiradas_list = Retirada.objects.select_related('produto').order_by('-data_retirada')

    paginator = Paginator(retiradas_list, 10)
    page_number = request.GET.get('page')  
    retiradas = paginator.get_page(page_number) 

    return render(request, 'produto/registrar_retirada.html', {
        'form': form,
        'retiradas': retiradas,
    })

@login_required
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

    entradas = Entrada.objects.order_by('-data_entrada')
    paginator = Paginator(entradas, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'page_obj': page_obj,
    }
    return render(request, 'produto/registrar_entrada.html', context)