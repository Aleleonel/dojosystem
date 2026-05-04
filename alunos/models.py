from io import BytesIO
from django.db import models
from django.utils import timezone
import qrcode
from django.core.files import File
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
import uuid



class Academia(models.Model):

    # 🏢 DADOS EMPRESARIAIS
    razao_social = models.CharField(max_length=200, blank=True, null=True)
    nome_fantasia = models.CharField(max_length=150, blank=True, null=True)
    cnpj = models.CharField(max_length=18, blank=True, null=True)
    inscricao_estadual = models.CharField(max_length=50, blank=True, null=True)

    # 👤 RESPONSÁVEL
    responsavel = models.CharField(max_length=150, null=True, blank=True)

    # 📞 CONTATO
    email = models.EmailField(blank=True, null=True)
    telefone_comercial = models.CharField(max_length=20, null=True, blank=True)

    # 📍 ENDEREÇO
    cep = models.CharField(max_length=10, null=True, blank=True)
    endereco = models.CharField(max_length=200, null=True, blank=True)
    numero = models.CharField(max_length=10, null=True, blank=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    estado = models.CharField(max_length=2, null=True, blank=True)

    # ⚙️ CONTROLE
    ativa = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_fantasia or self.razao_social or "Academia"

class Perfil(models.Model):

    TIPO_USUARIO = [
        ('dono', 'Dono'),
        ('professor', 'Professor'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    academia = models.ForeignKey(Academia, on_delete=models.CASCADE, null=True, blank=True)

    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO, default='professor')

    def __str__(self):
        return f"{self.user.username} - {self.tipo}"


class Aluno(models.Model):

    GRADUACAO_CHOICES = [
        ('branca', 'Faixa Branca'),
        ('azul', 'Faixa Azul'),
        ('roxa', 'Faixa Roxa'),
        ('marrom', 'Faixa Marrom'),
        ('preta', 'Faixa Preta'),
    ]

    nome = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=20)
    data_nascimento = models.DateField()
    data_matricula = models.DateField(auto_now_add=True)

    graduacao = models.CharField(max_length=10, choices=GRADUACAO_CHOICES)

    foto = models.ImageField(upload_to='alunos/', blank=True, null=True)

    ativo = models.BooleanField(default=True)

    codigo_barras = models.CharField(max_length=50, unique=True)

   # usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # 👈 NOVO CAMPO
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    academia = models.ForeignKey(Academia, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.nome
    
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True)

    def gerar_codigo_unico(self):
        while True:
            codigo = uuid.uuid4().hex[:10]
            if not Aluno.objects.filter(codigo_barras=codigo).exists():
                return codigo

    def save(self, *args, **kwargs):

        if not self.codigo_barras:
            self.codigo_barras = self.gerar_codigo_unico()

        criando = self._state.adding

        super().save(*args, **kwargs)

        if criando and not self.qr_code:
            url = reverse('checkin_qr', args=[self.codigo_barras])
            dominio = settings.DOMINIO

            qr = qrcode.make(f"{dominio}{url}")

            buffer = BytesIO()
            qr.save(buffer, format='PNG')

            filename = f'aluno_{self.id}.png'
            self.qr_code.save(filename, File(buffer), save=False)

            super().save(update_fields=['qr_code'])



class Frequencia(models.Model):

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    data = models.DateField(default=timezone.now)
    hora = models.TimeField(auto_now_add=True)

    class Meta:
        unique_together = ('aluno', 'data')  # evita duplicidade no mesmo dia

    def __str__(self):
        return f"{self.aluno.nome} - {self.data}"
    

