from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    class RolInstitucional(models.TextChoices):
        ADMINISTRADOR = 'ADMIN', 'Administrador'
        ESTANDAR = 'ESTANDAR', 'Cliente'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil', verbose_name="Usuario")
    rut = models.CharField(max_length=12, unique=True, verbose_name="RUT (Ej: 12345678-9)")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono de contacto")
    rol_institucional = models.CharField(
        max_length=20, 
        choices=RolInstitucional.choices, 
        default=RolInstitucional.ESTANDAR, 
        verbose_name="Rol Institucional"
    )

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"

    def __str__(self):
        return f"{self.user.username} - RUT: {self.rut}"
