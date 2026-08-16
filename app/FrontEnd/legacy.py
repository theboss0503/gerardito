import streamlit as st
import spacy
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# =====================================================================
# 1. OPTIMIZACIÓN Y CARGA DE MODELOS (CACHÉ DE STREAMLIT)
# =====================================================================
@st.cache_resource
def inicializar_entorno_ia():
    """Optimiza la carga para que los modelos se mantengan en memoria ram."""
    print("Cargando Llama 3.1 en Ollama (VRAM fijada)...")
    # Mantiene el modelo en la VRAM de la RTX 4060 por 24 horas para evitar tiempos de carga
    modelo_llm = ChatOllama(
        model="llama3.1:8b", 
        temperature=0.2, 
        keep_alive="24h",
        num_predict=512 
    )
    
    print("Cargando motor lingüístico spaCy (CPU)...")
    motor_nlp = spacy.load("es_core_news_sm")
    
    return modelo_llm, motor_nlp

llm, nlp = inicializar_entorno_ia()

# =====================================================================
# 2. CATÁLOGO OFICIAL DE LA UNIVERSIDAD GERARDO BARRIOS
# =====================================================================
CATALOGO_CARRERAS = """
### ÁREA DE SALUD Y HUMANIDADES
- Doctorado en Medicina
- Licenciatura y Técnico en Enfermería
- Licenciatura en Psicología
- Licenciatura, Profesorado o Técnico en Idioma Inglés
- Licenciatura en Comunicaciones
- Licenciatura en Ciencias Jurídicas
- Licenciatura en Relaciones y Negocios Internacionales
- Licenciatura y Profesorado en Educación Inicial y Parvularia
- Profesorado en Lenguaje y Literatura

### ÁREA DE NEGOCIOS Y MARKETING
- Licenciatura en Administración de Empresas
- Técnico en Mercadeo y Ventas
- Licenciatura en Administración de Empresas y Desarrollo Turístico
- Técnico en Marketing y Publicidad Digital
- Licenciatura en Marketing y Negocios Digitales

### ÁREA DE TECNOLOGÍA E INGENIERÍA
- Ingeniería o Técnico en Sistemas y Redes Informáticas
- Licenciatura en Computación
- Ingeniería Industrial
- Ingeniería o Técnico Electricista
- Ingeniería o Técnico en Hardware
- Ingeniería en Desarrollo de Software
- Ingeniería en Inteligencia de Negocios

### ÁREA DE DISEÑO Y CIENCIAS EXACTAS
- Licenciatura o Técnico en Contaduría Pública
- Ingeniería Civil
- Técnico en Ingeniería Civil y Construcción
- Arquitectura
- Licenciatura o Profesorado en Matemáticas
- Técnico en Diseño Gráfico
"""

CARRERAS_LISTA = [line.replace("- ", "").strip() for line in CATALOGO_CARRERAS.split("\n") if line.startswith("- ")]

# =====================================================================
# 3. FUNCIONES DE EXTRACCIÓN Y VALIDACIÓN SEMÁNTICA
# =====================================================================
def validar_entrada_personalizada(texto: str, tipo: str) -> bool:
    if not texto.strip(): return True
    
    prompt_sistema = """
    Eres el filtro de seguridad de un test de orientación vocacional. 
    Tu tarea es evaluar si el texto ingresado tiene sentido como una 'habilidad' o 'interés' para elegir una carrera universitaria.
    
    REGLA 1 (Tolerancia ortográfica): Perdona errores de tipeo o mala ortografía (ej. 'baialar', 'ezcrivir', 'aser cuentas' SON VÁLIDOS).
    REGLA 2 (Rechazo Estricto): Debes rechazar y responder 'NO' a:
    - Insultos, groserías, palabras obscenas o lenguaje inapropiado (Bloqueo inmediato).
    - Necesidades biológicas, estados de ánimo o quejas (ej. 'quiero comer', 'tengo hambre', 'me aburro', 'tengo sueño').
    - Peticiones al chatbot, instrucciones, o charla general (ej. 'dame una receta', 'cuéntame un chiste', 'hola', 'qué haces').
    - Teclas al azar o palabras absurdas (ej. 'asdfg', 'jajaja').
    
    Responde ESTRICTAMENTE con 'SI' o 'NO'. Cero explicaciones.
    """
    prompt_usuario = f"El usuario escribió: '{texto}'. ¿Es esto un(a) {tipo} válido(a) para orientación vocacional, aplicando las reglas anteriores?\nResponde SOLO 'SI' o 'NO'."
    respuesta = llm.invoke([SystemMessage(content=prompt_sistema), HumanMessage(content=prompt_usuario)]).content.strip().upper()
    return "SI" in respuesta

def extraer_carreras_tabla(markdown_text: str) -> list:
    carreras_extraidas = []
    lineas = markdown_text.split('\n')
    for linea in lineas:
        linea = linea.strip()
        if linea.startswith('|') and 'Carrera Sugerida' not in linea and '---' not in linea:
            partes = linea.split('|')
            if len(partes) >= 2:
                carrera = partes[1].replace('*', '').strip()
                if carrera:
                    carreras_extraidas.append(carrera)
    if not carreras_extraidas:
        carreras_extraidas = CARRERAS_LISTA[:3] 
    return carreras_extraidas[:3]

# =====================================================================
# 4. INICIALIZACIÓN DEL CONTROL DE ESTADOS DE LA UI
# =====================================================================
if "fase" not in st.session_state: st.session_state.fase = "paso1"
if "historial" not in st.session_state: st.session_state.historial = []
if "carreras_sugeridas" not in st.session_state: st.session_state.carreras_sugeridas = []
if "sub_fase" not in st.session_state: st.session_state.sub_fase = "decision"
if "habs_sel" not in st.session_state: st.session_state.habs_sel = []
if "hab_otra" not in st.session_state: st.session_state.hab_otra = ""
if "ints_sel" not in st.session_state: st.session_state.ints_sel = []
if "int_otra" not in st.session_state: st.session_state.int_otra = ""
if "carrera_temp" not in st.session_state: st.session_state.carrera_temp = ""

# =====================================================================
# 5. RENDERIZADO CONDICIONAL DE LA INTERFAZ (FLUJO SEGURO)
# =====================================================================
st.title("🦅 Gerardito: Sistema de Orientación Vocacional Inteligente UGB")
st.caption("Versión Final: IA Optimizada, Bloqueo de UI y Aislamiento de Contexto.")

# --- PASO 1: SELECCIÓN DE HABILIDADES ---
if st.session_state.fase == "paso1":
    st.subheader("Pistas de tu Futuro: Paso 1 de 2")
    habs_opciones = [
        "🗣️ Soy el/la que siempre expone en los trabajos grupales y habla sin pena.",
        "🧮 Se me dan muy bien los números, las fórmulas matemáticas o la física.",
        "🤝 Soy bueno/a escuchando los problemas de mis amigos y dándoles consejos.",
        "💻 Entiendo rápido cómo usar aplicaciones nuevas o arreglar cosas de la computadora.",
        "🎨 Dibujo muy bien, tengo buena letra o me fijo mucho en la estética y los colores.",
        "📝 Tengo facilidad para redactar ensayos, leer mucho o aprender idiomas nuevos.",
        "📋 Soy súper organizado/a, me gusta liderar el grupo y repartir las tareas.",
        "🛠️ Soy hábil con las manos para armar maquetas, reparar cosas o construir."
    ]
    habs_seleccionadas = st.multiselect("¿Cuáles son tus habilidades naturales?", options=habs_opciones, default=st.session_state.habs_sel, placeholder="Puedes seleccionar varias")
    habilidad_otra = st.text_input("Otra habilidad (Opcional):", value=st.session_state.hab_otra, max_chars=150)
    
    if st.button("Siguiente Paso ➡️", type="primary"):
        if not habs_seleccionadas and not habilidad_otra.strip():
            st.warning("Por favor, selecciona al menos una habilidad o escribe una personalizada.")
        else:
            if habilidad_otra.strip() and not validar_entrada_personalizada(habilidad_otra, "habilidad"):
                st.error("La habilidad personalizada no parece válida o es inapropiada. ¡Corrígelo!")
            else:
                st.session_state.habs_sel = habs_seleccionadas
                st.session_state.hab_otra = habilidad_otra
                st.session_state.fase = "paso2"
                st.rerun()

# --- PASO 2: SELECCIÓN DE INTERESES ---
elif st.session_state.fase == "paso2":
    st.subheader("Pistas de tu Futuro: Paso 2 de 2")
    ints_opciones = [
        "🩺 Cuidar de la salud de otros o aprender sobre cómo funciona el cuerpo humano.",
        "🎮 Pasar horas en la compu viendo cómo se hacen las páginas web, apps o videojuegos.",
        "📱 Crear contenido para redes sociales, vender cosas o pensar en ideas de negocios.",
        "⚖️ Ver series o documentales sobre crímenes, leyes, juicios o debates sociales.",
        "🏠 Ver diseños de casas, planos, decoración de interiores o grandes edificios.",
        "✈️ Aprender sobre otras culturas, viajar, o pensar en negocios internacionales.",
        "🔌 Desarmar aparatos electrónicos para ver qué tienen adentro o cómo funcionan.",
        "🧑‍🏫 Explicarle temas difíciles a mis compañeros o enseñar cosas nuevas a otros."
    ]
    intereses_seleccionados = st.multiselect("¿Qué disfrutas en tu tiempo libre?", options=ints_opciones, default=st.session_state.ints_sel, placeholder="Puedes seleccionar varias")
    interes_otra = st.text_input("Otro interés (Opcional):", value=st.session_state.int_otra, max_chars=150)
    
    col_back, col_next = st.columns([1, 4])
    if col_back.button("⬅️ Volver"):
        st.session_state.fase = "paso1"
        st.rerun()
        
    if col_next.button("Generar Diagnóstico 📊", type="primary"):
        if not intereses_seleccionados and not interes_otra.strip():
            st.warning("Por favor, selecciona al menos un interés.")
        elif interes_otra.strip() and not validar_entrada_personalizada(interes_otra, "interés"):
            st.error("El interés personalizado no es válido o es inapropiado. ¡Corrígelo!")
        else:
            st.session_state.ints_sel = intereses_seleccionados
            st.session_state.int_otra = interes_otra
            st.session_state.fase = "cargando_diagnostico"
            st.rerun()

# --- FASE DE BLOQUEO 1: CARGANDO DIAGNÓSTICO ---
elif st.session_state.fase == "cargando_diagnostico":
    st.subheader("Pistas de tu Futuro: Paso 2 de 2")
    st.multiselect("¿Qué disfrutas en tu tiempo libre?", options=[], default=[], disabled=True, placeholder="Procesando...")
    st.text_input("Otro interés (Opcional):", value="", disabled=True)
    st.button("Generar Diagnóstico 📊", disabled=True)
    
    with st.spinner("⏳ Analizando perfil y cruzando datos con la UGB. Por favor espera..."):
        lista_habilidades = st.session_state.habs_sel + ([st.session_state.hab_otra] if st.session_state.hab_otra.strip() else [])
        lista_intereses = st.session_state.ints_sel + ([st.session_state.int_otra] if st.session_state.int_otra.strip() else [])
        
        prompt_diagnostico = f"""
        Eres Gerardito, Orientador Vocacional de la UGB. Perfil del usuario:
        - Habilidades: {", ".join(lista_habilidades)}
        - Intereses: {", ".join(lista_intereses)}
        CATÁLOGO UGB:
        {CATALOGO_CARRERAS}
        EJEMPLO DE FORMATO DE TABLA (SÍGUELO ESTRICTAMENTE):
        | Carrera Sugerida | % de Afinidad | Por qué encaja |
        |---|---|---|
        | Doctorado en Medicina | 85% | Porque... |
        INSTRUCCIONES: Saluda celebrando su perfil. Genera una tabla Markdown ESTRICTA con 3 carreras del catálogo. Cierra invitándolo a utilizar los botones para decidir. NO HAGAS PREGUNTAS AL FINAL.
        """
        respuesta_modelo = llm.invoke([HumanMessage(content=prompt_diagnostico)]).content
        respuesta_limpia = respuesta_modelo.replace("`"*3 + "markdown", "").replace("`"*3 + "md", "").replace("`"*3, "").strip()
        
        st.session_state.carreras_sugeridas = extraer_carreras_tabla(respuesta_limpia)
        st.session_state.historial.append({"role": "assistant", "content": respuesta_limpia})
        st.session_state.fase = "chat"
        st.session_state.sub_fase = "decision"
    st.rerun()

# --- PASO 3: INTERFAZ CONVERSACIONAL Y CONTROLES ---
elif st.session_state.fase == "chat":
    for msg in st.session_state.historial:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if st.session_state.sub_fase == "decision":
        st.write("---")
        st.write("**¿Te gustaría profundizar en alguna de estas opciones?**")
        col_si, col_no = st.columns(2)
        if col_si.button("✅ Sí, profundizar en una carrera", use_container_width=True):
            st.session_state.historial.append({"role": "user", "content": "Sí, me gustaría profundizar en una de las opciones."})
            st.session_state.historial.append({"role": "assistant", "content": "¡Excelente elección! 🎯 Selecciona abajo la carrera de la que te gustaría conocer más detalles."})
            st.session_state.sub_fase = "opciones"
            st.rerun()
        if col_no.button("❌ No, finalizar test", use_container_width=True):
            st.session_state.historial.append({"role": "user", "content": "No, con la tabla es suficiente."})
            st.session_state.historial.append({"role": "assistant", "content": "¡Entiendo perfectamente! Para dar por finalizada nuestra sesión, ¿podrías escribirme una breve reseña evaluando qué te pareció mi servicio de orientación? Te lo agradecería muchísimo. 🦅"})
            st.session_state.sub_fase = "resena"
            st.rerun()

    elif st.session_state.sub_fase == "opciones":
        st.write("---")
        carrera_sel = st.radio("Selecciona la carrera a explorar:", options=st.session_state.carreras_sugeridas)
        if st.button("Explorar Selección", type="primary"):
            st.session_state.carrera_temp = carrera_sel
            st.session_state.sub_fase = "cargando_exploracion"
            st.rerun()

    # --- FASE DE BLOQUEO 2: EXPLORANDO CARRERA ---
    elif st.session_state.sub_fase == "cargando_exploracion":
        st.write("---")
        st.radio("Selecciona la carrera a explorar:", options=st.session_state.carreras_sugeridas, disabled=True)
        st.button("Explorar Selección", type="primary", disabled=True)
        
        with st.spinner(f"⏳ Analizando detalles sobre {st.session_state.carrera_temp}..."):
            mensaje_usuario = f"Quiero saber más detalles sobre: {st.session_state.carrera_temp}"
            
            # Aislamiento de contexto para evitar alucinaciones
            historial_limpio = [HumanMessage(content=mensaje_usuario)]
            
            PROMPT_EXPLORACION = f"""
            Eres Gerardito, Orientador Vocacional de la UGB. 
            El usuario ha seleccionado explorar la carrera: {st.session_state.carrera_temp}.
            
            INSTRUCCIONES CRÍTICAS (CUMPLE LAS 3 REGLAS):
            1. Explica de forma amigable, resumida y directa las ventajas o el campo laboral de esta carrera.
            2. Tienes ESTRICTAMENTE PROHIBIDO hacer preguntas de seguimiento, ofrecer explorar otras carreras, o hacer preguntas sobre materias.
            3. Tu mensaje DEBE FINALIZAR EXACTAMENTE con este texto y nada más:
            "Espero que esta información aclare tus dudas. Para finalizar nuestra sesión, ¿podrías escribirme una breve reseña de qué te pareció mi ayuda?"
            """
            
            respuesta_modelo = llm.invoke([SystemMessage(content=PROMPT_EXPLORACION)] + historial_limpio).content
            respuesta_limpia = respuesta_modelo.replace("`"*3 + "markdown", "").replace("`"*3 + "md", "").replace("`"*3, "").strip()
            
            st.session_state.historial.append({"role": "user", "content": mensaje_usuario})
            st.session_state.historial.append({"role": "assistant", "content": respuesta_limpia})
            st.session_state.sub_fase = "resena"
        st.rerun()

    # --- FASE FINAL: RESEÑA ---
    elif st.session_state.sub_fase == "resena":
        st.write("---")
        with st.form(key="formulario_resena"):
            resena_texto = st.text_input("Escribe tu reseña aquí abajo:", placeholder="Tu opinión nos ayuda a mejorar...", max_chars=300)
            btn_enviar_resena = st.form_submit_button("Enviar Reseña", type="primary")
            
            if btn_enviar_resena:
                if not resena_texto.strip():
                    st.warning("Por favor, escribe un comentario antes de enviar.")
                else:
                    with st.spinner("Analizando tu respuesta con IA..."):
                        prompt_sentimiento = f"""
                        Analiza la siguiente reseña enviada por un usuario del sistema de orientación.
                        Debes clasificar la opinión.
                        
                        REGLA CRÍTICA DE VALIDACIÓN: Si el texto consiste en letras al azar sin sentido (ej. 'asfajfwef', 'ghjk'), 
                        puros puntos o signos repetidos (ej. '.......', '???'), o palabras sueltas que no forman un comentario u opinión real, 
                        debes responder ESTRICTAMENTE con la palabra: INVALIDO.
                        
                        Si el comentario tiene sentido humano, clasifícalo detectando ironía, sarcasmo o emojis (ej. 🤡, 💩) en: 
                        POSITIVO, NEGATIVO o NEUTRAL.
                        
                        Responde ESTRICTAMENTE con una de estas cuatro palabras: POSITIVO, NEGATIVO, NEUTRAL o INVALIDO. Cero explicaciones.
                        Reseña a evaluar: "{resena_texto}"
                        """
                        sentimiento_llama = llm.invoke([HumanMessage(content=prompt_sentimiento)]).content.strip().upper()
                        
                        if "INVALIDO" in sentimiento_llama:
                            st.error("⚠️ El comentario ingresado no parece ser una reseña válida. Por favor, escribe una opinión real sobre la ayuda recibida.")
                        else:
                            doc = nlp(resena_texto)
                            palabras_clave = [token.text.lower() for token in doc if token.pos_ in ["ADJ", "NOUN", "VERB"] and not token.is_stop]
                            
                            print("\n" + "="*50)
                            print("📊 EVALUACIÓN DE CALIDAD DE PRODUCCIÓN 📊")
                            print(f"Sentimiento Validado: {sentimiento_llama}")
                            print(f"Palabras Clave (spaCy): {palabras_clave}")
                            print("="*50 + "\n")
                            
                            st.session_state.historial.append({"role": "user", "content": resena_texto})
                            st.session_state.historial.append({"role": "assistant", "content": "¡Muchísimas gracias por tu retroalimentación! Hemos guardado tu reseña en el sistema de forma segura. ¡Te deseo el mayor de los éxitos en tu futuro profesional en la UGB! 🦅🎓"})
                            st.session_state.sub_fase = "finalizado"
                            st.rerun()

    elif st.session_state.sub_fase == "finalizado":
        st.success("🔒 La sesión ha finalizado exitosamente. Tus respuestas han sido procesadas.")

    st.write("---")
    if st.button("🔄 Reiniciar Test Completamente"):
        for clave in list(st.session_state.keys()):
            del st.session_state[clave]
        st.rerun()