from django.urls import path
from .views import views

urlpatterns = [
    path('', views.listar_produtos, name='listar_produtos'),
    path('novo/', views.criar_produto, name='criar_produto'),
    path('excluir/<int:id>/', views.excluir_produto, name='excluir_produto'),
    path('registrar-retirada/', views.registrar_retirada, name='registrar_retirada'),
    path('registrar-entrada/', views.registrar_entrada, name='registrar_entrada'),
]