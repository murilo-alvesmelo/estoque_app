from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("inicio.urls")), 
    path('produto/', include('produto.urls')),
    path('vendas/', include('vendas.urls')),
]
