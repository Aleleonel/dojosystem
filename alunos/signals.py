import uuid
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Perfil, Academia

@receiver(post_save, sender=User)
def criar_perfil(sender, instance, created, **kwargs):
    if created:

        # 👑 SUPERUSER = DONO
        if instance.is_superuser:

            academia = Academia.objects.create(
                razao_social=f"Academia {instance.username} LTDA",
                nome_fantasia=f"Academia {instance.username}",
                cnpj=uuid.uuid4().hex[:14]
            )

            Perfil.objects.create(
                user=instance,
                academia=academia,
                tipo='dono'
            )

        else:
            # 🥋 PROFESSOR (sem academia ainda)
            Perfil.objects.create(
                user=instance,
                tipo='professor'
            )