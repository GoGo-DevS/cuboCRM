from django.db import models


class TimeStampedModel(models.Model):
    """Base abstracta: created/updated en todos los modelos del producto."""

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
