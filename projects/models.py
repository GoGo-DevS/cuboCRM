from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.urls import reverse

from core.models import TimeStampedModel


class Project(TimeStampedModel):
    class Tipo(models.TextChoices):
        BRANDING = "branding", "Branding"
        MOTION = "motion", "Motion Graphics"
        VIDEO = "video", "Video"
        REDES = "redes", "Redes Sociales"
        PACKAGING = "packaging", "Packaging"
        EDITORIAL = "editorial", "Diseño Editorial"
        WEB = "web", "Diseño Web"

    class Estado(models.TextChoices):
        PLANIFICADO = "planificado", "Planificado"
        PRODUCCION = "produccion", "En Producción"
        FEEDBACK = "feedback", "Esperando Feedback"
        CORRECCIONES = "correcciones", "Correcciones"
        APROBADO = "aprobado", "Aprobado"
        ENTREGADO = "entregado", "Entregado"
        CERRADO = "cerrado", "Cerrado"

    PIPELINE = [
        Estado.PLANIFICADO,
        Estado.PRODUCCION,
        Estado.FEEDBACK,
        Estado.CORRECCIONES,
        Estado.APROBADO,
        Estado.ENTREGADO,
        Estado.CERRADO,
    ]

    nombre = models.CharField(max_length=180)
    cliente = models.ForeignKey(
        "clients.Client", on_delete=models.CASCADE, related_name="proyectos"
    )
    brief = models.ForeignKey(
        "briefs.Brief", null=True, blank=True, on_delete=models.SET_NULL,
        related_name="proyectos",
    )
    tipo = models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.BRANDING)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PLANIFICADO)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_entrega = models.DateField(null=True, blank=True)
    monto = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
        related_name="proyectos",
    )

    class Meta:
        ordering = ["-creado"]
        verbose_name = "proyecto"
        verbose_name_plural = "proyectos"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("projects:detail", args=[self.pk])

    @property
    def es_activo(self):
        return self.estado not in (self.Estado.ENTREGADO, self.Estado.CERRADO)

    @property
    def color_estado(self):
        return {
            self.Estado.PLANIFICADO: "secondary",
            self.Estado.PRODUCCION: "primary",
            self.Estado.FEEDBACK: "info",
            self.Estado.CORRECCIONES: "warning",
            self.Estado.APROBADO: "success",
            self.Estado.ENTREGADO: "success",
            self.Estado.CERRADO: "dark",
        }.get(self.estado, "secondary")

    @property
    def total_pagado(self):
        agg = self.pagos.filter(pagado=True).aggregate(t=Sum("monto"))
        return agg["t"] or 0

    @property
    def saldo_pendiente(self):
        return (self.monto or 0) - self.total_pagado

    @property
    def pct_pagado(self):
        if not self.monto:
            return 0
        return round(min(self.total_pagado / self.monto, 1) * 100)


class Deliverable(TimeStampedModel):
    class Tipo(models.TextChoices):
        LOGO = "logo", "Logo"
        MANUAL = "manual", "Manual de Marca"
        ANIMACION = "animacion", "Animación"
        REEL = "reel", "Reel"
        VIDEO = "video", "Video"
        BANNER = "banner", "Banner"
        FLYER = "flyer", "Flyer"
        PRESENTACION = "presentacion", "Presentación"
        MOCKUP = "mockup", "Mockups"

    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        EN_PROCESO = "en_proceso", "En Proceso"
        EN_REVISION = "en_revision", "En Revisión"
        APROBADO = "aprobado", "Aprobado"
        ENTREGADO = "entregado", "Entregado"

    proyecto = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="entregables")
    nombre = models.CharField(max_length=180)
    tipo = models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.LOGO)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    archivo = models.FileField(upload_to="entregables/", blank=True, null=True)
    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    fecha = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-creado"]
        verbose_name = "entregable"
        verbose_name_plural = "entregables"

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"

    @property
    def color_estado(self):
        return {
            self.Estado.PENDIENTE: "secondary",
            self.Estado.EN_PROCESO: "primary",
            self.Estado.EN_REVISION: "warning",
            self.Estado.APROBADO: "success",
            self.Estado.ENTREGADO: "success",
        }.get(self.estado, "secondary")


class Revision(TimeStampedModel):
    class Version(models.TextChoices):
        V1 = "v1", "V1"
        V2 = "v2", "V2"
        V3 = "v3", "V3"
        FINAL = "final", "Final"

    class Estado(models.TextChoices):
        ENVIADA = "enviada", "Enviada al cliente"
        CAMBIOS = "cambios", "Cambios solicitados"
        APROBADA = "aprobada", "Aprobada"

    entregable = models.ForeignKey(
        Deliverable, on_delete=models.CASCADE, related_name="revisiones"
    )
    version = models.CharField(max_length=10, choices=Version.choices, default=Version.V1)
    estado = models.CharField(max_length=12, choices=Estado.choices, default=Estado.ENVIADA)
    comentarios = models.TextField(blank=True)
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ["-creado"]
        verbose_name = "revisión"
        verbose_name_plural = "revisiones"

    def __str__(self):
        return f"{self.entregable.nombre} · {self.get_version_display()}"
