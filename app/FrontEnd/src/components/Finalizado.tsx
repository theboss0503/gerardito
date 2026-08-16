import type { ResenaResponse } from "../types";

interface Props {
  resultado: ResenaResponse;
  onReiniciar: () => void;
}

const ETIQUETAS: Record<string, string> = {
  POSITIVO: "😊 Positivo",
  NEGATIVO: "😞 Negativo",
  NEUTRAL: "😐 Neutral",
};

export default function Finalizado({ resultado, onReiniciar }: Props) {
  return (
    <section className="paso centrado">
      <h2 className="paso-titulo">Sesión Finalizada 🎉</h2>
      <div className="tarjeta-exito">
        <p>
          🔒 La sesión ha finalizado exitosamente. Tus respuestas han sido procesadas.
        </p>
        <p className="resultado-sentimiento">
          Sentimiento detectado:{" "}
          <span className={`badge badge-${resultado.sentimiento.toLowerCase()}`}>
            {ETIQUETAS[resultado.sentimiento] ?? resultado.sentimiento}
          </span>
        </p>
        {resultado.palabras_clave.length > 0 && (
          <p className="palabras-clave">
            Palabras clave: {resultado.palabras_clave.join(", ")}
          </p>
        )}
      </div>
      <div className="acciones">
        <button type="button" className="btn btn-primario" onClick={onReiniciar}>
          🔄 Volver a hacer el test
        </button>
      </div>
    </section>
  );
}