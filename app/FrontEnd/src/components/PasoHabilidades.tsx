import { useState } from "react";
import { api, ApiError } from "../api/client";
import { OPCIONES_HABILIDADES } from "../data/opciones";
import type { TipoValidacion } from "../types";

interface Props {
  seleccionadas: string[];
  otra: string;
  onSeleccion: (sel: string[]) => void;
  onOtra: (texto: string) => void;
  onSiguiente: (sel: string[], otra: string, otraCorregida: string) => void;
}

export default function PasoHabilidades({
  seleccionadas,
  otra,
  onSeleccion,
  onOtra,
  onSiguiente,
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

  async function siguiente() {
    setError(null);
    if (seleccionadas.length === 0 && !otra.trim()) {
      setError("Por favor, selecciona al menos una habilidad o escribe una personalizada.");
      return;
    }

    let otraCorregida = otra;

    if (otra.trim()) {
      setCargando(true);
      try {
        const resultado = await api.validarTexto({
          texto: otra,
          tipo: "habilidad" as TipoValidacion,
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

    onSiguiente(seleccionadas, otra, otraCorregida);
  }

  return (
    <section className="paso">
      <div className="progreso">
        <span className="activo">Paso 1 de 2</span>
        <span>Paso 2 de 2</span>
      </div>

      <h2 className="paso-titulo">Pistas de tu Futuro</h2>
      <p className="paso-subtitulo">¿Cuáles son tus habilidades naturales?</p>

      <div className="opciones-grid">
        {OPCIONES_HABILIDADES.map((opcion) => {
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

      <label className="campo" htmlFor="otra-habilidad">
        Otra habilidad (Opcional):
        <input
          id="otra-habilidad"
          type="text"
          maxLength={150}
          value={otra}
          onChange={(e) => onOtra(e.target.value)}
          placeholder="Escribe aquí tu habilidad..."
        />
      </label>

      {error && <p className="mensaje-error">{error}</p>}

      <div className="acciones">
        <button
          type="button"
          className="btn btn-primario"
          onClick={siguiente}
          disabled={cargando}
        >
          {cargando ? "Validando..." : "Siguiente Paso ➡️"}
        </button>
      </div>
    </section>
  );
}
