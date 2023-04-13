from django.urls import path
from . import views

urlpatterns = [
    path('lista/', views.lista_eventos, name='lista_eventos'),
    path('novo/', views.novo_evento, name='novo_evento'),
    path('ver_evento/<int:id>', views.ver_evento, name='ver_evento'),
]
