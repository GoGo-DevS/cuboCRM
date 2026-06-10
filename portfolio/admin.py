from django.contrib import admin

from .models import CaseStudy, Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("autor_nombre", "cliente", "rating", "creado")
    list_filter = ("rating",)
    search_fields = ("autor_nombre", "cliente__nombre")
    autocomplete_fields = ("cliente", "proyecto")


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ("titulo", "proyecto", "publicado", "creado")
    list_filter = ("publicado",)
    search_fields = ("titulo",)
    prepopulated_fields = {"slug": ("titulo",)}
    autocomplete_fields = ("proyecto", "testimonio")
