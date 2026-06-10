from django.db import models
from django.urls import reverse

from core.models import TimeStampedModel


class Company(TimeStampedModel):
    nombre = models.CharField(max_length=160)
    rubro = models.CharField(max_length=120, blank=True)
    sitio_web = models.URLField(blank=True)
    instagram = models.CharField(max_length=120, blank=True)
    ciudad = models.CharField(max_length=120, blank=True)
    pais = models.CharField(max_length=80, blank=True, default="Chile")
    logo = models.ImageField(upload_to="empresas/", blank=True, null=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "empresa"
        verbose_name_plural = "empresas"

    def __str__(self):
        return self.nombre


class Client(TimeStampedModel):
    nombre = models.CharField(max_length=160)
    empresa = models.ForeignKey(
        Company, null=True, blank=True, on_delete=models.SET_NULL, related_name="contactos"
    )
    cargo = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    whatsapp = models.CharField(max_length=40, blank=True)
    instagram = models.CharField(max_length=120, blank=True)
    linkedin = models.CharField(max_length=200, blank=True)
    notas = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "cliente"
        verbose_name_plural = "clientes"

    def __str__(self):
        if self.empresa:
            return f"{self.nombre} · {self.empresa.nombre}"
        return self.nombre

    def get_absolute_url(self):
        return reverse("clients:detail", args=[self.pk])

    @property
    def es_recurrente(self):
        return self.proyectos.count() > 1
