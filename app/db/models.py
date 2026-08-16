import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, Float, Integer, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db.connection import Base


def utcnow():
    return datetime.now(timezone.utc)


class Sesion(Base):
    __tablename__ = "sesiones"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    habilidades: Mapped[dict] = mapped_column(JSON, nullable=False)
    habilidad_personalizada: Mapped[str | None] = mapped_column(Text, nullable=True)
    intereses: Mapped[dict] = mapped_column(JSON, nullable=False)
    interes_personalizado: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Diagnostico(Base):
    __tablename__ = "diagnosticos"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sesion_id: Mapped[str] = mapped_column(String(36), ForeignKey("sesiones.id"), nullable=False)
    resultado_markdown: Mapped[str] = mapped_column(Text, nullable=False)
    carreras_sugeridas: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Exploracion(Base):
    __tablename__ = "exploraciones"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sesion_id: Mapped[str] = mapped_column(String(36), ForeignKey("sesiones.id"), nullable=False)
    diagnostico_id: Mapped[str] = mapped_column(String(36), ForeignKey("diagnosticos.id"), nullable=False)
    carrera: Mapped[str] = mapped_column(String(120), nullable=False)
    respuesta_llm: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Resena(Base):
    __tablename__ = "resenas"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sesion_id: Mapped[str] = mapped_column(String(36), ForeignKey("sesiones.id"), nullable=False)
    comentario: Mapped[str] = mapped_column(String(500), nullable=False)
    sentimiento: Mapped[str] = mapped_column(String(20), nullable=False)
    palabras_clave: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Metrica(Base):
    __tablename__ = "metricas"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    endpoint: Mapped[str] = mapped_column(String(120), nullable=False)
    method: Mapped[str] = mapped_column(String(10), nullable=False)
    status_code: Mapped[int] = mapped_column(Integer, nullable=False)
    tiempo_total_ms: Mapped[float] = mapped_column(Float, nullable=False)
    tiempo_llm_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    request_bytes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    response_bytes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    session_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
