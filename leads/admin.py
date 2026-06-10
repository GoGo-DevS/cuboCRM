from django.contrib import admin

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "empresa", "fuente", "estado", "valor_estimado", "creado")
    list_filter = ("estado", "fuente", "creado")
    search_fields = ("nombre", "empresa", "email", "instagram")
    list_editable = ("estado",)
    date_hierarchy = "creado"
    readonly_fields = ("creado", "actualizado")
