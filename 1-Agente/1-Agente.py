import os
import json
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
#ESTE CODIGO ES UN CHATBOT CON OLLAMA, TIENE MEMORIA Y PUEDE RECORDAR LO QUE EL USUARIO LE HA DICHO
MEMORY_FILE = "memoria.json"

# Inicializa el modelo de Ollama (mistral, llama3, etc.)
chat = ChatOllama(model="mistral")

# Prompt del sistema
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente conversacional que recuerda lo que el usuario te ha dicho."),
    MessagesPlaceholder(variable_name="messages")
])

def cargar_memoria():
    """Carga el historial de mensajes desde un archivo JSON si está bien formado"""
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
            print("⚠️ Archivo de memoria corrupto. Se reiniciará.")
            return []
    return []

def guardar_memoria(history):
    """Guarda el historial de mensajes en un archivo JSON"""
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        raw_history = [
            {"type": "human" if isinstance(m, HumanMessage) else "ai", "content": m.content}
            for m in history
        ]
        json.dump(raw_history, f, indent=2, ensure_ascii=False)

def main():
    chat_history = cargar_memoria()
    print("🤖 Chatbot con memoria activado. Escribe 'salir' para terminar.\n")

    while True:
        user_input = input("Tú: ")
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("💾 Guardando memoria...")
            guardar_memoria(chat_history)
            print("👋 Hasta luego!")
            break

        chat_history.append(HumanMessage(content=user_input))

        chain = prompt | chat
        response = chain.invoke({"messages": chat_history})

        print("Bot:", response.content)
        chat_history.append(AIMessage(content=response.content))


if __name__ == "__main__":
    main()
