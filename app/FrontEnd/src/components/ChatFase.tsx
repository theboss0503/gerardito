import MarkdownTabla from "./MarkdownTabla";

export interface Mensaje {
  rol: "usuario" | "asistente";
  contenido: string;
}

export type SubFase = "decision" | "opciones" | "cargandoExploracion" | "resena";

interface Props {
  mensajes: Mensaje[];
  subFase: SubFase;
  carreras: string[];
  carreraSeleccionada: string;
  explorando: boolean;
  error: string | null;
  onSiProfundizar: () => void;
  onNoFinalizar: () => void;
  onSeleccionarCarrera: (carrera: string) => void;
  onExplorar: () => void;
}

export default function ChatFase({
  mensajes,
  subFase,
  carreras,
  carreraSeleccionada,
  explorando,
  error,
  onSiProfundizar,
  onNoFinalizar,
  onSeleccionarCarrera,
  onExplorar,
}: Props) {
  return (
    <section className="chat-fase">
      <div className="chat-burbujas">
        {mensajes.map((msg, i) => (
          <div key={i} className={`burbuja burbuja-${msg.rol}`}>
            {msg.rol === "asistente" ? (
              <MarkdownTabla contenido={msg.contenido} />
            ) : (
              <p>{msg.contenido}</p>
            )}
          </div>
        ))}
      </div>

      {subFase === "decision" && (
        <div className="bloque-decision">
          <hr />
          <p className="pregunta">
            <strong>¿Te gustaría profundizar en alguna de estas opciones?</strong>
          </p>
          <div className="acciones fila">
            <button type="button" className="btn btn-primario" onClick={onSiProfundizar}>
              ✅ Sí, profundizar en una carrera
            </button>
            <button type="button" className="btn btn-secundario" onClick={onNoFinalizar}>
              ❌ No, finalizar test
            </button>
          </div>
        </div>
      )}

      {subFase === "opciones" && (
        <div className="bloque-opciones">
          <hr />
          <p className="pregunta">
            <strong>Selecciona la carrera que te gustaría explorar:</strong>
          </p>
          <div className="radio-lista">
            {carreras.map((carrera) => (
              <label key={carrera} className="radio-item">
                <input
                  type="radio"
                  name="carrera"
                  value={carrera}
                  checked={carreraSeleccionada === carrera}
                  onChange={() => onSeleccionarCarrera(carrera)}
                />
                <span>{carrera}</span>
              </label>
            ))}
          </div>
          <div className="acciones">
            <button
              type="button"
              className="btn btn-primario"
              onClick={onExplorar}
              disabled={!carreraSeleccionada || explorando}
            >
              {explorando ? "Analizando..." : "Explorar Selección"}
            </button>
          </div>
        </div>
      )}

      {subFase === "cargandoExploracion" && (
        <div className="cargando-box">
          <div className="spinner" />
          <p>Analizando detalles sobre la carrera seleccionada...</p>
        </div>
      )}

      {error && <p className="mensaje-error">{error}</p>}
    </section>
  );
}
