from django.contrib import admin

from .models import Brief


@admin.register(Brief)
class BriefAdmin(admin.ModelAdmin):
    list_display = ("nombre_marca", "cliente", "estado", "creado")
    list_filter = ("estado", "creado")
    search_fields = ("nombre_marca", "cliente__nombre")
    autocomplete_fields = ("cliente",)
