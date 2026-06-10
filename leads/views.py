from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from clients.models import Client, Company

from .forms import LeadForm
from .models import Lead


@login_required
def board(request):
    """Kanban de leads agrupado por estado."""
    fuente = request.GET.get("fuente", "")
    qs = Lead.objects.all()
    if fuente:
        qs = qs.filter(fuente=fuente)

    columnas = []
    for estado in Lead.PIPELINE:
        leads = [l for l in qs if l.estado == estado]
        columnas.append(
            {
                "key": estado,
                "label": Lead.Estado(estado).label,
                "leads": leads,
                "total": len(leads),
                "valor": sum(l.valor_estimado for l in leads),
            }
        )
    contexto = {
        "columnas": columnas,
        "fuentes": Lead.Fuente.choices,
        "fuente_sel": fuente,
        "total": qs.count(),
    }
    return render(request, "leads/board.html", contexto)


@login_required
def detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    return render(request, "leads/detail.html", {"lead": lead})


@login_required
def create(request):
    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save()
            messages.success(request, f"Lead «{lead.nombre}» creado.")
            return redirect(lead.get_absolute_url())
    else:
        form = LeadForm()
    return render(request, "leads/form.html", {"form": form, "titulo": "Nuevo lead"})


@login_required
def update(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == "POST":
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, "Lead actualizado.")
            return redirect(lead.get_absolute_url())
    else:
        form = LeadForm(instance=lead)
    return render(
        request, "leads/form.html",
        {"form": form, "titulo": f"Editar · {lead.nombre}", "lead": lead},
    )


@login_required
@require_POST
def delete(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    lead.delete()
    messages.info(request, "Lead eliminado.")
    return redirect("leads:board")


@login_required
@require_POST
def set_estado(request, pk):
    """Mover lead de columna (drag&drop por AJAX o submit normal)."""
    lead = get_object_or_404(Lead, pk=pk)
    nuevo = request.POST.get("estado")
    if nuevo in Lead.Estado.values:
        lead.estado = nuevo
        lead.save(update_fields=["estado", "actualizado"])
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"ok": True, "estado": lead.estado})
        messages.success(request, "Estado actualizado.")
    return redirect(request.META.get("HTTP_REFERER", "leads:board"))


@login_required
@require_POST
def convert(request, pk):
    """Convierte un lead ganado en cliente (get_or_create por email/nombre)."""
    lead = get_object_or_404(Lead, pk=pk)
    if lead.cliente:
        messages.info(request, "Este lead ya está vinculado a un cliente.")
        return redirect(lead.cliente.get_absolute_url())

    empresa = None
    if lead.empresa:
        empresa, _ = Company.objects.get_or_create(nombre=lead.empresa)

    cliente, creado = Client.objects.get_or_create(
        nombre=lead.nombre,
        email=lead.email or "",
        defaults={
            "empresa": empresa,
            "cargo": lead.cargo,
            "whatsapp": lead.whatsapp,
            "instagram": lead.instagram,
            "linkedin": lead.linkedin,
            "notas": lead.notas,
        },
    )
    lead.cliente = cliente
    lead.estado = Lead.Estado.GANADO
    lead.save(update_fields=["cliente", "estado", "actualizado"])
    messages.success(
        request,
        f"Cliente {'creado' if creado else 'vinculado'}: {cliente.nombre}.",
    )
    return redirect(cliente.get_absolute_url())
