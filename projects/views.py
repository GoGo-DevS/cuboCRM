from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import DeliverableForm, ProjectForm, RevisionForm
from .models import Deliverable, Project, Revision


@login_required
def board(request):
    tipo = request.GET.get("tipo", "")
    qs = Project.objects.select_related("cliente")
    if tipo:
        qs = qs.filter(tipo=tipo)
    columnas = []
    for estado in Project.PIPELINE:
        items = [p for p in qs if p.estado == estado]
        columnas.append(
            {
                "key": estado,
                "label": Project.Estado(estado).label,
                "proyectos": items,
                "total": len(items),
            }
        )
    return render(
        request, "projects/board.html",
        {"columnas": columnas, "tipos": Project.Tipo.choices, "tipo_sel": tipo, "total": qs.count()},
    )


@login_required
def detail(request, pk):
    proyecto = get_object_or_404(
        Project.objects.select_related("cliente", "brief"), pk=pk
    )
    contexto = {
        "proyecto": proyecto,
        "entregables": proyecto.entregables.all(),
        "pagos": proyecto.pagos.all(),
        "deliverable_form": DeliverableForm(),
        "tiene_caso": hasattr(proyecto, "caso_estudio"),
    }
    return render(request, "projects/detail.html", contexto)


@login_required
def create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            proyecto = form.save()
            messages.success(request, f"Proyecto «{proyecto.nombre}» creado.")
            return redirect(proyecto.get_absolute_url())
    else:
        initial = {}
        if request.GET.get("cliente"):
            initial["cliente"] = request.GET["cliente"]
        form = ProjectForm(initial=initial)
    return render(request, "projects/form.html", {"form": form, "titulo": "Nuevo proyecto"})


@login_required
def update(request, pk):
    proyecto = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            messages.success(request, "Proyecto actualizado.")
            return redirect(proyecto.get_absolute_url())
    else:
        form = ProjectForm(instance=proyecto)
    return render(
        request, "projects/form.html",
        {"form": form, "titulo": f"Editar · {proyecto.nombre}", "proyecto": proyecto},
    )


@login_required
@require_POST
def set_estado(request, pk):
    proyecto = get_object_or_404(Project, pk=pk)
    nuevo = request.POST.get("estado")
    if nuevo in Project.Estado.values:
        proyecto.estado = nuevo
        proyecto.save(update_fields=["estado", "actualizado"])
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"ok": True, "estado": proyecto.estado})
        messages.success(request, "Estado actualizado.")
    return redirect(request.META.get("HTTP_REFERER", "projects:board"))


@login_required
@require_POST
def deliverable_create(request, pk):
    proyecto = get_object_or_404(Project, pk=pk)
    form = DeliverableForm(request.POST, request.FILES)
    if form.is_valid():
        entregable = form.save(commit=False)
        entregable.proyecto = proyecto
        entregable.save()
        messages.success(request, f"Entregable «{entregable.nombre}» agregado.")
    else:
        messages.error(request, "Revisa los datos del entregable.")
    return redirect(proyecto.get_absolute_url())


@login_required
@require_POST
def deliverable_set_estado(request, pk):
    entregable = get_object_or_404(Deliverable, pk=pk)
    nuevo = request.POST.get("estado")
    if nuevo in Deliverable.Estado.values:
        entregable.estado = nuevo
        entregable.save(update_fields=["estado", "actualizado"])
        messages.success(request, "Entregable actualizado.")
    return redirect(entregable.proyecto.get_absolute_url())


@login_required
def revision_create(request, pk):
    entregable = get_object_or_404(Deliverable, pk=pk)
    if request.method == "POST":
        form = RevisionForm(request.POST)
        if form.is_valid():
            rev = form.save(commit=False)
            rev.entregable = entregable
            rev.autor = request.user
            rev.save()
            messages.success(request, f"Revisión {rev.get_version_display()} registrada.")
            return redirect(entregable.proyecto.get_absolute_url())
    else:
        form = RevisionForm(initial={"entregable": entregable})
        form.fields["entregable"].queryset = entregable.proyecto.entregables.all()
    return render(
        request, "projects/revision_form.html",
        {"form": form, "entregable": entregable, "titulo": f"Nueva revisión · {entregable.nombre}"},
    )
