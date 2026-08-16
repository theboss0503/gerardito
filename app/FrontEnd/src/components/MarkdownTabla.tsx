interface TablaExtraida {
  cabecera: string[];
  filas: string[][];
}

function parsearTabla(markdown: string): TablaExtraida | null {
  const lineas = markdown.split("\n").map((l) => l.trim());
  const idxCabecera = lineas.findIndex(
    (l) => l.startsWith("|") && l.includes("Carrera Sugerida")
  );
  if (idxCabecera === -1) return null;

  const cabecera = lineas[idxCabecera]
    .split("|")
    .map((c) => c.replace(/\*/g, "").trim())
    .filter((c) => c.length > 0);

  const filas: string[][] = [];
  for (let i = idxCabecera + 2; i < lineas.length; i++) {
    const l = lineas[i].trim();
    if (!l.startsWith("|")) break;
    if (l.replace(/-|\||:/g, "").trim() === "") continue;
    const celdas = l
      .split("|")
      .map((c) => c.replace(/\*/g, "").trim())
      .filter((c) => c.length > 0);
    if (celdas.length) filas.push(celdas);
  }

  return { cabecera, filas };
}

export default function MarkdownTabla({ contenido }: { contenido: string }) {
  const tabla = parsearTabla(contenido);

  if (!tabla) {
    return (
      <div className="markdown-cuerpo">
        {contenido.split("\n").map((linea, i) => (
          <p key={i}>{linea}</p>
        ))}
      </div>
    );
  }

  const [antes, resto] = contenido.split(/^\|.*Carrera Sugerida.*\|\s*$/m, 2);

  return (
    <div className="markdown-cuerpo">
      {antes
        ?.trim()
        .split("\n")
        .filter((l) => l.trim() && !l.trim().startsWith("|"))
        .map((linea, i) => <p key={i}>{linea}</p>)}

      <div className="tabla-wrap">
        <table className="tabla-carreras">
          <thead>
            <tr>
              {tabla.cabecera.map((h, i) => (
                <th key={i}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {tabla.filas.map((fila, i) => (
              <tr key={i}>
                {fila.map((celda, j) => (
                  <td key={j} className={j === 0 ? "celda-carrera" : ""}>
                    {celda}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {resto
        ?.trim()
        .split("\n")
        .filter((l) => l.trim() && !l.trim().startsWith("|"))
        .map((linea, i) => <p key={i}>{linea}</p>)}
    </div>
  );
}