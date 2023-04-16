from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from evento.models import Certificado


@login_required(login_url='/usuario/logar/')
def meus_certificados(request):
    certificados = Certificado.objects.filter(participante=request.user)
    return render(request, 'meus_certificados.html', {'certificados': certificados})
