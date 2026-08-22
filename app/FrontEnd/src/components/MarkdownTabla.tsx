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

function parsearLineaMD(linea: string): React.ReactNode {
  const partes: React.ReactNode[] = [];
  let restante = linea;
  let key = 0;

  while (restante.length > 0) {
    const negritaMatch = restante.match(/^(.*?)\*\*(.*?)\*\*/);
    if (negritaMatch) {
      if (negritaMatch[1]) partes.push(<span key={key++}>{negritaMatch[1]}</span>);
      partes.push(<strong key={key++}>{negritaMatch[2]}</strong>);
      restante = restante.slice(negritaMatch[0].length);
      continue;
    }

    const cursivaMatch = restante.match(/^(.*?)\*([^*]+?)\*/);
    if (cursivaMatch) {
      if (cursivaMatch[1]) partes.push(<span key={key++}>{cursivaMatch[1]}</span>);
      partes.push(<em key={key++}>{cursivaMatch[2]}</em>);
      restante = restante.slice(cursivaMatch[0].length);
      continue;
    }

    partes.push(<span key={key++}>{restante}</span>);
    break;
  }

  return partes.length === 1 ? partes[0] : <>{partes}</>;
}

function renderizarLinea(linea: string, i: number): React.ReactNode {
  const texto = linea.trim();

  const headingMatch = texto.match(/^(#{1,6})\s+(.+)/);
  if (headingMatch) {
    const nivel = headingMatch[1].length;
    const Tag = `h${Math.min(nivel, 6)}` as keyof JSX.IntrinsicElements;
    return <Tag key={i}>{parsearLineaMD(headingMatch[2])}</Tag>;
  }

  const bulletMatch = texto.match(/^[\*\-]\s+(.+)/);
  if (bulletMatch) {
    return (
      <li key={i} className="markdown-li">
        {parsearLineaMD(bulletMatch[1])}
      </li>
    );
  }

  if (!texto) return null;

  return <p key={i}>{parsearLineaMD(texto)}</p>;
}

export default function MarkdownTabla({ contenido }: { contenido: string }) {
  const tabla = parsearTabla(contenido);

  if (!tabla) {
    const lineas = contenido.split("\n");
    const elementos: React.ReactNode[] = [];
    let itemsLista: React.ReactNode[] = [];

    const cerrarLista = () => {
      if (itemsLista.length > 0) {
        elementos.push(
          <ul key={`ul-${elementos.length}`} className="markdown-ul">
            {itemsLista}
          </ul>
        );
        itemsLista = [];
      }
    };

    for (let i = 0; i < lineas.length; i++) {
      const linea = lineas[i].trim();
      const esBullet = /^[\*\-]\s+/.test(linea);

      if (esBullet) {
        itemsLista.push(renderizarLinea(linea, i));
      } else {
        cerrarLista();
        const el = renderizarLinea(linea, i);
        if (el) elementos.push(el);
      }
    }
    cerrarLista();

    return <div className="markdown-cuerpo">{elementos}</div>;
  }

  const [antes, resto] = contenido.split(/^\|.*Carrera Sugerida.*\|\s*$/m, 2);

  return (
    <div className="markdown-cuerpo">
      {antes
        ?.trim()
        .split("\n")
        .filter((l) => l.trim() && !l.trim().startsWith("|"))
        .map((linea, i) => <p key={i}>{parsearLineaMD(linea.trim())}</p>)}

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
        .map((linea, i) => <p key={i}>{parsearLineaMD(linea.trim())}</p>)}
    </div>
  );
}
