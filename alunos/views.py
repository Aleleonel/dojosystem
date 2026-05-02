from django.shortcuts import render, get_object_or_404, redirect
from .models import Aluno
from .forms import AlunoForm
from django.utils import timezone
from .models import Frequencia
from django.db.models import Count
from django.utils import timezone


def lista_alunos(request):
    alunos = Aluno.objects.all()
    return render(request, 'alunos/lista.html', {'alunos': alunos})

def criar_aluno(request):
    form = AlunoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('lista_alunos')
    return render(request, 'alunos/form.html', {'form': form})

def editar_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)
    form = AlunoForm(request.POST or None, request.FILES or None, instance=aluno)
    if form.is_valid():
        form.save()
        return redirect('lista_alunos')
    return render(request, 'alunos/form.html', {'form': form})

def deletar_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)
    aluno.delete()
    return redirect('lista_alunos')

def registrar_frequencia(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)

    hoje = timezone.now().date()

    ja_registrado = Frequencia.objects.filter(aluno=aluno, data=hoje).exists()

    if not ja_registrado:
        Frequencia.objects.create(aluno=aluno)

    return redirect('lista_alunos')

def historico_frequencia(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    frequencias = Frequencia.objects.filter(aluno=aluno).order_by('-data')

    return render(request, 'alunos/historico.html', {
        'aluno': aluno,
        'frequencias': frequencias
    })

def leitor_qr(request):
    return render(request, 'alunos/leitor.html')


def checkin_qr(request, codigo):
    aluno = get_object_or_404(Aluno, codigo_barras=codigo)

    hoje = timezone.now().date()

    ja_registrado = Frequencia.objects.filter(aluno=aluno, data=hoje).exists()

    if not ja_registrado:
        Frequencia.objects.create(aluno=aluno)

    return redirect('lista_alunos')


def dashboard(request):

    hoje = timezone.now().date()

    total_alunos = Aluno.objects.count()
    alunos_ativos = Aluno.objects.filter(ativo=True).count()
    presencas_hoje = Frequencia.objects.filter(data=hoje).count()

    # Ranking de frequência
    ranking = (
        Frequencia.objects
        .values('aluno__nome')
        .annotate(total=Count('id'))
        .order_by('-total')[:5]
    )

    # Frequência por dia (últimos 7 dias)
    ultimos_dias = (
        Frequencia.objects
        .values('data')
        .annotate(total=Count('id'))
        .order_by('data')
    )

    return render(request, 'alunos/dashboard.html', {
        'total_alunos': total_alunos,
        'alunos_ativos': alunos_ativos,
        'presencas_hoje': presencas_hoje,
        'ranking': ranking,
        'ultimos_dias': ultimos_dias
    })