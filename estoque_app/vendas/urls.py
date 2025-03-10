from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_venda, name='registrar_venda'),
    path('listar/', views.listar_vendas, name='listar_vendas'),
]