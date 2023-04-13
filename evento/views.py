from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import Evento
from django.db.models import Q


@login_required(login_url='/usuario/logar/')
def novo_evento(request):
    if request.method == "GET":
        return render(request, 'novo_evento.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        data_inicio = request.POST.get('data_inicio')
        data_termino = request.POST.get('data_termino')
        carga_horaria = request.POST.get('carga_horaria')

        cor_principal = request.POST.get('cor_principal')
        cor_secundaria = request.POST.get('cor_secundaria')
        cor_fundo = request.POST.get('cor_fundo')
        
        logo = request.FILES.get('logo')

        if len(nome) == 0:
            messages.add_message(request, messages.WARNING, 'O campo nome é obrigatório')
            return redirect(reverse('novo_evento'))
        
        #TODO: Outras validações
        
        evento = Evento(
            criador=request.user,
            nome=nome,
            descricao=descricao,
            data_inicio=data_inicio,
            data_termino=data_termino,
            carga_horaria=carga_horaria,
            cor_principal=cor_principal,
            cor_secundaria=cor_secundaria,
            cor_fundo=cor_fundo,
            logo=logo,
        )
    
        evento.save()
        
        messages.add_message(request, messages.SUCCESS, 'Evento cadastrado com sucesso')
        return redirect(reverse('novo_evento'))

@login_required(login_url='/usuario/logar/')
def lista_eventos(request):
    if request.method == "GET":
        eventos = Evento.objects.filter(criador=request.user)
        nome = request.GET.get('nome')
        # data_inicio = request.GET.get('data_inicio')
        data = request.GET.get('data')
        status = request.GET.get('status')
        if nome:
            eventos = eventos.filter(nome__icontains=nome)

        # if data_inicio:
        #     eventos = eventos.filter(data_inicio__icontains=data_inicio)
        if data:
            eventos = eventos.filter(Q(data_inicio=data)|Q(data_termino=data))

        # if status:
        #     eventos = eventos.filter(status=status)

        lista_status = {'I': 'Inicializado', 'F': 'Finalizado'}

        context = {
            'nome': nome,
            # 'data_inicio': data_inicio,
            'data': data,
            'status': status,
            'eventos': eventos,
            'lista_status': lista_status
        }
        return render(request, 'lista_eventos.html', context)

@login_required(login_url='/usuario/logar/')
def ver_evento(request, id):
    pass
