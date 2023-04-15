from django.urls import path
from . import views

urlpatterns = [
    path('todos/', views.lista_todos, name='lista_todos'),
    path('minha_lista/', views.lista_meus_eventos, name='lista_meus_eventos'),
    path('minhas_participacoes/', views.lista_minhas_participacoes, name='lista_minhas_participacoes'),
    path('lista_de_terceiros/', views.lista_terceiros, name='lista_terceiros'),
    path('novo/', views.novo_evento, name='novo_evento'),
    path('<int:id>/ver/', views.ver_evento, name='ver_evento'),
    path('<int:id>/participantes/', views.participantes_evento, name='participantes_evento'),
    path('<int:id>/exportar_csv/', views.exportar_csv, name="exportar_csv"),
]
