import os
import json
import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# Archivo donde se guarda la memoria
MEMORY_FILE = "memoria.json"

# Modelo LLM local
chat = ChatOllama(model="mistral")

# Prompt general
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente conversacional que recuerda lo que el usuario te ha dicho."),
    MessagesPlaceholder(variable_name="messages")
])

# Cargar memoria desde archivo
def cargar_memoria():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                contenido = f.read().strip()
                if not contenido:
                    return []
                raw_history = json.loads(contenido)
                history = []
                for m in raw_history:
                    if m["type"] == "human":
                        history.append(HumanMessage(content=m["content"]))
                    elif m["type"] == "ai":
                        history.append(AIMessage(content=m["content"]))
                return history
        except json.JSONDecodeError:
            return []
    return []

# Guardar memoria a archivo
def guardar_memoria(history):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        raw_history = [
            {"type": "human" if isinstance(m, HumanMessage) else "ai", "content": m.content}
            for m in history
        ]
        json.dump(raw_history, f, indent=2, ensure_ascii=False)

# Configuración inicial de la app
st.set_page_config(page_title="Agente IA con memoria", layout="centered")
st.title("🤖 Agente IA con memoria (local)")

# Cargar memoria en sesión
if "history" not in st.session_state:
    st.session_state.history = cargar_memoria()

# Mostrar historial
for msg in st.session_state.history:
    with st.chat_message("user" if isinstance(msg, HumanMessage) else "assistant"):
        st.markdown(msg.content)

# Entrada del usuario
user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    st.session_state.history.append(HumanMessage(content=user_input))

    chain = prompt | chat
    response = chain.invoke({"messages": st.session_state.history})

    st.session_state.history.append(AIMessage(content=response.content))

    # Mostrar respuesta
    with st.chat_message("assistant"):
        st.markdown(response.content)

    guardar_memoria(st.session_state.history)



