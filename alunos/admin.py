from django.contrib import admin
from .models import Aluno

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'graduacao', 'telefone', 'ativo')
    search_fields = ('nome', 'telefone')
    list_filter = ('graduacao', 'ativo')
