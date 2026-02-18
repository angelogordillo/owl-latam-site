from datetime import datetime, timezone
from pathlib import Path
import os
import smtplib

from email.message import EmailMessage
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import EmailStr
from dotenv import load_dotenv

load_dotenv()

OWL_LEAD_TO = os.getenv("OWL_LEAD_TO", "angelo@theowl.solutions")
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER or "no-reply@theowl.solutions")
SMTP_STARTTLS = os.getenv("SMTP_STARTTLS", "true").lower() in {"1", "true", "yes", "on"}

app = FastAPI(title="OWL LATAM Website")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=static_dir), name="static")


def send_owl_lead_email(
    nombre: str,
    apellido: str,
    empresa: str,
    pagina_web: str | None,
    correo_corporativo: str,
    telefono: str,
    whatsapp: str,
):
    if not SMTP_HOST or not SMTP_USER or not SMTP_PASSWORD:
        raise RuntimeError("SMTP is not configured")

    msg = EmailMessage()
    msg["Subject"] = f"Nuevo lead OWL LATAM: {nombre} {apellido} - {empresa}"
    msg["From"] = SMTP_FROM
    msg["To"] = OWL_LEAD_TO
    msg["Reply-To"] = correo_corporativo

    body = (
        "Nuevo registro desde formulario OWL LATAM\\n\\n"
        f"Nombre: {nombre}\\n"
        f"Apellido: {apellido}\\n"
        f"Empresa: {empresa}\\n"
        f"Pagina web: {pagina_web or '-'}\\n"
        f"Correo corporativo: {correo_corporativo}\\n"
        f"Telefono: {telefono}\\n"
        f"WhatsApp: {whatsapp}\\n"
        f"Fecha UTC: {datetime.now(timezone.utc).isoformat()}\\n"
    )
    msg.set_content(body)

    if SMTP_PORT == 465 and not SMTP_STARTTLS:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=20) as smtp:
            smtp.login(SMTP_USER, SMTP_PASSWORD)
            smtp.send_message(msg)
        return

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as smtp:
        smtp.ehlo()
        if SMTP_STARTTLS:
            smtp.starttls()
            smtp.ehlo()
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.send_message(msg)


@app.get("/")
def owl_home():
    owl_path = Path(__file__).parent / "owl-latam.html"
    return FileResponse(
        owl_path,
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )

@app.get("/fva")
def fva_page():
    fva_path = Path(__file__).parent / "fva.html"
    return FileResponse(
        fva_path,
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )

@app.get("/calendario")
def calendario():
    calendario_path = Path(__file__).parent / "calendario.html"
    return FileResponse(
        calendario_path,
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )

@app.get("/casos")
def casos():
    casos_path = Path(__file__).parent / "casos.html"
    return FileResponse(
        casos_path,
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/api/owl-latam/lead")
def submit_owl_latam_lead(
    nombre: str = Form(...),
    apellido: str = Form(...),
    empresa: str = Form(...),
    web: str = Form(""),
    correo: EmailStr = Form(...),
    telefono: str = Form(...),
    whatsapp: str = Form(...),
):
    try:
        send_owl_lead_email(
            nombre=nombre.strip(),
            apellido=apellido.strip(),
            empresa=empresa.strip(),
            pagina_web=web.strip() or None,
            correo_corporativo=str(correo).strip(),
            telefono=telefono.strip(),
            whatsapp=whatsapp.strip(),
        )
        return {"ok": True, "message": "Registro enviado correctamente."}
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Email send failed: {exc}")
