import { useEffect, useState } from "react";
import { api, ApiError } from "../api/client";
import { extraerCarreras } from "../lib/markdown";
import type { CarreraSugerida } from "../types";

interface Props {
  habilidades: string[];
  intereses: string[];
  onResultado: (markdown: string, carreras: CarreraSugerida[]) => void;
  onError: (mensaje: string) => void;
}

export default function CargandoDiagnostico({
  habilidades,
  intereses,
  onResultado,
  onError,
}: Props) {
  const [fallo, setFallo] = useState(false);

  useEffect(() => {
    let activo = true;

    (async () => {
      try {
        const resultado = await api.diagnostico({ habilidades, intereses });
        if (!activo) return;
        const carreras = extraerCarreras(resultado.resultado_markdown).map(
          (nombre) => ({ nombre })
        );
        onResultado(resultado.resultado_markdown, carreras);
      } catch (e) {
        if (!activo) return;
        setFallo(true);
        onError(
          e instanceof ApiError
            ? e.message
            : "No se pudo conectar con el servicio de diagnóstico."
        );
      }
    })();

    return () => {
      activo = false;
    };
  }, [habilidades, intereses, onResultado, onError]);

  return (
    <section className="paso centrado">
      <h2 className="paso-titulo">Pistas de tu Futuro · Paso 2 de 2</h2>
      <div className="cargando-box">
        <div className="spinner" />
        <p>Analizando tu perfil y cruzando datos con la UGB. Por favor espera...</p>
      </div>
      {fallo && (
        <p className="mensaje-error">
          Ocurrió un error al generar el diagnóstico. Intenta de nuevo.
        </p>
      )}
    </section>
  );
}