import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from django.db.models import Sum  
from produto.models import Produto
from vendas.models import Venda
from datetime import timedelta
from django.db.models import F, ExpressionWrapper, DecimalField
from django.core.paginator import Paginator

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home") 
        else:
            return render(request, "inicio/login.html", {"error": "Usuário ou senha inválidos"})
    
    return render(request, "inicio/login.html")

def logout_view(request):
    logout(request)
    return redirect("login") 


@login_required
def dashboard(request):
    # 🔹 Definir período da semana atual
    hoje = now().date()
    inicio_semana = hoje - timedelta(days=hoje.weekday())  # Segunda-feira
    fim_semana = inicio_semana + timedelta(days=6)  # Domingo

    # 🔹 Buscar vendas dentro da semana
    vendas_semana = Venda.objects.filter(data_venda__date__range=[inicio_semana, fim_semana])

    # 🔹 Calcular Receita por Dia da Semana (Formato: {'03/03': 0, '04/03': 58, ...})
    receita_por_dia = {}
    for i in range(7):  # Segunda a Domingo
        dia = inicio_semana + timedelta(days=i)
        total_dia = vendas_semana.filter(data_venda__date=dia).aggregate(
            total=Sum(ExpressionWrapper(F('quantidade') * F('preco_unitario'), output_field=DecimalField()))
        )['total'] or 0  
        receita_por_dia[dia.strftime("%d/%m")] = float(total_dia)  # ✅ Converte Decimal para float

    # 🔹 Manter Receita em JSON para o Gráfico
    receita_por_dia_labels = json.dumps(list(receita_por_dia.keys()))  
    receita_por_dia_values = json.dumps(list(receita_por_dia.values()))  

    # 🔹 Faturamento total da semana
    receita_total = sum(receita_por_dia.values())

    # 🔹 Movimentações recentes (Paginação)
    movimentacoes_list = vendas_semana.annotate(
        valor_venda=ExpressionWrapper(F('quantidade') * F('preco_unitario'), output_field=DecimalField())
    ).order_by('-data_venda')

    paginator = Paginator(movimentacoes_list, 5)  # 🔹 Exibir 5 registros por página
    page_number = request.GET.get('page')  # 🔹 Obtém o número da página atual
    movimentacoes = paginator.get_page(page_number)  # 🔹 Retorna a página de registros

    # 🔹 Produtos com estoque baixo (menos de 5 unidades)
    produtos_baixo_estoque = Produto.objects.filter(estoque__lt=5).order_by('estoque')


    # 🔹 valor total do estoque (preco de custo)
    valor_total_estoque = Produto.objects.aggregate(
        total=Sum(ExpressionWrapper(F('preco_custo') * F('estoque'), output_field=DecimalField()))
    )['total'] or 0  
    
   # 🔹 Categorias mais vendidas
    categorias_vendas = vendas_semana.values('produto__categoria').annotate(
        total_vendido=Sum(F('quantidade') * F('preco_unitario'))
    ).order_by('-total_vendido')

    # 🔹 Criando um dicionário com todas as categorias
    categorias_disponiveis = dict(Produto.CATEGORIAS_CHOICES)
    categorias_dict = {nome: 0 for nome in categorias_disponiveis.values()}  # Inicia todas com 0

    for item in categorias_vendas:
        categoria_nome = categorias_disponiveis.get(item['produto__categoria'], 'Outros')
        categorias_dict[categoria_nome] = float(item['total_vendido'])

    categorias_labels = list(categorias_dict.keys())
    categorias_values = list(categorias_dict.values())  

    return render(request, 'inicio/dashboard.html', {
        'inicio_semana': inicio_semana,
        'fim_semana': fim_semana,
        'receita_por_dia_labels': receita_por_dia_labels,
        'receita_por_dia_values': receita_por_dia_values,
        'receita_semana': receita_total,
        'movimentacoes': movimentacoes,  
        'produtos_baixo_estoque': produtos_baixo_estoque,
        'valor_total_estoque': valor_total_estoque,
        'categorias_labels_vendas': json.dumps(categorias_labels),
        'categorias_values_vendas': json.dumps(categorias_values),
    })