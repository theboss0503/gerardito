export type TipoValidacion = "habilidad" | "interes";

export interface ValidacionInput {
  texto: string;
  tipo: TipoValidacion;
}

export interface ValidacionResponse {
  es_valido: boolean;
  mensaje_ui: string;
  clasificacion: string | null;
}

export interface PerfilEstudiante {
  habilidades: string[];
  intereses: string[];
}

export interface DiagnosticoResponse {
  resultado_markdown: string;
}

export interface ExploracionResponse {
  respuesta_chat: string;
}

export interface ResenaInput {
  comentario: string;
}

export interface ResenaResponse {
  mensaje: string;
  sentimiento: "POSITIVO" | "NEGATIVO" | "NEUTRAL";
  palabras_clave: string[];
}

export interface CarreraSugerida {
  nombre: string;
}