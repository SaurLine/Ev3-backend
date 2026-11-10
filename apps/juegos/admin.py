from django.contrib import admin
from .models import Genero, Videojuego

admin.site.site_header = 'MamboStore - Panel de Control'
admin.site.site_title = 'MamboStore Admin'
admin.site.index_title = 'Gestión Operativa de Recursos y Servicios'



@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug')
    search_fields = ('nombre',)
    prepopulated_fields = {'slug': ('nombre',)}



@admin.register(Videojuego)
class VideojuegoAdmin(admin.ModelAdmin):

    list_display = ('codigo', 'titulo', 'genero', 'precio', 'stock', 'estado', 'activo')
    

    list_filter = ('genero', 'estado', 'activo', 'plataforma')
    

    search_fields = ('codigo', 'titulo', 'desarrollador', 'descripcion')
    

    list_editable = ('precio', 'stock', 'estado', 'activo')
    

    prepopulated_fields = {'slug': ('titulo',)}
    

    fieldsets = (
        ('Información Principal y Contexto', {
            'fields': (
                ('titulo', 'slug'),
                'codigo',
                'genero',
                'desarrollador'
            ),
            'description': 'Datos fundamentales de identificación y clasificación del recurso.'
        }),
        ('Inventario, Precios y Plataforma', {
            'fields': (
                ('precio', 'stock'),
                'plataforma'
            ),
            'description': 'Gestión cuantitativa de comercialización y plataforma compatible.'
        }),
        ('Estado y Vigencia Operativa', {
            'fields': (
                'estado',
                'activo'
            ),
            'description': 'Control del estado operativo en la tienda y baja lógica del registro.'
        }),
        ('Multimedia', {
            'fields': (
                'imagen',
            ),
            'classes': ('collapse',), 
            'description': 'Recurso visual de portada.'
        }),
    )