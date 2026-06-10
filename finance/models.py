from django.db import models

from core.models import TimeStampedModel


class Payment(TimeStampedModel):
    class Tipo(models.TextChoices):
        ANTICIPO = "anticipo", "Anticipo"
        SALDO = "saldo", "Saldo"
        ABONO = "abono", "Abono"
        UNICO = "unico", "Pago único"

    class Metodo(models.TextChoices):
        TRANSFERENCIA = "transferencia", "Transferencia"
        EFECTIVO = "efectivo", "Efectivo"
        TARJETA = "tarjeta", "Tarjeta"
        PAYPAL = "paypal", "PayPal"
        OTRO = "otro", "Otro"

    proyecto = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, related_name="pagos"
    )
    tipo = models.CharField(max_length=15, choices=Tipo.choices, default=Tipo.ANTICIPO)
    metodo = models.CharField(max_length=15, choices=Metodo.choices, default=Metodo.TRANSFERENCIA)
    monto = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    fecha = models.DateField(null=True, blank=True)
    pagado = models.BooleanField(default=False)
    nota = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-fecha", "-creado"]
        verbose_name = "pago"
        verbose_name_plural = "pagos"

    def __str__(self):
        return f"{self.get_tipo_display()} · {self.proyecto.nombre} · ${self.monto:,.0f}"
