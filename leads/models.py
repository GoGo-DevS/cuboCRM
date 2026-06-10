from django.db import models
from django.urls import reverse

from core.models import TimeStampedModel


class Lead(TimeStampedModel):
    class Fuente(models.TextChoices):
        INSTAGRAM = "instagram", "Instagram"
        BEHANCE = "behance", "Behance"
        LINKEDIN = "linkedin", "LinkedIn"
        WEB = "web", "Web"
        REFERIDO = "referido", "Referido"
        FACEBOOK = "facebook", "Facebook"
        OTRO = "otro", "Otro"

    class Estado(models.TextChoices):
        NUEVO = "nuevo", "Nuevo"
        CONTACTADO = "contactado", "Contactado"
        REUNION = "reunion", "Reunión Agendada"
        BRIEF_SOLICITADO = "brief_solicitado", "Brief Solicitado"
        BRIEF_RECIBIDO = "brief_recibido", "Brief Recibido"
        COTIZACION = "cotizacion", "Cotización Enviada"
        NEGOCIACION = "negociacion", "Negociación"
        GANADO = "ganado", "Ganado"
        PERDIDO = "perdido", "Perdido"

    # Orden de columnas del Kanban (estados activos del pipeline).
    PIPELINE = [
        Estado.NUEVO,
        Estado.CONTACTADO,
        Estado.REUNION,
        Estado.BRIEF_SOLICITADO,
        Estado.BRIEF_RECIBIDO,
        Estado.COTIZACION,
        Estado.NEGOCIACION,
        Estado.GANADO,
        Estado.PERDIDO,
    ]

    nombre = models.CharField("nombre contacto", max_length=160)
    empresa = models.CharField(max_length=160, blank=True)
    cargo = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    whatsapp = models.CharField(max_length=40, blank=True)
    instagram = models.CharField(max_length=120, blank=True)
    linkedin = models.CharField(max_length=200, blank=True)
    behance = models.CharField(max_length=200, blank=True)
    sitio_web = models.URLField(blank=True)

    fuente = models.CharField(max_length=20, choices=Fuente.choices, default=Fuente.INSTAGRAM)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.NUEVO)
    valor_estimado = models.DecimalField(
        max_digits=12, decimal_places=0, default=0,
        help_text="Valor potencial del proyecto (CLP)",
    )
    notas = models.TextField(blank=True)

    # Trazabilidad de conversión a cliente.
    cliente = models.ForeignKey(
        "clients.Client", null=True, blank=True, on_delete=models.SET_NULL,
        related_name="leads_origen",
    )

    class Meta:
        ordering = ["-creado"]
        verbose_name = "lead"
        verbose_name_plural = "leads"

    def __str__(self):
        empresa = f" · {self.empresa}" if self.empresa else ""
        return f"{self.nombre}{empresa}"

    def get_absolute_url(self):
        return reverse("leads:detail", args=[self.pk])

    @property
    def es_activo(self):
        return self.estado not in (self.Estado.GANADO, self.Estado.PERDIDO)

    @property
    def color_estado(self):
        mapa = {
            self.Estado.NUEVO: "secondary",
            self.Estado.CONTACTADO: "info",
            self.Estado.REUNION: "primary",
            self.Estado.BRIEF_SOLICITADO: "warning",
            self.Estado.BRIEF_RECIBIDO: "warning",
            self.Estado.COTIZACION: "info",
            self.Estado.NEGOCIACION: "primary",
            self.Estado.GANADO: "success",
            self.Estado.PERDIDO: "danger",
        }
        return mapa.get(self.estado, "secondary")
