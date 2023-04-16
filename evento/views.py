import csv
import os
from secrets import token_urlsafe
from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from .models import Certificado, Evento
from django.db.models import Q
from io import BytesIO  
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image, ImageDraw, ImageFont
import sys


def define_contexto(request, eventos, titulo):
    nome = request.GET.get('nome')
    data = request.GET.get('data')
    status = request.GET.get('status')
    if nome:
        eventos = eventos.filter(nome__icontains=nome)

    if data:
        eventos = eventos.filter(Q(data_inicio=data)|Q(data_termino=data))

    if status:
        eventos = eventos.filter(status=status)

    lista_status = {'I': 'Inicializado', 'F': 'Finalizado'}

    context = {
        'titulo': titulo,
        'nome': nome,
        'data': data,
        'status': status,
        'eventos': eventos,
        'lista_status': lista_status
    }

    return context

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
def lista_todos(request):
    titulo = 'Eventos em geral'
    if request.method == "GET":
        eventos = Evento.objects.all()

        context = define_contexto(request, eventos, titulo)

        return render(request, 'lista_eventos.html', context)

@login_required(login_url='/usuario/logar/')
def lista_meus_eventos(request):
    titulo = 'Meus eventos'
    if request.method == "GET":
        eventos = Evento.objects.filter(criador=request.user)

        context = define_contexto(request, eventos, titulo)

        return render(request, 'lista_eventos.html', context)

@login_required(login_url='/usuario/logar/')
def lista_terceiros(request):
    titulo = 'Eventos de terceiros'
    if request.method == "GET":
        eventos = Evento.objects.exclude(criador=request.user)

        context = define_contexto(request, eventos, titulo)

        return render(request, 'lista_eventos.html', context)

@login_required(login_url='/usuario/logar/')
def lista_minhas_participacoes(request):
    titulo = 'Minhas participações'
    if request.method == "GET":
        eventos = request.user.evento_participantes.all()

        context = define_contexto(request, eventos, titulo)

        return render(request, 'lista_eventos.html', context)

@login_required(login_url='/usuario/logar/')
def ver_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if request.method == "GET":
        return render(request,'ver_evento.html', {'evento': evento})
    elif request.method == "POST":
        if request.user in evento.participantes.all():
            messages.add_message(request, messages.WARNING, 'Participante já inscrito neste evento!')
            return redirect(reverse('ver_evento', kwargs={'id': id}))
    
        evento.participantes.add(request.user)
        evento.save()

        messages.add_message(request, messages.SUCCESS, 'Inscrição realizada com sucesso.')
        return redirect(reverse('ver_evento', kwargs={'id': id}))

@login_required(login_url='/usuario/logar/')
def participantes_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if not evento.criador == request.user:
        raise Http404('Este evento não lhe pertence!')
    
    if request.method == "GET":
        participantes = evento.participantes.all()[:3]
        return render(request, 'participantes_evento.html', {'evento': evento, 'participantes': participantes})

@login_required(login_url='/usuario/logar/')
def exportar_csv(request, id):
    evento = get_object_or_404(Evento, id=id)
    if not evento.criador == request.user:
        raise Http404('Este evento não lhe pertence!')
    
    participantes = evento.participantes.all()
    
    token = f'csv/{token_urlsafe(6)}.csv'
    path = os.path.join(settings.MEDIA_ROOT, token)

    with open(path, 'w') as arq:
        writer = csv.writer(arq, delimiter=";")
        for participante in participantes:
            x = (participante.username, participante.email)
            writer.writerow(x)

    return redirect(f'/media/{token}')

@login_required(login_url='/usuario/logar/')
def certificados_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if not evento.criador == request.user:
        raise Http404('Este evento não lhe pertence!')
    if request.method == "GET":
        qtd_certificados = evento.participantes.all().count() - Certificado.objects.filter(evento=evento).count()
        return render(request, 'certificados_evento.html', {'evento': evento, 'qtd_certificados': qtd_certificados})

@login_required(login_url='/usuario/logar/')
def gerar_certificado(request, id):
    evento = get_object_or_404(Evento, id=id)
    if not evento.criador == request.user:
        raise Http404('Este evento não lhe pertence!')

    path_template = os.path.join(settings.BASE_DIR, 'templates/static/evento/img/template_certificado.png')
    path_fonte = os.path.join(settings.BASE_DIR, 'templates/static/fontes/arimo.ttf')

    contador = 0
    for participante in evento.participantes.all():
        if not Certificado.objects.filter(participante=participante).filter(evento=evento).exists():
            img = Image.open(path_template)
            draw = ImageDraw.Draw(img)
            fonte_nome = ImageFont.truetype(path_fonte, 80)
            fonte_info = ImageFont.truetype(path_fonte, 40)
            draw.text((224, 630), f"{participante.username}", font=fonte_nome, fill=(0, 0, 0))
            draw.text((761, 764), f"{evento.nome}", font=fonte_info, fill=(0, 0, 0))
            draw.text((816, 834), f"{evento.carga_horaria} horas", font=fonte_info, fill=(0, 0, 0))
            output = BytesIO()
            img.save(output, format="PNG", quality=100)
            output.seek(0)
            img_final = InMemoryUploadedFile(output,
                                            'ImageField',
                                            f'{token_urlsafe(8)}.png',
                                            'image/jpeg',
                                            sys.getsizeof(output),
                                            None)
            certificado_gerado = Certificado(
                certificado=img_final,
                participante=participante,
                evento=evento,
            )
            certificado_gerado.save()
            contador += 1
    
    if contador > 0:
        msg = 'certificados gerados' if contador > 1 else 'certificado gerado'
        messages.add_message(request, messages.SUCCESS, f'{contador} {msg}.')
    else:
        messages.add_message(request, messages.WARNING, 'Nenhum certificado foi gerado!')

    return redirect(reverse('certificados_evento', kwargs={'id': evento.id}))

@login_required(login_url='/usuario/logar/')
def buscar_certificado(request, id):
    evento = get_object_or_404(Evento, id=id)
    if not evento.criador == request.user:
        raise Http404('Este evento não lhe pertence!')
    
    email = request.POST.get('email')
    certificado = Certificado.objects.filter(evento=evento).filter(participante__email=email).first()
    if not certificado:
        messages.add_message(request, messages.WARNING, 'Certificado não localizado!')
        return redirect(reverse('certificados_evento', kwargs={'id': evento.id}))
    
    return redirect(certificado.certificado.url)

