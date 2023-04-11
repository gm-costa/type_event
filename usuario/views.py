from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


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
            messages.add_message(request, messages.WARNING, 'Todos os campos são obrigatórios!')
            # return redirect(reverse('cadastro'))
            return render(request, 'cadastro.html', context)

        if not (senha == confirmar_senha):    
            messages.add_message(request, messages.WARNING, 'Senhas diferentes!')
            return render(request, 'cadastro.html', context)
        
        user = User.objects.filter(username=username)

        if user.exists():
            messages.add_message(request, messages.WARNING, 'Usuário já cadastrado!')
            return render(request, 'cadastro.html', context)  
        
        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()
        return redirect(reverse('logar'))

def logar(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if not user:
            messages.add_message(request, messages.ERROR, 'Usuário ou senha inválidos')
            return render(request, 'login.html', {'username': username, 'senha': senha})
        
        login(request, user)
        # return HttpResponse('logado')
        return redirect('/eventos/novo/')


def sair(request):
    logout(request)
    return redirect(reverse('logar'))
