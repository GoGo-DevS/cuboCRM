from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("proyecto", "tipo", "monto", "metodo", "fecha", "pagado")
    list_filter = ("pagado", "tipo", "metodo")
    search_fields = ("proyecto__nombre",)
    autocomplete_fields = ("proyecto",)
    list_editable = ("pagado",)
