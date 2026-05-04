from django.contrib import admin
from .models import Aluno

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'graduacao', 'telefone', 'ativo')
    search_fields = ('nome', 'telefone')
    list_filter = ('graduacao', 'ativo')

from django.utils.html import format_html

def qr_preview(self, obj):
    if obj.qr_code:
        return format_html(f'<img src="{obj.qr_code.url}" width="100"/>')
    return "-"

qr_preview.short_description = "QR Code"