from datetime import date

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import render

from briefs.models import Brief
from clients.models import Client
from finance.models import Payment
from leads.models import Lead
from projects.models import Project


@login_required
def dashboard(request):
    hoy = date.today()

    leads_qs = Lead.objects.all()
    proyectos_qs = Project.objects.all()

    # --- KPIs comerciales ---
    leads_nuevos = leads_qs.filter(estado=Lead.Estado.NUEVO).count()
    leads_activos = leads_qs.exclude(
        estado__in=[Lead.Estado.GANADO, Lead.Estado.PERDIDO]
    ).count()
    cotizaciones_pendientes = leads_qs.filter(
        estado__in=[Lead.Estado.COTIZACION, Lead.Estado.NEGOCIACION]
    ).count()
    ganados = leads_qs.filter(estado=Lead.Estado.GANADO).count()
    perdidos = leads_qs.filter(estado=Lead.Estado.PERDIDO).count()
    cerrados = ganados + perdidos
    conversion = round((ganados / cerrados) * 100) if cerrados else 0

    # --- KPIs producción ---
    proyectos_activos = proyectos_qs.exclude(
        estado__in=[Project.Estado.ENTREGADO, Project.Estado.CERRADO]
    ).count()
    proyectos_entregados = proyectos_qs.filter(
        estado__in=[Project.Estado.ENTREGADO, Project.Estado.CERRADO]
    ).count()

    # --- KPIs finanzas ---
    pagos_mes = Payment.objects.filter(
        pagado=True, fecha__year=hoy.year, fecha__month=hoy.month
    ).aggregate(t=Sum("monto"))["t"] or 0
    pagos_ano = Payment.objects.filter(
        pagado=True, fecha__year=hoy.year
    ).aggregate(t=Sum("monto"))["t"] or 0
    por_cobrar = (
        proyectos_qs.aggregate(t=Sum("monto"))["t"] or 0
    ) - (Payment.objects.filter(pagado=True).aggregate(t=Sum("monto"))["t"] or 0)

    # --- Clientes ---
    total_clientes = Client.objects.count()
    recurrentes = (
        Client.objects.annotate(n=Count("proyectos")).filter(n__gt=1).count()
    )

    # --- Distribuciones para gráficos ---
    leads_por_estado = []
    for estado in Lead.PIPELINE:
        leads_por_estado.append(
            {
                "label": Lead.Estado(estado).label,
                "value": leads_qs.filter(estado=estado).count(),
                "key": estado,
            }
        )

    proyectos_por_tipo = []
    for tipo in Project.Tipo:
        c = proyectos_qs.filter(tipo=tipo).count()
        if c:
            proyectos_por_tipo.append({"label": tipo.label, "value": c})

    contexto = {
        "leads_nuevos": leads_nuevos,
        "leads_activos": leads_activos,
        "cotizaciones_pendientes": cotizaciones_pendientes,
        "conversion": conversion,
        "ganados": ganados,
        "proyectos_activos": proyectos_activos,
        "proyectos_entregados": proyectos_entregados,
        "pagos_mes": pagos_mes,
        "pagos_ano": pagos_ano,
        "por_cobrar": por_cobrar,
        "total_clientes": total_clientes,
        "recurrentes": recurrentes,
        "leads_por_estado": leads_por_estado,
        "max_leads": max([x["value"] for x in leads_por_estado] + [1]),
        "proyectos_por_tipo": proyectos_por_tipo,
        "briefs_pendientes": Brief.objects.exclude(
            estado=Brief.Estado.APROBADO
        ).count(),
        "ultimos_leads": leads_qs[:6],
        "proximas_entregas": proyectos_qs.filter(
            fecha_entrega__isnull=False
        ).exclude(
            estado__in=[Project.Estado.ENTREGADO, Project.Estado.CERRADO]
        ).order_by("fecha_entrega")[:6],
    }
    return render(request, "core/dashboard.html", contexto)
