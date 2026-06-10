from django.contrib import admin

from .models import Client, Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("nombre", "rubro", "ciudad", "pais")
    search_fields = ("nombre", "rubro")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("nombre", "empresa", "email", "whatsapp", "activo")
    list_filter = ("activo", "creado")
    search_fields = ("nombre", "email", "empresa__nombre")
    autocomplete_fields = ("empresa",)
