# Prompt para arrancar Creative Growth CRM con Claude Code

> Copia TODO el bloque de abajo y pégalo en **Claude Code** (o Claude en tu IDE),
> con la terminal abierta en la carpeta donde quieras tener el proyecto.
> Claude se encarga de clonar, instalar, levantar y explicarte cómo mejorarlo.

---

```
Hola Claude. Vas a ayudarme a levantar y luego mejorar un CRM hecho en Django
que me pasó un amigo. Está en GitHub. Trabaja paso a paso y NO borres datos sin avisarme.

CONTEXTO DEL PROYECTO
- Nombre: Creative Growth CRM (marca "cub.")
- Qué es: un "Creative Operations System" para estudios/freelancers creativos.
  Gestiona el ciclo completo: Lead → Cliente → Brief → Proyecto → Entregables/Revisiones
  → Pagos → Caso de éxito (portafolio).
- Stack: Python 3.13, Django 6, SQLite en desarrollo (Postgres en producción),
  HTML + CSS propio (sin framework) + JavaScript vanilla. Patrón MVT, sin React.
- Repo: https://github.com/GoGo-DevS/cuboCRM
- Apps Django: core (dashboard, datos demo), leads (Kanban), clients, briefs,
  projects (con entregables y revisiones), finance (pagos), portfolio (casos de éxito).

TAREA 1 — Clonar y levantar (Windows / PowerShell; si estás en Mac/Linux, adapta los comandos)
1. Clona el repo:
   git clone https://github.com/GoGo-DevS/cuboCRM.git
   cd cuboCRM
2. Crea un entorno virtual e instala dependencias:
   python -m venv venv
   .\venv\Scripts\python.exe -m pip install --upgrade pip
   .\venv\Scripts\python.exe -m pip install -r requirements.txt
3. Prepara la base de datos y carga datos de ejemplo:
   .\venv\Scripts\python.exe manage.py migrate
   .\venv\Scripts\python.exe manage.py seed_demo
4. Levanta el servidor:
   .\venv\Scripts\python.exe manage.py runserver
5. Dime que abra http://127.0.0.1:8000/ y que entre con usuario "admin" y clave "admin".
   Confírmame que ves el dashboard con datos de ejemplo (leads, proyectos, etc.).

TAREA 2 — Orientarme en el código
Lee primero DESIGN.md y README.md del repo (tienen la arquitectura completa y el roadmap).
Luego hazme un resumen corto de:
- cómo están organizadas las apps y qué hace cada una,
- el flujo de datos de un lead hasta convertirse en caso de éxito,
- dónde tocar para cambiar estilos (static/css/app.css) y plantillas (templates/ y <app>/templates/).

TAREA 3 — Mejorar (espera mis instrucciones)
Cuando todo corra, pregúntame qué quiero mejorar. Posibles próximos pasos del roadmap V2
(están en DESIGN.md): roles y permisos, portal del cliente para aprobar revisiones,
cotizaciones/propuestas en PDF, gestor de archivos con versiones, notificaciones por
email/WhatsApp, reportes y export CSV.

REGLAS DE TRABAJO
- Antes de cambios grandes, explícame qué vas a hacer y por qué.
- Cada cambio debe quedar conectado de punta a punta (modelo → vista → formulario → plantilla).
- No subas nada a GitHub ni hagas commits sin que yo te lo pida explícitamente.
- Si algo falla al instalar o migrar, diagnostica el error y propón la solución antes de seguir.

Empieza por la TAREA 1.
```

---

## Notas para humanos (no son parte del prompt)
- El login demo es **admin / admin** (lo crea el comando `seed_demo`). Cámbialo antes de usarlo en serio.
- La base `db.sqlite3` NO está en el repo (se genera con `migrate` + `seed_demo`).
- Para desplegar en producción (Render + Cloudflare), mira la sección 21 de **DESIGN.md**.
