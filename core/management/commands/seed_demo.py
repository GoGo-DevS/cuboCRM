"""
Carga datos demo realistas para ver el CRM en acción.
Uso:  python manage.py seed_demo
Idempotente: usa get_or_create. Crea superusuario admin/admin si no existe.
"""
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from briefs.models import Brief
from clients.models import Client, Company
from finance.models import Payment
from leads.models import Lead
from portfolio.models import CaseStudy, Testimonial
from projects.models import Deliverable, Project, Revision

User = get_user_model()


class Command(BaseCommand):
    help = "Carga datos demo para Creative Growth CRM"

    def handle(self, *args, **options):
        hoy = date.today()

        admin, creado = User.objects.get_or_create(
            username="admin",
            defaults={"is_staff": True, "is_superuser": True, "email": "admin@cub.studio"},
        )
        if creado:
            admin.set_password("admin")
            admin.save()
            self.stdout.write(self.style.SUCCESS("Superusuario creado: admin / admin"))

        # ---------- LEADS ----------
        leads_data = [
            ("Valentina Soto", "Café Raíz", "Dueña", "instagram", "cotizacion", 850000),
            ("Matías Rojas", "Estudio Pilates Norte", "Socio", "referido", "reunion", 1200000),
            ("Camila Fuentes", "Joyería Lúcida", "Fundadora", "behance", "nuevo", 600000),
            ("Diego Araya", "TechBolt SpA", "CEO", "linkedin", "negociacion", 2400000),
            ("Fernanda Vidal", "Veterinaria Patitas", "Admin", "facebook", "contactado", 480000),
            ("Ignacio Pérez", "Brew & Co", "Gerente", "web", "brief_recibido", 1500000),
            ("Antonia Lagos", "Yoga Lila", "Profesora", "instagram", "perdido", 350000),
            ("Sebastián Núñez", "Constructora Andes", "Marketing", "referido", "ganado", 3200000),
        ]
        leads = []
        for nombre, empresa, cargo, fuente, estado, valor in leads_data:
            lead, _ = Lead.objects.get_or_create(
                nombre=nombre,
                defaults=dict(
                    empresa=empresa, cargo=cargo, fuente=fuente, estado=estado,
                    valor_estimado=Decimal(valor), whatsapp="+56912345678",
                    instagram="@" + empresa.lower().replace(" ", ""),
                    notas="Lead demo cargado por seed_demo.",
                ),
            )
            leads.append(lead)

        # ---------- CLIENTES ----------
        clientes_def = [
            ("Café Raíz", "Cafetería", "Valentina Soto"),
            ("Constructora Andes", "Construcción", "Sebastián Núñez"),
            ("Estudio Pilates Norte", "Fitness", "Matías Rojas"),
            ("Joyería Lúcida", "Retail", "Camila Fuentes"),
        ]
        clientes = {}
        for emp_nombre, rubro, contacto in clientes_def:
            empresa, _ = Company.objects.get_or_create(
                nombre=emp_nombre, defaults={"rubro": rubro, "ciudad": "Santiago"}
            )
            cliente, _ = Client.objects.get_or_create(
                nombre=contacto,
                defaults={"empresa": empresa, "email": contacto.split()[0].lower() + "@demo.cl",
                          "whatsapp": "+56987654321", "cargo": "Contacto principal"},
            )
            clientes[emp_nombre] = cliente

        # ---------- BRIEFS ----------
        brief, _ = Brief.objects.get_or_create(
            cliente=clientes["Café Raíz"], nombre_marca="Café Raíz",
            defaults=dict(
                rubro="Cafetería de especialidad", estado="aprobado",
                historia="Cafetería de barrio que nace del amor por el café de origen.",
                objetivos="Identidad cálida y artesanal que conecte con la comunidad.",
                publico_objetivo="Jóvenes profesionales 25-40, amantes del café.",
                personalidad="cálida, artesanal, cercana, premium",
                colores_deseados="terracota, verde oliva, crema",
                colores_prohibidos="neón, fucsia",
                tipografias="serif para títulos, sans para texto",
            ),
        )

        # ---------- PROYECTOS ----------
        proyectos_def = [
            ("Branding Café Raíz", "Café Raíz", "branding", "produccion", 850000, brief),
            ("Identidad Constructora Andes", "Constructora Andes", "branding", "entregado", 3200000, None),
            ("Reels Pilates Norte", "Estudio Pilates Norte", "redes", "feedback", 600000, None),
            ("Packaging Joyería Lúcida", "Joyería Lúcida", "packaging", "aprobado", 1100000, None),
        ]
        proyectos = {}
        for nombre, emp, tipo, estado, monto, br in proyectos_def:
            p, _ = Project.objects.get_or_create(
                nombre=nombre,
                defaults=dict(
                    cliente=clientes[emp], tipo=tipo, estado=estado,
                    monto=Decimal(monto), brief=br, responsable=admin,
                    fecha_inicio=hoy - timedelta(days=20),
                    fecha_entrega=hoy + timedelta(days=12),
                    descripcion="Proyecto demo generado por seed_demo.",
                ),
            )
            proyectos[nombre] = p

        # ---------- ENTREGABLES + REVISIONES ----------
        p_cafe = proyectos["Branding Café Raíz"]
        for nombre, tipo, estado in [
            ("Logotipo principal", "logo", "en_revision"),
            ("Manual de marca", "manual", "pendiente"),
            ("Mockups redes", "mockup", "en_proceso"),
        ]:
            d, creado_d = Deliverable.objects.get_or_create(
                proyecto=p_cafe, nombre=nombre,
                defaults={"tipo": tipo, "estado": estado, "responsable": admin, "fecha": hoy},
            )
            if creado_d and tipo == "logo":
                Revision.objects.create(
                    entregable=d, version="v1", estado="cambios", autor=admin,
                    comentarios="Cliente pide explorar versión más artesanal del isotipo.",
                )
                Revision.objects.create(
                    entregable=d, version="v2", estado="enviada", autor=admin,
                    comentarios="Segunda ronda con paleta terracota.",
                )

        # ---------- PAGOS ----------
        Payment.objects.get_or_create(
            proyecto=p_cafe, tipo="anticipo",
            defaults={"monto": Decimal(425000), "pagado": True, "fecha": hoy - timedelta(days=15), "metodo": "transferencia"},
        )
        Payment.objects.get_or_create(
            proyecto=p_cafe, tipo="saldo",
            defaults={"monto": Decimal(425000), "pagado": False, "metodo": "transferencia"},
        )
        p_andes = proyectos["Identidad Constructora Andes"]
        Payment.objects.get_or_create(
            proyecto=p_andes, tipo="unico",
            defaults={"monto": Decimal(3200000), "pagado": True, "fecha": hoy - timedelta(days=5), "metodo": "transferencia"},
        )

        # ---------- TESTIMONIO + CASO ----------
        testi, _ = Testimonial.objects.get_or_create(
            cliente=clientes["Constructora Andes"], proyecto=p_andes,
            defaults={
                "texto": "El estudio captó nuestra esencia desde la primera reunión. La nueva identidad nos posicionó como líderes.",
                "autor_nombre": "Sebastián Núñez", "autor_cargo": "Marketing, Constructora Andes",
                "rating": 5,
            },
        )
        CaseStudy.objects.get_or_create(
            proyecto=p_andes,
            defaults={
                "titulo": "Rebranding que posicionó a Constructora Andes",
                "descripcion": "Rediseño integral de identidad para una constructora con 15 años de trayectoria.",
                "resultados": "+40% de recordación de marca · nueva papelería y señalética · sitio web renovado.",
                "testimonio": testi, "publicado": True,
            },
        )

        self.stdout.write(self.style.SUCCESS(
            f"Demo lista: {Lead.objects.count()} leads · {Client.objects.count()} clientes · "
            f"{Project.objects.count()} proyectos · {Payment.objects.count()} pagos."
        ))
        self.stdout.write(self.style.WARNING("Entra con  admin / admin  en /login/"))
