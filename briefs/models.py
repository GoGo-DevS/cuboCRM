from django.db import models
from django.urls import reverse

from core.models import TimeStampedModel


class Brief(TimeStampedModel):
    class Estado(models.TextChoices):
        BORRADOR = "borrador", "Borrador"
        RECIBIDO = "recibido", "Recibido"
        APROBADO = "aprobado", "Aprobado"

    cliente = models.ForeignKey(
        "clients.Client", on_delete=models.CASCADE, related_name="briefs"
    )
    nombre_marca = models.CharField(max_length=160)
    rubro = models.CharField(max_length=120, blank=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.BORRADOR)

    historia = models.TextField("historia de marca", blank=True)
    objetivos = models.TextField(blank=True)
    publico_objetivo = models.TextField("público objetivo", blank=True)
    competencia = models.TextField(blank=True)
    personalidad = models.CharField(
        max_length=255, blank=True,
        help_text="Ej: moderna, cercana, premium, disruptiva",
    )
    referencias = models.TextField("referencias / inspiraciones", blank=True)
    colores_deseados = models.CharField(max_length=255, blank=True)
    colores_prohibidos = models.CharField(max_length=255, blank=True)
    tipografias = models.CharField(max_length=255, blank=True)
    adjunto = models.FileField(upload_to="briefs/", blank=True, null=True)

    class Meta:
        ordering = ["-creado"]
        verbose_name = "brief"
        verbose_name_plural = "briefs"

    def __str__(self):
        return f"Brief · {self.nombre_marca}"

    def get_absolute_url(self):
        return reverse("briefs:detail", args=[self.pk])

    @property
    def color_estado(self):
        return {
            self.Estado.BORRADOR: "secondary",
            self.Estado.RECIBIDO: "info",
            self.Estado.APROBADO: "success",
        }.get(self.estado, "secondary")
