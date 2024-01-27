from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from receitas.models import Receita
from usuarios.views import dashboard


def index(request):
    receitas = Receita.objects.order_by('-data_receita').filter(publicada=True)
    paginator = Paginator(receitas, 3)
    page = request.GET.get('page')
    receitas_por_pagina = paginator.get_page(page)

    dados = {
        'receitas': receitas_por_pagina
    }

    return render(request, 'receitas/index.html', context=dados)


def receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id, publicada=True)
    
    dados_receita = {
        'receita': receita
    }
    
    return render(request, 'receitas/receita.html', dados_receita)


def criar_receita(request):
    if request.method == 'POST':
        nome_receita  = request.POST['nome_receita']
        ingredientes  = request.POST['ingredientes']
        modo_preparo  = request.POST['modo_preparo']
        tempo_preparo = request.POST['tempo_preparo']
        rendimento    = request.POST['rendimento']
        categoria     = request.POST['categoria']
        foto_receita  = request.FILES['foto_receita']

        pessoa = get_object_or_404(User, pk=request.user.id)
        receita = Receita.objects.create(pessoa=pessoa, nome_receita=nome_receita, ingredientes=ingredientes,
                                         modo_preparo=modo_preparo, tempo_preparo=tempo_preparo, rendimento=rendimento,
                                         categoria=categoria, foto=foto_receita)
        receita.save()
        messages.success(request, f'A receita "{nome_receita}" foi registrada com sucesso')
        return redirect(dashboard)

    return render(request, 'receitas/form_edita_receita.html')


def deletar_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    nome_receita = receita.nome_receita
    receita.delete()
    messages.success(request, f'A receita "{nome_receita}" foi removida com sucesso')
    return redirect('dashboard')


def editar_receita(request, receita_id):
    
    receita = get_object_or_404(Receita, pk=receita_id)

    dados = {
        'receita': receita
    }

    return render(request, 'receitas/form_edita_receita.html', dados)


def atualizar_receita(request):
    if request.method == 'POST':
        receita_id  = request.POST['receita_id']
        receita = get_object_or_404(Receita, pk=receita_id)

        receita.nome_receita  = request.POST['nome_receita']
        receita.ingredientes  = request.POST['ingredientes']
        receita.modo_preparo  = request.POST['modo_preparo']
        receita.tempo_preparo = request.POST['tempo_preparo']
        receita.rendimento    = request.POST['rendimento']
        receita.categoria     = request.POST['categoria']
        if 'foto_receita' in request.FILES:
            receita.foto          = request.FILES['foto_receita']
        receita.save()

        messages.success(request, f'A receita foi atualizada com sucesso')

        return redirect('dashboard')
