from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('receita/<int:receita_id>', receita, name='receita'),
    path('buscar', buscar, name='buscar'),
    path('criar/receita', criar_receita, name='criar_receita'),
    path('deletar/receita/<int:receita_id>', deletar_receita, name='deletar_receita'),
    path('editar/receita/<int:receita_id>', editar_receita, name='editar_receita'),
    path('atualizar/receita', atualizar_receita, name='atualizar_receita'),
]