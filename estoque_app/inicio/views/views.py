from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from produto.models.models import Produto, Retirada

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
    produtos = Produto.objects.all()
    movimentacoes = Retirada.objects.all().order_by('-data_retirada')[:10]

    context = {
        'produtos': produtos,
        'movimentacoes': movimentacoes
    }
    return render(request, 'inicio/dashboard.html', context)