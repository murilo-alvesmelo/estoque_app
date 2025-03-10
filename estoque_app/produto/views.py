from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Produto
from .form import ProdutoForm

@login_required
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
def editar_produto(request, id):
    produto = Produto.objects.get(id=id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = ProdutoForm(instance=produto)
    
    return render(request, 'produto/editar_produto.html', {'form': form})
