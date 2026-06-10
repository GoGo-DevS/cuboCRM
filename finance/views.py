from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from projects.models import Project

from .forms import PaymentForm
from .models import Payment


@login_required
def overview(request):
    hoy = date.today()
    pagos = Payment.objects.select_related("proyecto", "proyecto__cliente")

    ingresos_mes = pagos.filter(
        pagado=True, fecha__year=hoy.year, fecha__month=hoy.month
    ).aggregate(t=Sum("monto"))["t"] or 0
    ingresos_ano = pagos.filter(pagado=True, fecha__year=hoy.year).aggregate(
        t=Sum("monto")
    )["t"] or 0
    total_pagado = pagos.filter(pagado=True).aggregate(t=Sum("monto"))["t"] or 0
    total_proyectos = Project.objects.aggregate(t=Sum("monto"))["t"] or 0
    pendiente = total_proyectos - total_pagado

    contexto = {
        "pagos": pagos[:50],
        "ingresos_mes": ingresos_mes,
        "ingresos_ano": ingresos_ano,
        "pendiente": pendiente,
        "total_pagado": total_pagado,
        "form": PaymentForm(),
    }
    return render(request, "finance/overview.html", contexto)


@login_required
@require_POST
def payment_create(request):
    form = PaymentForm(request.POST)
    if form.is_valid():
        pago = form.save()
        messages.success(request, f"Pago registrado: ${pago.monto:,.0f}.")
    else:
        messages.error(request, "Revisa los datos del pago.")
    next_url = request.POST.get("next")
    if next_url:
        return redirect(next_url)
    return redirect("finance:overview")


@login_required
@require_POST
def payment_toggle(request, pk):
    pago = get_object_or_404(Payment, pk=pk)
    pago.pagado = not pago.pagado
    if pago.pagado and not pago.fecha:
        pago.fecha = date.today()
    pago.save(update_fields=["pagado", "fecha", "actualizado"])
    messages.success(request, "Estado de pago actualizado.")
    return redirect(request.META.get("HTTP_REFERER", "finance:overview"))
