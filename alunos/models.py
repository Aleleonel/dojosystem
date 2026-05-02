from io import BytesIO
from django.db import models
from django.utils import timezone
import qrcode
from django.core.files import File

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

    def __str__(self):
        return self.nome
    
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.qr_code:
            qr = qrcode.make(self.codigo_barras)

            buffer = BytesIO()
            qr.save(buffer, format='PNG')

            filename = f'aluno_{self.id}.png'
            self.qr_code.save(filename, File(buffer), save=False)

        super().save(*args, **kwargs)



class Frequencia(models.Model):

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    data = models.DateField(default=timezone.now)
    hora = models.TimeField(auto_now_add=True)

    class Meta:
        unique_together = ('aluno', 'data')  # evita duplicidade no mesmo dia

    def __str__(self):
        return f"{self.aluno.nome} - {self.data}"
    

