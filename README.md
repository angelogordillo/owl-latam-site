# OWL LATAM Standalone

Proyecto independiente para publicar la landing de OWL LATAM en Railway.

## Archivos
- `main.py`: app FastAPI (landing + endpoint de formulario)
- `owl-latam.html`: landing page
- `owl-logo.png`: logo
- `requirements.txt`: dependencias Python
- `railway.json`: comando de inicio para Railway
- `.env.example`: variables SMTP necesarias

## Correr local
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Abrir: `http://127.0.0.1:8000`

## Deploy en Railway
1. Crear repo nuevo y subir esta carpeta.
2. En Railway: New Project -> Deploy from GitHub repo.
3. Variables de entorno:
   - `OWL_LEAD_TO`
   - `SMTP_HOST`
   - `SMTP_PORT`
   - `SMTP_USER`
   - `SMTP_PASSWORD`
   - `SMTP_FROM`
   - `SMTP_STARTTLS`
4. Dominio:
   - Añadir `www.theowlsolutions.lat` en Domains.
   - Crear CNAME `www` al target que entregue Railway.
