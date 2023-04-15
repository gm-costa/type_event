from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# from .utils import verificar_forca_senha


def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        context = {
            'username': username,
            'email': email,
            'senha': senha,
            'confirmar_senha': confirmar_senha
        }

        if len(username) == 0 or len(email) == 0 or len(senha) == 0:
            messages.add_message(request, messages.INFO, 'Todos os campos são obrigatórios!')
            # return redirect(reverse('cadastro'))
            return render(request, 'cadastro.html', context)

        if not (senha == confirmar_senha):    
            messages.add_message(request, messages.ERROR, 'Senhas diferentes!')
            return render(request, 'cadastro.html', context)
        
        if len(senha) > 20:    
            messages.add_message(request, messages.ERROR, 'A senha deve ter no máximo 20 caracteres!')
            return render(request, 'cadastro.html', context)
        
        # forca_senha = verificar_forca_senha(senha)
        
        user = User.objects.filter(username=username)

        if user.exists():
            messages.add_message(request, messages.INFO, 'Usuário já cadastrado!')
            return render(request, 'cadastro.html', context)  
        
        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Usuário cadastrado com sucesso.')
        return redirect(reverse('logar'))

def logar(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if not user:
            messages.add_message(request, messages.ERROR, 'Usuário ou senha inválidos!')
            return render(request, 'login.html', {'username': username, 'senha': senha})
        
        login(request, user)
        return redirect(reverse('lista_meus_eventos'))

def sair(request):
    logout(request)
    return redirect(reverse('logar'))
