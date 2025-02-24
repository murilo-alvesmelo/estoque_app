from django.contrib import admin
from django.urls import path, include
from inicio.views.views import dashboard
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='home'),
    path('produto/', include('produto.urls')),
]
