from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BriefForm
from .models import Brief


@login_required
def brief_list(request):
    briefs = Brief.objects.select_related("cliente")
    return render(request, "briefs/list.html", {"briefs": briefs})


@login_required
def brief_detail(request, pk):
    brief = get_object_or_404(Brief.objects.select_related("cliente"), pk=pk)
    return render(request, "briefs/detail.html", {"brief": brief})


@login_required
def brief_create(request):
    if request.method == "POST":
        form = BriefForm(request.POST, request.FILES)
        if form.is_valid():
            brief = form.save()
            messages.success(request, f"Brief «{brief.nombre_marca}» creado.")
            return redirect(brief.get_absolute_url())
    else:
        initial = {}
        if request.GET.get("cliente"):
            initial["cliente"] = request.GET["cliente"]
        form = BriefForm(initial=initial)
    return render(request, "briefs/form.html", {"form": form, "titulo": "Nuevo brief"})


@login_required
def brief_update(request, pk):
    brief = get_object_or_404(Brief, pk=pk)
    if request.method == "POST":
        form = BriefForm(request.POST, request.FILES, instance=brief)
        if form.is_valid():
            form.save()
            messages.success(request, "Brief actualizado.")
            return redirect(brief.get_absolute_url())
    else:
        form = BriefForm(instance=brief)
    return render(
        request, "briefs/form.html",
        {"form": form, "titulo": f"Editar · {brief.nombre_marca}", "brief": brief},
    )
