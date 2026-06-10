from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from projects.models import Project

from .models import CaseStudy


@login_required
def case_list(request):
    casos = CaseStudy.objects.select_related("proyecto", "proyecto__cliente")
    return render(request, "portfolio/list.html", {"casos": casos})


@login_required
def case_detail(request, slug):
    caso = get_object_or_404(
        CaseStudy.objects.select_related("proyecto", "proyecto__cliente", "testimonio"),
        slug=slug,
    )
    return render(request, "portfolio/detail.html", {"caso": caso})


@login_required
def case_from_project(request, pk):
    """Convierte un proyecto en caso de estudio (autogenera borrador)."""
    proyecto = get_object_or_404(Project, pk=pk)
    caso = getattr(proyecto, "caso_estudio", None)
    if caso:
        messages.info(request, "Este proyecto ya tiene un caso de estudio.")
        return redirect(caso.get_absolute_url())

    caso = CaseStudy.objects.create(
        proyecto=proyecto,
        titulo=f"{proyecto.nombre} · {proyecto.cliente.nombre}",
        descripcion=proyecto.descripcion,
        resultados="",
        testimonio=proyecto.testimonios.first(),
    )
    messages.success(
        request,
        "Caso de estudio generado. Completa resultados e imagen para publicarlo.",
    )
    return redirect(caso.get_absolute_url())


@login_required
def case_toggle_publish(request, slug):
    caso = get_object_or_404(CaseStudy, slug=slug)
    caso.publicado = not caso.publicado
    caso.save(update_fields=["publicado", "actualizado"])
    messages.success(
        request, "Caso publicado." if caso.publicado else "Caso despublicado."
    )
    return redirect(caso.get_absolute_url())
