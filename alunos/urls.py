
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.lista_alunos, name='lista_alunos'),
    path('novo/', views.criar_aluno, name='criar_aluno'),
    path('editar/<int:id>/', views.editar_aluno, name='editar_aluno'),
    path('deletar/<int:id>/', views.deletar_aluno, name='deletar_aluno'),
    path('presenca/<int:aluno_id>/', views.registrar_frequencia, name='registrar_frequencia'),
    path('historico/<int:aluno_id>/', views.historico_frequencia, name='historico_frequencia'),
    path('leitor/', views.leitor_qr, name='leitor_qr'),
    path('checkin/<str:codigo>/', views.checkin_qr, name='checkin_qr'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('usuarios/cadastro/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin/painel/', views.painel_admin, name='painel_admin'),
    path('academia/cadastro/', views.cadastrar_academia, name='cadastrar_academia'),
    
]