import os
import json
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

MEMORY_FILE = "memoria.json"

# Modelo inicial
chat = ChatOllama(model="mistral")

# Prompt editable
system_prompt = "Eres un asistente conversacional que recuerda lo que el usuario le ha dicho."
prompt_template = lambda sp: ChatPromptTemplate.from_messages([
    ("system", sp),
    MessagesPlaceholder(variable_name="messages")
])

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
            print("⚠️ Archivo de memoria corrupto. Se reiniciará.")
            return []
    return []

def guardar_memoria(history):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        raw_history = [
            {"type": "human" if isinstance(m, HumanMessage) else "ai", "content": m.content}
            for m in history
        ]
        json.dump(raw_history, f, indent=2, ensure_ascii=False)

def mostrar_historial(history):
    print("\n📜 Historial de conversación:")
    for i, m in enumerate(history):
        prefix = "Tú" if isinstance(m, HumanMessage) else "Bot"
        print(f"{prefix}: {m.content}")
    print()

def main():
    global system_prompt
    chat_history = cargar_memoria()
    print("🤖 Chatbot con memoria y comandos activado. Escribe 'salir' para terminar.\n")

    while True:
        user_input = input("Tú: ")

        if user_input.lower() in ["salir", "exit", "quit"]:
            print("💾 Guardando memoria...")
            guardar_memoria(chat_history)
            print("👋 Hasta luego!")
            break

        # 🛠 Comandos especiales
        if user_input.strip() == "/limpiar":
            chat_history = []
            guardar_memoria(chat_history)
            print("🧹 Memoria borrada.")
            continue

        if user_input.strip() == "/historial":
            mostrar_historial(chat_history)
            continue

        if user_input.strip().startswith("/sistema "):
            system_prompt = user_input.replace("/sistema ", "")
            print(f"🔧 Nuevo prompt del sistema: {system_prompt}")
            continue

        # Conversación normal
        chat_history.append(HumanMessage(content=user_input))
        chain = prompt_template(system_prompt) | chat
        response = chain.invoke({"messages": chat_history})
        print(f"Bot: {response.content}\n")
        chat_history.append(AIMessage(content=response.content))


if __name__ == "__main__":
    main()
