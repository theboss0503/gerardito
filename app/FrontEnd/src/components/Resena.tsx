import { useState } from "react";
import { api, ApiError } from "../api/client";
import type { ResenaResponse } from "../types";

interface Props {
  onEnviada: (resultado: ResenaResponse) => void;
}

export default function Resena({ onEnviada }: Props) {
  const [texto, setTexto] = useState("");
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function enviar() {
    setError(null);
    if (!texto.trim()) {
      setError("Por favor, escribe un comentario antes de enviar.");
      return;
    }

    setCargando(true);
    try {
      const resultado = await api.resena({ comentario: texto });
      setCargando(false);
      onEnviada(resultado);
    } catch (e) {
      setCargando(false);
      setError(
        e instanceof ApiError
          ? "⚠️ " + e.message
          : "⚠️ No se pudo conectar con el servicio de reseñas."
      );
    }
  }

  return (
    <div className="bloque-resena">
      <hr />
      <p className="pregunta">
        <strong>Para finalizar nuestra sesión, escribe una breve reseña evaluando mi servicio:</strong>
      </p>
      <textarea
        className="textarea"
        maxLength={300}
        rows={4}
        value={texto}
        onChange={(e) => setTexto(e.target.value)}
        placeholder="Tu opinión nos ayuda a mejorar..."
      />
      {error && <p className="mensaje-error">{error}</p>}
      <div className="acciones">
        <button
          type="button"
          className="btn btn-primario"
          onClick={enviar}
          disabled={cargando}
        >
          {cargando ? "Analizando tu respuesta con IA..." : "Enviar Reseña"}
        </button>
      </div>
    </div>
  );
}