# DESIGN.md — Creative Growth CRM (`cub.`)
> Documento vivo de arquitectura y producto. El MVP del repo ya implementa lo marcado ✅.

---

## 1. Visión del producto
**Creative Growth CRM** no es un CRM genérico: es un **Creative Operations System** que une
**Ventas + Producción + Diseño + Entrega + Portafolio** en un solo flujo. Está pensado para
diseñadores gráficos, brand/motion designers, freelancers y estudios boutique que hoy gestionan
su negocio entre WhatsApp, Notion, Drive, Excel y la cabeza.

La promesa: *del lead al caso de éxito sin cambiar de herramienta.*

## 2. Problemas que resuelve
- **Pipeline comercial invisible**: leads en DMs que se enfrían sin seguimiento → Kanban ✅
- **Briefs incompletos**: el encargo creativo se pierde en chats → Brief estructurado ✅
- **Producción sin control de versiones**: "¿esta es la V2 o la V3?" → Entregables + Revisiones ✅
- **Cobros que se escapan**: anticipos/saldos sin trazar → Finanzas por proyecto ✅
- **Portafolio que nunca se actualiza**: proyectos entregados que no se capitalizan → Casos de éxito 1-clic ✅
- **Cliente recurrente desaprovechado**: sin visión de quién ya compró → ficha 360° del cliente ✅

## 3. Arquitectura general
Patrón **MVT** clásico de Django, modular por dominio. Sin SPA, sin APIs innecesarias:
templates server-side + JS vanilla para interacciones puntuales (drag&drop Kanban, toggles).

```
Navegador ──HTTP──> Django (config/) ──> Apps de dominio ──> ORM ──> SQLite (dev) / PostgreSQL (prod)
                         │
                         ├── templates/ (base + por app)   ← UI premium, CSS propio
                         └── static/css/app.css            ← tema "cub." (lima + negro)
```

## 4. Apps Django y su responsabilidad
| App | Responsabilidad | Estado |
|-----|-----------------|--------|
| `core` | Base abstracta (TimeStamped), dashboard, branding, helpers de UI, comando `seed_demo` | ✅ |
| `leads` | Captación: modelo Lead, Kanban 9 estados, conversión a cliente | ✅ |
| `clients` | Empresas + contactos (Company/Client), ficha 360° | ✅ |
| `briefs` | Brief creativo estructurado por cliente | ✅ |
| `projects` | Proyecto + Entregable + Revisión (versionado V1→Final) | ✅ |
| `finance` | Pagos por proyecto (anticipo/saldo), dashboard financiero | ✅ |
| `portfolio` | Testimonios + Casos de éxito publicables | ✅ |
| `accounts` (futuro) | Roles, permisos, multi-tenant | 🔜 V2/SaaS |
| `notifications` (futuro) | Avisos de cambio de estado, recordatorios | 🔜 V2 |

## 5. Modelo de datos (entidades y relaciones)
```
Company 1──* Client
Client  1──* Lead (origen)         Client 1──* Brief        Client 1──* Project
Brief   1──* Project (opcional)
Project 1──* Deliverable 1──* Revision
Project 1──* Payment
Project 1──1 CaseStudy             Client 1──* Testimonial ──? CaseStudy
User    1──* Project (responsable) / Deliverable / Revision
```
- **TimeStampedModel** (abstracta) da `creado`/`actualizado` a todo.
- **Cardinalidades clave**: un cliente tiene N proyectos (recurrencia = `proyectos.count() > 1`);
  un proyecto tiene N entregables, cada entregable N revisiones; un proyecto tiene 1 caso de éxito.
- **FKs con `SET_NULL`** donde la pérdida del padre no debe borrar el hijo (brief→project, lead→client).

## 6. Casos de uso (implementados)
1. Registrar un lead desde Instagram → arrastrarlo por el Kanban → ganarlo → se crea el cliente.
2. Cargar el brief del cliente → crear proyecto vinculado al brief.
3. Agregar entregables (logo, manual, reel) → registrar rondas de revisión V1/V2/Final.
4. Registrar anticipo y saldo → ver % cobrado y total por cobrar en Finanzas.
5. Al entregar → generar caso de éxito con testimonio → publicarlo en el portafolio.

## 7. Flujo completo (pipeline)
`Lead → Contactado → Reunión → Brief solicitado/recibido → Cotización → Negociación → Ganado`
`→ Cliente → Brief → Proyecto (Planificado→Producción→Feedback→Correcciones→Aprobado→Entregado)`
`→ Pago saldo → Caso de éxito → Cliente recurrente`

## 8–9. Wireframes / UX-UI
Layout **sidebar oscura fija + contenido claro** (estilo Linear/Notion/HubSpot), acento lima `#c6f432`.
- **Sidebar**: marca `cub.`, secciones Comercial / Producción, link a Django Admin, usuario.
- **Topbar**: título de página + breadcrumb + acciones contextuales.
- **Patrones**: KPI cards, tablas, Kanban con drag&drop, fichas a 2 columnas, toasts.
Todo con CSS propio (sin dependencia de build) y responsive (sidebar colapsable en móvil).

## 10. Dashboard
Widgets: leads nuevos, cotizaciones pendientes, proyectos activos, **conversión %** (card destacada),
ingresos mes/año, por cobrar, clientes/recurrentes, briefs abiertos, barras de pipeline,
próximas entregas, últimos leads, proyectos por servicio.

## 11. Roadmap — MVP (este repo) ✅
- [x] Kanban de leads + CRUD + conversión a cliente
- [x] Clientes/empresas con ficha 360°
- [x] Briefs creativos
- [x] Proyectos + entregables + revisiones
- [x] Finanzas por proyecto + dashboard financiero
- [x] Casos de éxito / portafolio
- [x] Dashboard ejecutivo
- [x] Django Admin mejorado + datos demo

## 12. Roadmap — V2
- [ ] **Roles y permisos** (Admin / Director Creativo / Diseñador / Vendedor / Cliente)
- [ ] **Portal del cliente**: aprobar revisiones y ver entregables con un link
- [ ] **Cotizaciones/propuestas** como documento generado (PDF) + estados
- [ ] **Gestor de archivos** con versionado y preview (AI/PSD/MP4/ZIP)
- [ ] **Notificaciones** (email/WhatsApp) en cambios de estado y vencimientos
- [ ] **Reportes** y export CSV; gráficos con Chart.js
- [ ] Recordatorios de seguimiento de leads fríos

## 13. Roadmap — SaaS
- [ ] **Multi-tenant** (modelo `Studio`/`Tenant`, scoping por estudio)
- [ ] **Suscripciones y planes** (límites de leads/proyectos/usuarios)
- [ ] Onboarding self-service + facturación (Stripe/Flow/Webpay)
- [ ] Personalización de marca por estudio (white-label del portafolio)

## 14. Estructura de carpetas
```
CreativeGrowthCRM/
├── manage.py · requirements.txt · README.md · DESIGN.md · .gitignore
├── config/            settings, urls, wsgi, asgi
├── core/              base model, dashboard, context_processor, _icon, _form_fields, seed_demo
├── leads/  clients/  briefs/  projects/  finance/  portfolio/
│   └── models · forms · views · urls · admin · migrations · templates/<app>/
├── templates/         base.html, registration/login.html
├── static/css/app.css
└── media/             uploads (logos, adjuntos, portadas)
```

## 15–18. Modelos / URLs / Views / Templates
Implementados (ver código). Mapa de URLs:
```
/                         dashboard
/leads/                   board (Kanban)     /leads/nuevo /<pk>/ /<pk>/editar /<pk>/estado /<pk>/convertir
/clients/                 list /nuevo /<pk>/ /<pk>/editar
/briefs/                  list /nuevo /<pk>/ /<pk>/editar
/projects/                board /nuevo /<pk>/ /<pk>/editar /<pk>/estado
                          /<pk>/entregable/nuevo  /entregable/<pk>/estado  /entregable/<pk>/revision
/finance/                 overview /pago/nuevo /pago/<pk>/toggle
/portfolio/               list /<slug>/ /proyecto/<pk>/generar /<slug>/publicar
/admin/                   Django admin
/login/ /logout/
```
Views: mezcla de funciones con `@login_required`; POST mutadores con `@require_POST` y soporte AJAX
en los cambios de estado del Kanban.

## 19–20. Permisos y seguridad
- **Hoy**: autenticación obligatoria (`LOGIN_URL`), CSRF en todos los POST, `@require_POST` en mutaciones.
- **Producción**: `DEBUG=False`, `SECRET_KEY`/hosts por entorno, `CSRF_TRUSTED_ORIGINS`, HTTPS (Cloudflare).
- **V2**: roles vía Groups/Permissions de Django + decoradores por rol; auditoría con timestamps ya presentes.

## 21. Estrategia de despliegue (Render + Cloudflare)
1. `requirements.txt`: activar gunicorn, whitenoise, dj-database-url, psycopg.
2. Render Web Service: build `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`; start `gunicorn config.wsgi`.
3. Variables: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS`, `DATABASE_URL`, `DJANGO_CSRF_TRUSTED_ORIGINS`.
4. Postgres administrado de Render; archivos media en almacenamiento externo (S3/R2) para escalar.
5. Cloudflare delante: CDN, SSL, caché de estáticos, WAF.

---
### Decisiones de arquitectura
- **SQLite en dev, Postgres en prod** vía `DATABASE_URL` (sin tocar código).
- **CSS propio** en vez de framework pesado: control total del look "cub." y cero build.
- **Apps por dominio** desde el día 1 para que el salto a multi-tenant (SaaS) sea aditivo, no un refactor.
- **Modelo abstracto TimeStamped** para auditoría barata y consistente.
