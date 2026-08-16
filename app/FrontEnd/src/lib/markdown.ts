import { CARRERAS_FALLBACK } from "../data/opciones";

export function extraerCarreras(markdown: string): string[] {
  const carreras: string[] = [];
  const lineas = markdown.split("\n");

  for (const linea of lineas) {
    const l = linea.trim();
    if (l.startsWith("|") && !l.includes("Carrera Sugerida") && !l.includes("---")) {
      const partes = l.split("|");
      if (partes.length >= 2) {
        const carrera = partes[1].replace(/\*/g, "").trim();
        if (carrera) carreras.push(carrera);
      }
    }
  }

  return carreras.length >= 1 ? carreras.slice(0, 3) : CARRERAS_FALLBACK;
}
