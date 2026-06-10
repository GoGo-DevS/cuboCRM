from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ClientForm
from .models import Client


@login_required
def client_list(request):
    q = request.GET.get("q", "").strip()
    qs = Client.objects.select_related("empresa").annotate(
        n_proyectos=Count("proyectos")
    )
    if q:
        qs = qs.filter(
            Q(nombre__icontains=q) | Q(empresa__nombre__icontains=q) | Q(email__icontains=q)
        )
    return render(request, "clients/list.html", {"clientes": qs, "q": q})


@login_required
def client_detail(request, pk):
    cliente = get_object_or_404(
        Client.objects.select_related("empresa"), pk=pk
    )
    contexto = {
        "cliente": cliente,
        "proyectos": cliente.proyectos.all(),
        "briefs": cliente.briefs.all(),
        "testimonios": cliente.testimonios.all(),
    }
    return render(request, "clients/detail.html", contexto)


@login_required
def client_create(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f"Cliente «{cliente.nombre}» creado.")
            return redirect(cliente.get_absolute_url())
    else:
        form = ClientForm()
    return render(request, "clients/form.html", {"form": form, "titulo": "Nuevo cliente"})


@login_required
def client_update(request, pk):
    cliente = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente actualizado.")
            return redirect(cliente.get_absolute_url())
    else:
        form = ClientForm(instance=cliente)
    return render(
        request, "clients/form.html",
        {"form": form, "titulo": f"Editar · {cliente.nombre}", "cliente": cliente},
    )
