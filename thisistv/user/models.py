from django.db import models
from django.contrib.auth.models import User

# Create your models here.

TYPE_USER_CHOICES = (
    ('A', 'Administrador'),
    ('G', 'Gerente'),
    ('O', 'Operador'),
)


class UserProfile(models.Model):
    """
        Cadastro de Usuários
    """
    djuser = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="")
    type_user = models.CharField("Tipo de Usuário", max_length=1,
                            choices=TYPE_USER_CHOICES, default='O')

    def __str__(self):
        return self.djuser.username
