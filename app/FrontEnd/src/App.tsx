import { useCallback, useState } from "react";
import { api, ApiError, resetSessionId } from "./api/client";
import PasoHabilidades from "./components/PasoHabilidades";
import PasoIntereses from "./components/PasoIntereses";
import CargandoDiagnostico from "./components/CargandoDiagnostico";
import ChatFase, { type Mensaje, type SubFase } from "./components/ChatFase";
import Resena from "./components/Resena";
import Finalizado from "./components/Finalizado";
import type { ResenaResponse } from "./types";

type Fase =
  | "habilidades"
  | "intereses"
  | "cargandoDiagnostico"
  | "chat"
  | "finalizado";

const estadoInicial = () => ({
  fase: "habilidades" as Fase,
  subFase: "decision" as SubFase,
  habilidades: [] as string[],
  habilidadOtra: "",
  habilidadCorregida: "",
  intereses: [] as string[],
  interesOtro: "",
  interesCorregido: "",
  mensajes: [] as Mensaje[],
  carreras: [] as string[],
  carreraSeleccionada: "",
  explorando: false,
  error: null as string | null,
  resultadoResena: null as ResenaResponse | null,
});

export default function App() {
  const [estado, setEstado] = useState(estadoInicial);

  function reiniciar() {
    resetSessionId();
    setEstado(estadoInicial());
  }

  const alSiguienteHabilidades = useCallback(
    (sel: string[], otra: string, otraCorregida: string) => {
      setEstado((e) => ({
        ...e,
        habilidades: sel,
        habilidadOtra: otra,
        habilidadCorregida: otraCorregida,
        fase: "intereses",
      }));
    },
    []
  );

  const alGenerarIntereses = useCallback(
    (sel: string[], otra: string, otraCorregida: string) => {
      setEstado((e) => ({
        ...e,
        intereses: sel,
        interesOtro: otra,
        interesCorregido: otraCorregida,
        fase: "cargandoDiagnostico",
      }));
    },
    []
  );

  const alResultadoDiagnostico = useCallback(
    (markdown: string, carreras: { nombre: string }[]) => {
      setEstado((e) => ({
        ...e,
        mensajes: [{ rol: "asistente", contenido: markdown }],
        carreras: carreras.map((c) => c.nombre),
        fase: "chat",
        subFase: "decision",
      }));
    },
    []
  );

  const alErrorDiagnostico = useCallback((mensaje: string) => {
    setEstado((e) => ({ ...e, error: mensaje, fase: "intereses" }));
  }, []);

  function siProfundizar() {
    setEstado((e) => ({
      ...e,
      subFase: "opciones",
    }));
  }

  function noFinalizar() {
    setEstado((e) => ({
      ...e,
      subFase: "resena",
    }));
  }

  async function explorar() {
    setEstado((e) => ({ ...e, subFase: "cargandoExploracion", explorando: true, error: null }));
    try {
      const resultado = await api.explorar(estado.carreraSeleccionada);
      setEstado((e) => ({
        ...e,
        mensajes: [
          ...e.mensajes,
          { rol: "asistente", contenido: resultado.respuesta_chat },
        ],
        subFase: "resena",
        explorando: false,
      }));
    } catch (err) {
      setEstado((e) => ({
        ...e,
        subFase: "opciones",
        explorando: false,
        error: err instanceof ApiError ? err.message : "Error al explorar la carrera.",
      }));
    }
  }

  function alEnviadaResena(resultado: ResenaResponse) {
    setEstado((e) => ({
      ...e,
      resultadoResena: resultado,
      fase: "finalizado",
    }));
  }

  const habilidadesParaDiagnostico = [
    ...estado.habilidades,
    ...(estado.habilidadCorregida.trim() ? [estado.habilidadCorregida] : []),
  ];

  const interesesParaDiagnostico = [
    ...estado.intereses,
    ...(estado.interesCorregido.trim() ? [estado.interesCorregido] : []),
  ];

  return (
    <div className="app">
      <header className="cabecera">
        <h1>🦅 Gerardito</h1>
        <p>Sistema de Orientación Vocacional Inteligente · UGB</p>
      </header>

      <main className="contenido">
        {estado.fase === "habilidades" && (
          <PasoHabilidades
            seleccionadas={estado.habilidades}
            otra={estado.habilidadOtra}
            onSeleccion={(sel) => setEstado((e) => ({ ...e, habilidades: sel }))}
            onOtra={(t) => setEstado((e) => ({ ...e, habilidadOtra: t }))}
            onSiguiente={alSiguienteHabilidades}
          />
        )}

        {estado.fase === "intereses" && (
          <PasoIntereses
            seleccionadas={estado.intereses}
            otra={estado.interesOtro}
            errorExterno={estado.error}
            onSeleccion={(sel) => setEstado((e) => ({ ...e, intereses: sel }))}
            onOtra={(t) => setEstado((e) => ({ ...e, interesOtro: t }))}
            onVolver={() => setEstado((e) => ({ ...e, fase: "habilidades" }))}
            onGenerar={alGenerarIntereses}
          />
        )}

        {estado.fase === "cargandoDiagnostico" && (
          <CargandoDiagnostico
            habilidades={habilidadesParaDiagnostico}
            intereses={interesesParaDiagnostico}
            onResultado={alResultadoDiagnostico}
            onError={alErrorDiagnostico}
          />
        )}

        {estado.fase === "chat" && (
          <>
            <ChatFase
              mensajes={estado.mensajes}
              subFase={estado.subFase}
              carreras={estado.carreras}
              carreraSeleccionada={estado.carreraSeleccionada}
              explorando={estado.explorando}
              error={estado.error}
              onSiProfundizar={siProfundizar}
              onNoFinalizar={noFinalizar}
              onSeleccionarCarrera={(c) =>
                setEstado((e) => ({ ...e, carreraSeleccionada: c }))
              }
              onExplorar={explorar}
            />
            {estado.subFase === "resena" && <Resena onEnviada={alEnviadaResena} />}
          </>
        )}

        {estado.fase === "finalizado" && estado.resultadoResena && (
          <Finalizado resultado={estado.resultadoResena} onReiniciar={reiniciar} />
        )}
      </main>

      <footer className="pie">
        Universidad Gerardo Barrios · Módulo 4 - Desarrollo de Aplicaciones con IA
      </footer>
    </div>
  );
}
