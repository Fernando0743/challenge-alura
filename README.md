# 🤖 Agente de Soporte Técnico y Preguntas - CloudPulse SaaS

¡Bienvenido al repositorio oficial del **Agente Inteligente de Soporte para CloudPulse**! Este proyecto es una solución basada en Inteligencia Artificial Generativa y la arquitectura **RAG (Retrieval-Augmented Generation)**, diseñada para responder preguntas en lenguaje natural utilizando como base de conocimiento la documentación técnica y comercial de la plataforma SaaS CloudPulse.

---

## 1. Descripción General del Proyecto

CloudPulse es una plataforma SaaS ficticia de monitoreo de infraestructura en la nube. Con el objetivo de optimizar la atención a usuarios y reducir la carga de soporte técnico, se construyó este agente virtual interactivo.

El agente es capaz de:
- Procesar e ingerir documentación en formato **PDF**.
- Realizar búsquedas semánticas eficientes sobre la información almacenada.
- Responder dudas sobre arquitectura, tecnologías de backend/frontend, planes de precio, políticas de SLA y soporte.
- Reconocer sus límites: Si una pregunta no está respaldada por la documentación, el agente responderá explícitamente que no cuenta con esa información, evitando alucinaciones.

---

## 2. Arquitectura de la Solución

La solución utiliza una arquitectura **RAG (Retrieval-Augmented Generation)** ligera y de alto rendimiento optimizada para entornos Cloud sin consumo excesivo de memoria:
graph LR
    PDF["[ Documento PDF ]"] --> Loader["[ PyPDFLoader & TextSplitter ]"]
    Loader --> Chunks["[ Chunks de Texto ]"]
    
    Embeddings["[ Cohere Embeddings ]"] --> Retriever["[ FAISS Retriever ]"]
    Retriever --> LLM["[ ChatCohere (Command-R) ]"]
    LLM --> UI["[ Interfaz Streamlit ]"]

    Chunks -. Contexto .-> Retriever
  
1. **Ingesta de Documentos:** El PDF con la especificación de CloudPulse es cargado mediante `PyPDFLoader` y dividido en fragmentos (*chunks*) utilizando `RecursiveCharacterTextSplitter`.
2. **Vectorización (Embeddings):** Los fragmentos son convertidos en vectores de alta dimensión mediante la API de `CohereEmbeddings` (`embed-multilingual-light-v3.0`), eliminando la carga computacional local.
3. **Almacenamiento Vectorial:** Se utiliza **FAISS** como base de datos vectorial en memoria por su velocidad y bajo consumo de recursos.
4. **Orquestación RAG (LCEL):** LangChain coordina la recuperación del contexto relevante y compone el prompt para el Modelo de Lenguaje.
5. **Generación de Respuestas:** El LLM `ChatCohere` (`command-r7b-12-2024`) procesa la consulta junto al contexto extraído para generar una respuesta precisa y profesional.

---

## 3. Tecnologías y Herramientas Utilizadas

- **Lenguaje de Programación:** Python 3.11
- **Orquestador de IA:** [LangChain](https://www.langchain.com/) (LangChain Core, Community y Cohere)
- **Modelo de Lenguaje (LLM):** Cohere (`command-r7b-12-2024`)
- **Embeddings:** Cohere (`embed-multilingual-light-v3.0`)
- **Base de Datos Vectorial:** FAISS (Facebook AI Similarity Search)
- **Procesamiento de Documentos:** `PyPDF`
- **Interfaz Web:** Streamlit
- **Despliegue y Hosting:** Render (Web Service)

---

## 4. Instrucciones para Ejecutar el Proyecto

### Prerrequisitos
- Tener instalado **Python 3.10** o superior.
- Obtener una **API Key gratuita** en [Cohere Dashboard](https://dashboard.cohere.com/).

---

### Instalación Local

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/TU_USUARIO/alura-agente-saas.git](https://github.com/TU_USUARIO/alura-agente-saas.git)
   cd alura-agente-saas
2. **Crear y activar un entorno virtual (opcional pero recomendado):**

   ```bash
   python -m venv venv
   
   # En Windows:
   venv\Scripts\activate
   
   # En macOS/Linux:
   source venv/bin/activate
3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
4. **Configurar la API Key:**
   Establece la variable de entorno en tu terminal:
   * Windows (PowerShell): `$env:COHERE_API_KEY="tu_api_key_aqui"`
   * Linux / macOS: `export COHERE_API_KEY="tu_api_key_aqui"`
5. **Iniciar la aplicación:**
    ```bash
    streamlit run app.py
La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`.

---

## 5. Ejemplos de Preguntas que el Agente Puede Responder

El agente está capacitado para responder preguntas en lenguaje natural sobre diversos dominios de la plataforma CloudPulse, así como para gestionar consultas fuera de su base de conocimiento:

### Arquitectura, Frontend y Backend
- `¿Qué lenguajes de programación se utilizan en el backend de la plataforma?`
- `¿Qué tecnología o framework se utiliza para la interfaz de usuario (frontend)?`
- `¿Cómo funciona el pipeline de procesamiento de métricas e ingesta de telemetría?`

### Planes, Precios y Límites
- `¿Cuánto cuesta el plan Pro y qué nivel de soporte incluye?`
- `¿Cuáles son las diferencias principales entre el plan Starter y el plan Enterprise?`
- `¿Cuántos servidores puedo monitorear con la suscripción básica y cuál es el límite de retención de datos?`

### Seguridad, Políticas de SLA y Garantías
- `¿Cuál es el porcentaje de disponibilidad (SLA) garantizado por CloudPulse?`
- `¿Qué tipo de cifrado y medidas de seguridad se aplican a los datos almacenados?`
- `¿Cómo se gestionan las ventanas de mantenimiento programado?`

### Manejo de Respuestas Fuera de Contexto (Control de Alucinaciones)
Para evitar la generación de información falsa, el agente reconoce explícitamente cuando una consulta no se encuentra en la documentación:
- `¿Cuál es la política de reembolso para eventos climáticos o desastres naturales?`
- `¿Tienen oficinas físicas o soporte presencial en Ciudad de México?`
- `¿Ofrecen descuentos especiales para estudiantes o instituciones educativas?`

## 6. Ejemplos de Respuestas Generadas por el Agente

A continuación se muestran los casos de prueba ejecutados en la aplicación desplegada en **Render**:

### Ejemplo 1: Consulta sobre Arquitectura
Prueba del agente respondiendo sobre tecnologías del backend (Python y Go).

![Consulta sobre Arquitectura](ruta/a/tu/captura-ejemplo1.png)

---

### Ejemplo 2: Consulta sobre Precios y Soporte
Prueba del agente respondiendo sobre costos del plan Pro y nivel de soporte técnico.

![Consulta sobre Precios](ruta/a/tu/captura-ejemplo2.png)

---

### Ejemplo 3: Pregunta Fuera de Contexto
Prueba del control de alucinaciones respondiendo correctamente ante información no disponible en el documento.

![Consulta Fuera de Contexto](ruta/a/tu/captura-ejemplo3.png)

## Evidencia del Despliegue en la Nube

El proyecto fue desplegado con éxito en la plataforma **Render** utilizando integración continua desde GitHub y variables de entorno para la gestión segura de claves.

- **Enlace Público de la Aplicación en Render:** [https://challenge-alura-jhd3.onrender.com]

---

## ✍️ Autor

Creado por **Fernando Vázquez** como parte del **Challenge Alura Latam / ONE (Oracle Next Education)** — Formación Tech Builder
