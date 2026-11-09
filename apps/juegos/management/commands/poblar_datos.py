from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tu_app.models import Genero, Videojuego
from decimal import Decimal

class Command(BaseCommand):
    help = 'Pobla la base de datos con 4 géneros, 8 videojuegos alineados al modelo y usuarios (admin y estándar).'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Iniciando proceso de población de datos...'))

        # 1. Creación de Usuarios de Prueba (Admin y Estándar)
        admin_user, created_admin = User.objects.get_or_create(
            username='admin_tienda',
            defaults={
                'email': 'admin@tiendajuegos.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created_admin:
            admin_user.set_password('admin1234')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('-> Usuario administrador creado: admin_tienda / admin1234'))
        else:
            self.stdout.write('-> El usuario administrador ya existía.')

        std_user, created_std = User.objects.get_or_create(
            username='cliente_estandar',
            defaults={
                'email': 'cliente@tiendajuegos.com',
                'is_staff': False,
                'is_superuser': False
            }
        )
        if created_std:
            std_user.set_password('cliente1234')
            std_user.save()
            self.stdout.write(self.style.SUCCESS('-> Usuario estándar creado: cliente_estandar / cliente1234'))
        else:
            self.stdout.write('-> El usuario estándar ya existía.')

        # 2. Creación de 4 Clasificadores (Géneros)
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

        # 3. Creación de 8 Entidades Principales (Videojuegos)
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
                "activo": False  # Ejemplo de registro con baja lógica (activo=False)
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