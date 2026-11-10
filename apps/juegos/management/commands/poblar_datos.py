from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.usuarios.models import PerfilUsuario
from apps.juegos.models import Genero, Videojuego  
from decimal import Decimal

class Command(BaseCommand):
    help = 'Pobla la base de datos con el usuario administrador, perfiles, géneros y videojuegos de prueba.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Iniciando proceso de población de datos...'))


        admin_user, created = User.objects.get_or_create(
            username='admin_tienda',
            defaults={
                'email': 'admin@tiendajuegos.com', 
                'first_name': 'Administrador',
                'is_staff': True, 
                'is_superuser': True
            }
        )
        admin_user.set_password('admin1234')
        admin_user.save()


        PerfilUsuario.objects.get_or_create(
            user=admin_user,
            defaults={
                'rut': '12345678-9', 
                'telefono': '+56911111111', 
                'rol_institucional': PerfilUsuario.RolInstitucional.ADMINISTRADOR
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('-> Administrador creado: admin_tienda / admin1234'))
        else:
            self.stdout.write('-> El administrador ya existía.')


        generos_data = [
            {"nombre": "Acción y Aventura", "slug": "accion-y-aventura"},
            {"nombre": "Rol (RPG)", "slug": "rol-rpg"},
            {"nombre": "Estrategia", "slug": "estrategia"},
            {"nombre": "Deportes", "slug": "deportes"}
        ]

        generos_objs = {}
        for g_data in generos_data:
            gen, _ = Genero.objects.get_or_create(
                slug=g_data["slug"],
                defaults={"nombre": g_data["nombre"]}
            )
            generos_objs[g_data["slug"]] = gen
        self.stdout.write(self.style.SUCCESS(f'-> {len(generos_data)} géneros asegurados.'))


        juegos_data = [
            {
                "codigo": "ACC-001",
                "slug": "shadow-chronicles",
                "titulo": "Shadow Chronicles",
                "descripcion": "Una aventura épica en un mundo cyberpunk asediado por corporaciones.",
                "desarrollador": "NeonByte Studios",
                "precio": Decimal("39.99"),
                "plataforma": Videojuego.Plataforma.PLAYSTATION,
                "stock": 15,
                "estado": Videojuego.EstadoJuego.DISPONIBLE,
                "genero_slug": "accion-y-aventura",
                "activo": True
            },
            {
                "codigo": "ACC-002",
                "slug": "mystic-quest",
                "titulo": "Mystic Quest Remastered",
                "descripcion": "Explora ruinas ancestrales resolviendo acertijos y combatiendo bestias.",
                "desarrollador": "Artifact Games",
                "precio": Decimal("24.50"),
                "plataforma": Videojuego.Plataforma.NINTENDO,
                "stock": 0,
                "estado": Videojuego.EstadoJuego.AGOTADO,
                "genero_slug": "accion-y-aventura",
                "activo": True
            },
            {
                "codigo": "RPG-001",
                "slug": "chronos-of-eloria",
                "titulo": "Chronos of Eloria",
                "descripcion": "RPG de mundo abierto con un sistema de decisiones ramificadas.",
                "desarrollador": "Solaria Soft",
                "precio": Decimal("59.99"),
                "plataforma": Videojuego.Plataforma.PC,
                "stock": 25,
                "estado": Videojuego.EstadoJuego.DISPONIBLE,
                "genero_slug": "rol-rpg",
                "activo": True
            },
            {
                "codigo": "RPG-002",
                "slug": "stellar-legends",
                "titulo": "Stellar Legends Online",
                "descripcion": "Alinea tu facción estelar y conquista sistemas solares enteros.",
                "desarrollador": "Galaxy Interactive",
                "precio": Decimal("49.99"),
                "plataforma": Videojuego.Plataforma.XBOX,
                "stock": 8,
                "estado": Videojuego.EstadoJuego.DISPONIBLE,
                "genero_slug": "rol-rpg",
                "activo": True
            },
            {
                "codigo": "EST-001",
                "slug": "tactical-command",
                "titulo": "Tactical Command 2088",
                "descripcion": "Estrategia militar por turnos con físicas de terreno avanzadas.",
                "desarrollador": "WarSim Labs",
                "precio": Decimal("29.99"),
                "plataforma": Videojuego.Plataforma.PC,
                "stock": 12,
                "estado": Videojuego.EstadoJuego.DISPONIBLE,
                "genero_slug": "estrategia",
                "activo": True
            },
            {
                "codigo": "EST-002",
                "slug": "empire-architect",
                "titulo": "Empire Architect",
                "descripcion": "Diseña, gestiona y defiende tu propia metrópolis medieval.",
                "desarrollador": "BrickHouse Games",
                "precio": Decimal("19.99"),
                "plataforma": Videojuego.Plataforma.PC,
                "stock": 0,
                "estado": Videojuego.EstadoJuego.AGOTADO,
                "genero_slug": "estrategia",
                "activo": True
            },
            {
                "codigo": "DEP-001",
                "slug": "super-striker-league",
                "titulo": "Super Striker League",
                "descripcion": "Fútbol arcade futurista con potenciadores y estadios flotantes.",
                "desarrollador": "ArcadeSports Co.",
                "precio": Decimal("29.99"),
                "plataforma": Videojuego.Plataforma.NINTENDO,
                "stock": 5,
                "estado": Videojuego.EstadoJuego.DISPONIBLE,
                "genero_slug": "deportes",
                "activo": True
            },
            {
                "codigo": "DEP-002",
                "slug": "pro-extreme-tennis",
                "titulo": "Pro Extreme Tennis",
                "descripcion": "Simulador de tenis realista con torneos globales en línea.",
                "desarrollador": "CourtMaster Software",
                "precio": Decimal("34.99"),
                "plataforma": Videojuego.Plataforma.PLAYSTATION,
                "stock": 0,
                "estado": Videojuego.EstadoJuego.AGOTADO,
                "genero_slug": "deportes",
                "activo": True
            },
        ]

        for j_data in juegos_data:
            genero_obj = generos_objs[j_data.pop("genero_slug")]
            Videojuego.objects.update_or_create(
                codigo=j_data["codigo"],
                defaults={**j_data, "genero": genero_obj}
            )

        self.stdout.write(self.style.SUCCESS(f'-> {len(juegos_data)} videojuegos creados o actualizados correctamente.'))
        self.stdout.write(self.style.SUCCESS('¡Población de datos finalizada con éxito!'))