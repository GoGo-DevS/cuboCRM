# Creative Growth CRM · `cub.`

**Creative Operations System** para diseñadores, estudios de branding, motion y agencias creativas.
Centraliza Ventas + Producción + Diseño + Entrega + Portafolio en un solo lugar.

Stack: **Django 5/6 · SQLite (dev) → PostgreSQL (prod) · Bootstrap-grade CSS propio · JS vanilla**.

---

## 🚀 Levantar en local (Windows / PowerShell)

```powershell
cd "C:\Users\diego\Proyectos GoGoDevS\CreativeGrowthCRM"

# 1. Migrar la base
.\venv\Scripts\python.exe manage.py migrate

# 2. Cargar datos demo + crear superusuario admin/admin
.\venv\Scripts\python.exe manage.py seed_demo

# 3. Levantar el servidor
.\venv\Scripts\python.exe manage.py runserver
```

Abre **http://127.0.0.1:8000/** → entra con **admin / admin**.

> El venv ya está creado dentro de la carpeta con Django + Pillow instalados.

---

## 🧭 Módulos (MVP funcional hoy)

| Módulo | URL | Qué hace |
|--------|-----|----------|
| Dashboard | `/` | KPIs comerciales, producción y finanzas + mini-gráficos |
| Leads | `/leads/` | Kanban arrastrable (9 estados) + CRUD + convertir a cliente |
| Clientes | `/clients/` | Ficha 360°: proyectos, briefs, testimonios, WhatsApp |
| Briefs | `/briefs/` | Brief creativo completo por cliente |
| Proyectos | `/projects/` | Kanban de producción + entregables + revisiones + pagos |
| Finanzas | `/finance/` | Ingresos mes/año, por cobrar, toggle pagado |
| Portafolio | `/portfolio/` | Generar caso de éxito desde un proyecto, publicar |
| Admin | `/admin/` | Django admin mejorado (filtros, inlines, autocomplete) |

---

## 🔁 Flujo end-to-end

`Lead (Kanban) → Ganar → Cliente → Brief → Proyecto → Entregables/Revisiones → Pagos → Caso de éxito`

Cada paso está conectado: ganar un lead crea el cliente; desde el cliente creas brief y proyecto;
al entregar generas el caso de estudio para el portafolio.

---

## 📦 Despliegue (Render + Cloudflare)

1. Descomenta gunicorn/whitenoise/dj-database-url/psycopg en `requirements.txt`.
2. Setea variables de entorno: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`,
   `DJANGO_ALLOWED_HOSTS`, `DATABASE_URL` (Postgres de Render).
3. `python manage.py collectstatic` lo sirve WhiteNoise.
4. Cloudflare delante para CDN/SSL.

Ver **DESIGN.md** para la arquitectura completa, modelo de datos y roadmap (MVP / V2 / SaaS).
