from django.db import models
from django.core.validators import MinValueValidator

class Genero(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")

    class Meta:
        verbose_name = "Género"
        verbose_name_plural = "Géneros"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Videojuego(models.Model):
    
    class EstadoJuego(models.TextChoices):
        DISPONIBLE = 'DISPONIBLE', 'Disponible'
        AGOTADO = 'AGOTADO', 'Agotado'

    class Plataforma(models.TextChoices):
        PC = 'PC', 'PC'
        PLAYSTATION = 'PS', 'PlayStation'
        XBOX = 'XBOX', 'Xbox'
        NINTENDO = 'SWITCH', 'Nintendo Switch'

    genero = models.ForeignKey(
        Genero, 
        on_delete=models.PROTECT, 
        related_name='videojuegos', 
        verbose_name="Género (Contexto)"
    )
    
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código Identificador")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug amigable")
    titulo = models.CharField(max_length=200, verbose_name="Título del videojuego")
    descripcion = models.TextField(verbose_name="Descripción detallada")
    desarrollador = models.CharField(max_length=150, verbose_name="Estudio desarrollador")
    precio = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.00)], 
        verbose_name="Precio"
    )
    
    plataforma = models.CharField(
        max_length=20, 
        choices=Plataforma.choices, 
        default=Plataforma.PC, 
        verbose_name="Plataforma"
    )

    stock = models.PositiveIntegerField(
        validators=[MinValueValidator(0)], 
        default=0, 
        verbose_name="Stock disponible"
    )
    
    estado = models.CharField(
        max_length=20, 
        choices=EstadoJuego.choices, 
        default=EstadoJuego.DISPONIBLE, 
        verbose_name="Estado operativo"
    )
    
    imagen = models.ImageField(
        upload_to='media/portadas', 
        blank=True, 
        null=True, 
        verbose_name="Portada"
    )
    
    activo = models.BooleanField(
        default=True, 
        verbose_name="Activo", 
        help_text="Desactivar para realizar baja lógica sin eliminar el registro."
    )
    
    creado = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    actualizado = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        verbose_name = "Videojuego"
        verbose_name_plural = "Videojuegos"
        ordering = ['-creado']

    def __str__(self):
        return f"{self.titulo} [{self.codigo}]"