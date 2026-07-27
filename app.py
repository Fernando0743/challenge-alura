import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_cohere import ChatCohere, CohereEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

st.set_page_config(page_title="Agente de Soporte - CloudPulse SaaS", page_icon="🤖")

st.title("🤖 Agente de Soporte Técnico y Preguntas - CloudPulse")
st.markdown("Haz preguntas en lenguaje natural sobre la arquitectura, precios, políticas y SLA de la plataforma.")


cohere_api_key = os.environ.get("COHERE_API_KEY")

if not cohere_api_key:
    st.error("No se encontró la API Key de Cohere.")
    st.stop()

@st.cache_resource
def inicializar_agente():
    dir_actual = os.path.dirname(os.path.abspath(__file__))
    
    pdf_path = os.path.join(dir_actual, "documento_saas.pdf")
    if not os.path.exists(pdf_path):
        archivos = [f for f in os.listdir(dir_actual) if f.endswith('.pdf')]
        if archivos:
            pdf_path = os.path.join(dir_actual, archivos[0])
        else:
            st.error("No se encontró ningún archivo PDF en el repositorio.")
            st.stop()

    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    splits = text_splitter.split_documents(docs)

    embeddings = CohereEmbeddings(
        model="embed-multilingual-light-v3.0", 
        cohere_api_key=cohere_api_key
    )
    vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    llm = ChatCohere(
        model="command-r7b-12-2024", 
        cohere_api_key=cohere_api_key,
        temperature=0.2
    )

    system_prompt = (
        "Eres un asistente virtual experto de la plataforma SaaS CloudPulse.\n"
        "Responde a las preguntas utilizando únicamente la información proporcionada en el contexto.\n"
        "Si no sabes la respuesta o no está en el documento, responde: 'No cuento con esa información en la documentación, ¿Alguna otra pregunta?'.\n"
        "Mantén tus respuestas profesionales, claras y directas.\n\n"
        "Contexto:\n{context}\n\n"
        "Pregunta: {question}"
    )

    prompt = ChatPromptTemplate.from_template(system_prompt)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # 6. Cadena RAG con LCEL
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain

with st.spinner("Cargando la base de conocimientos..."):
    rag_chain = inicializar_agente()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Soy tu asistente virtual de CloudPulse SaaS. ¿En qué te puedo ayudar hoy?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt_input := st.chat_input("Escribe tu pregunta aquí (ej. ¿Qué lenguajes usan en el backend?):"):
    st.session_state.messages.append({"role": "user", "content": prompt_input})
    st.chat_message("user").write(prompt_input)

    with st.chat_message("assistant"):
        with st.spinner("Buscando en la documentación..."):
            respuesta = rag_chain.invoke(prompt_input)
            st.write(respuesta)
            st.session_state.messages.append({"role": "assistant", "content": respuesta})
