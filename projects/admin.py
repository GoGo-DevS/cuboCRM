from django.contrib import admin

from .models import Deliverable, Project, Revision


class DeliverableInline(admin.TabularInline):
    model = Deliverable
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("nombre", "cliente", "tipo", "estado", "monto", "fecha_entrega")
    list_filter = ("estado", "tipo", "creado")
    search_fields = ("nombre", "cliente__nombre")
    autocomplete_fields = ("cliente", "brief", "responsable")
    inlines = [DeliverableInline]
    date_hierarchy = "creado"


class RevisionInline(admin.TabularInline):
    model = Revision
    extra = 0


@admin.register(Deliverable)
class DeliverableAdmin(admin.ModelAdmin):
    list_display = ("nombre", "proyecto", "tipo", "estado", "fecha")
    list_filter = ("estado", "tipo")
    search_fields = ("nombre", "proyecto__nombre")
    autocomplete_fields = ("proyecto", "responsable")
    inlines = [RevisionInline]


@admin.register(Revision)
class RevisionAdmin(admin.ModelAdmin):
    list_display = ("entregable", "version", "estado", "creado")
    list_filter = ("estado", "version")
