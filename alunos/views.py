from django.shortcuts import render, get_object_or_404, redirect
from .models import Aluno
from .forms import AlunoForm
from django.utils import timezone
from .models import Frequencia
from django.db.models import Count
from django.contrib.auth import login
from .forms import UsuarioForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from .forms import AcademiaForm
from .models import Perfil, Academia


def dono_required(view_func):
    def wrapper(request, *args, **kwargs):
        perfil = getattr(request.user, 'perfil', None)

        if not perfil or perfil.tipo != 'dono':
            raise PermissionDenied

        return view_func(request, *args, **kwargs)
    return wrapper


def get_perfil(request):
    perfil = getattr(request.user, 'perfil', None)

    if not perfil:
        academia = Academia.objects.first()
        perfil = Perfil.objects.create(
            user=request.user,
            academia=academia,
            tipo='professor'
        )

    return perfil



@login_required
def cadastrar_academia(request):
    form = AcademiaForm(request.POST or None)

    if form.is_valid():
        academia = form.save()

        # vincula academia ao usuário logado
        perfil, criado = Perfil.objects.get_or_create(user=request.user)

        perfil.academia = academia
        perfil.save()

        return redirect('dashboard')

    return render(request, 'academia/cadastro.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True

@login_required
@dono_required
def painel_admin(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    hoje = timezone.now().date()

    total_usuarios = User.objects.count()
    total_professores = User.objects.filter(is_staff=True).count()
    total_alunos = Aluno.objects.count()
    presencas_hoje = Frequencia.objects.filter(data=hoje).count()

    # Ranking de alunos
    ranking = (
        Frequencia.objects
        .values('aluno__nome')
        .annotate(total=Count('id'))
        .order_by('-total')[:5]
    )

    # Frequência por dia
    frequencia_dias = (
        Frequencia.objects
        .values('data')
        .annotate(total=Count('id'))
        .order_by('data')
    )

    context = {
        'total_usuarios': total_usuarios,
        'total_professores': total_professores,
        'total_alunos': total_alunos,
        'presencas_hoje': presencas_hoje,
        'ranking': ranking,
        'frequencia_dias': frequencia_dias,
    }

    return render(request, 'admin/painel.html', context)

@login_required
def lista_alunos(request):
    perfil = get_perfil(request)

    alunos = Aluno.objects.filter(academia=perfil.academia)

    return render(request, 'alunos/lista.html', {'alunos': alunos})

@login_required
def criar_aluno(request):
    perfil = request.user.perfil

    form = AlunoForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        aluno = form.save(commit=False)
        aluno.usuario = request.user
        aluno.academia = perfil.academia
        aluno.save()

        return redirect('lista_alunos')

    return render(request, 'alunos/form.html', {'form': form})

@login_required
def editar_aluno(request, id):   
    aluno = get_object_or_404(Aluno, id=id, usuario=request.user)

    form = AlunoForm(request.POST or None, request.FILES or None, instance=aluno)
    if form.is_valid():
        form.save()
        return redirect('lista_alunos')
    return render(request, 'alunos/form.html', {'form': form})

@login_required
def deletar_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id, usuario=request.user)
    aluno.delete()
    return redirect('lista_alunos')

@login_required
def registrar_frequencia(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id, usuario=request.user)

    hoje = timezone.now().date()

    ja_registrado = Frequencia.objects.filter(aluno=aluno, data=hoje).exists()

    if not ja_registrado:
        Frequencia.objects.create(aluno=aluno)

    return redirect('lista_alunos')

@login_required
def historico_frequencia(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id, usuario=request.user)
    frequencias = Frequencia.objects.filter(aluno=aluno).order_by('-data')

    return render(request, 'alunos/historico.html', {
        'aluno': aluno,
        'frequencias': frequencias
    })

@login_required
def leitor_qr(request):
    return render(request, 'alunos/leitor.html')

@login_required
def checkin_qr(request, codigo):
    perfil = get_perfil(request)

    aluno = get_object_or_404(
        Aluno,
        codigo_barras=codigo,
        academia=perfil.academia
    )

    hoje = timezone.now().date()

    ja_registrado = Frequencia.objects.filter(
        aluno=aluno,
        data=hoje
    ).exists()

    if not ja_registrado:
        Frequencia.objects.create(aluno=aluno)

    return redirect('lista_alunos')

@login_required
def dashboard(request):

    perfil = get_perfil(request)
    hoje = timezone.now().date()

    total_alunos = Aluno.objects.filter(
        academia=perfil.academia
    ).count()

    alunos_ativos = Aluno.objects.filter(
        academia=perfil.academia,
        ativo=True
    ).count()

    presencas_hoje = Frequencia.objects.filter(
        aluno__academia=perfil.academia,
        data=hoje
    ).count()

    ranking = (
        Frequencia.objects
        .filter(aluno__academia=perfil.academia)
        .values('aluno__nome')
        .annotate(total=Count('id'))
        .order_by('-total')[:5]
    )

    ultimos_dias = (
        Frequencia.objects
        .filter(aluno__academia=perfil.academia)
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


@login_required
def cadastrar_usuario(request):

    if request.method == 'POST':
        form = UsuarioForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()

            return redirect('login')
        else:
            print(form.errors)  # 👈 DEBUG

    else:
        form = UsuarioForm()

    return render(request, 'usuarios/cadastro.html', {'form': form})