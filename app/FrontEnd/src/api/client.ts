import type {
  DiagnosticoResponse,
  ExploracionResponse,
  PerfilEstudiante,
  ResenaInput,
  ResenaResponse,
  ValidacionInput,
  ValidacionResponse,
} from "../types";

const BASE_URL = (import.meta.env.VITE_API_URL as string | undefined) ?? "/api/v1";

let _sessionId = crypto.randomUUID();

export function resetSessionId() {
  _sessionId = crypto.randomUUID();
}

function headers(): Record<string, string> {
  return {
    "Content-Type": "application/json",
    "X-Session-Id": _sessionId,
  };
}

async function request<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    let detail = `Error ${res.status}`;
    try {
      const data = await res.json();
      if (data && typeof data.detail === "string") detail = data.detail;
    } catch {
      // ignore
    }
    throw new ApiError(res.status, detail);
  }

  return (await res.json()) as T;
}

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

export const api = {
  validarTexto: (input: ValidacionInput) =>
    request<ValidacionResponse>("/validar-texto", input),

  diagnostico: (perfil: PerfilEstudiante) =>
    request<DiagnosticoResponse>("/diagnostico", perfil),

  explorar: (carrera: string) =>
    request<ExploracionResponse>("/explorar", { carrera }),

  resena: (input: ResenaInput) => request<ResenaResponse>("/resena", input),
};