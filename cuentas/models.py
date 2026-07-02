from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class UsuarioManager(BaseUserManager):
    def create_user(self, documento, nombre_completo, sexo, password=None):
        if not documento:
            raise ValueError("El documento de identidad es obligatorio")
        usuario = self.model(
            documento=documento,
            nombre_completo=nombre_completo,
            sexo=sexo,
        )
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, documento, nombre_completo, sexo, password=None):
        usuario = self.create_user(documento, nombre_completo, sexo, password)
        usuario.is_staff = True
        usuario.is_superuser = True
        usuario.save(using=self._db)
        return usuario


class Usuario(AbstractBaseUser, PermissionsMixin):
    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    )

    documento = models.CharField(max_length=20, unique=True, verbose_name="Documento de identidad")
    nombre_completo = models.CharField(max_length=150, verbose_name="Nombre completo")
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, verbose_name="Sexo")
    fecha_registro = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'documento'
    REQUIRED_FIELDS = ['nombre_completo', 'sexo']

    def __str__(self):
        return f"{self.nombre_completo} ({self.documento})"
