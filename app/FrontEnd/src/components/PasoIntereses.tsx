import { useState } from "react";
import { api, ApiError } from "../api/client";
import { OPCIONES_INTERESES } from "../data/opciones";
import type { TipoValidacion } from "../types";

interface Props {
  seleccionadas: string[];
  otra: string;
  errorExterno?: string | null;
  onSeleccion: (sel: string[]) => void;
  onOtra: (texto: string) => void;
  onVolver: () => void;
  onGenerar: (sel: string[], otra: string, otraCorregida: string) => void;
}

export default function PasoIntereses({
  seleccionadas,
  otra,
  errorExterno,
  onSeleccion,
  onOtra,
  onVolver,
  onGenerar,
}: Props) {
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function toggle(opcion: string) {
    if (seleccionadas.includes(opcion)) {
      onSeleccion(seleccionadas.filter((o) => o !== opcion));
    } else {
      onSeleccion([...seleccionadas, opcion]);
    }
  }

  async function generar() {
    setError(null);
    if (seleccionadas.length === 0 && !otra.trim()) {
      setError("Por favor, selecciona al menos un interés.");
      return;
    }

    let otraCorregida = otra;

    if (otra.trim()) {
      setCargando(true);
      try {
        const resultado = await api.validarTexto({
          texto: otra,
          tipo: "interes" as TipoValidacion,
        });
        if (!resultado.es_valido) {
          setError(resultado.mensaje_ui);
          setCargando(false);
          return;
        }
        if (resultado.clasificacion) {
          otraCorregida = resultado.clasificacion;
        }
      } catch (e) {
        setError(
          e instanceof ApiError ? e.message : "No se pudo conectar con el servicio de validación."
        );
        setCargando(false);
        return;
      }
      setCargando(false);
    }

    onGenerar(seleccionadas, otra, otraCorregida);
  }

  return (
    <section className="paso">
      <div className="progreso">
        <span>Paso 1 de 2</span>
        <span className="activo">Paso 2 de 2</span>
      </div>

      <h2 className="paso-titulo">Pistas de tu Futuro</h2>
      <p className="paso-subtitulo">¿Qué disfrutas en tu tiempo libre?</p>

      <div className="opciones-grid">
        {OPCIONES_INTERESES.map((opcion) => {
          const activa = seleccionadas.includes(opcion);
          return (
            <button
              key={opcion}
              type="button"
              className={`opcion-card ${activa ? "opcion-activa" : ""}`}
              onClick={() => toggle(opcion)}
              aria-pressed={activa}
            >
              <span className="opcion-chek">{activa ? "☑" : "☐"}</span>
              {opcion}
            </button>
          );
        })}
      </div>

      <label className="campo" htmlFor="otro-interes">
        Otro interés (Opcional):
        <input
          id="otro-interes"
          type="text"
          maxLength={150}
          value={otra}
          onChange={(e) => onOtra(e.target.value)}
          placeholder="Escribe aquí tu interés..."
        />
      </label>

      {(error ?? errorExterno) && (
        <p className="mensaje-error">{error ?? errorExterno}</p>
      )}

      <div className="acciones fila">
        <button type="button" className="btn btn-secundario" onClick={onVolver}>
          ⬅️ Volver
        </button>
        <button
          type="button"
          className="btn btn-primario"
          onClick={generar}
          disabled={cargando}
        >
          {cargando ? "Validando..." : "Generar Diagnóstico 📊"}
        </button>
      </div>
    </section>
  );
}
