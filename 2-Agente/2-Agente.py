import os
import json
from datetime import datetime
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

MEMORY_FILE = "memoria.json"
MODELO = "mistral"

# Inicializa el modelo Ollama
try:
    chat = ChatOllama(model=MODELO)
except Exception as e:
    print(f"❌ Error al cargar el modelo Ollama '{MODELO}': {e}")
    exit()

# Prompt editable
system_prompt = "Eres un asistente conversacional que recuerda lo que el usuario le ha dicho."
prompt_template = lambda sp: ChatPromptTemplate.from_messages([
    ("system", sp),
    MessagesPlaceholder(variable_name="messages")
])

def mostrar_banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(f"""
 ________  ________  _______   ________   _________  _______                               _______         
|\   __  \|\   ____\|\  ___ \ |\   ___  \|\___   ___\\  ___ \                             /  ___  \        
\ \  \|\  \ \  \___|\ \   __/|\ \  \\ \  \|___ \  \_\ \   __/|         ____________      /__/|_/  /|       
 \ \   __  \ \  \  __\ \  \_|/_\ \  \\ \  \   \ \  \ \ \  \_|/__      |\____________\    |__|//  / /       
  \ \  \ \  \ \  \|\  \ \  \_|\ \ \  \\ \  \   \ \  \ \ \  \_|\ \     \|____________|        /  /_/__      
   \ \__\ \__\ \_______\ \_______\ \__\\ \__\   \ \__\ \ \_______\                          |\________\    
    \|__|\|__|\|_______|\|_______|\|__| \|__|    \|__|  \|_______|                           \|_______|    

  💬 Modelo: {MODELO}   |   🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
  (GitHub: https://github.com/jmatias2411/AgentesPy.git)

🧠 Comandos disponibles:
  /historial        → Mostrar historial de conversación
  /limpiar          → Borrar la memoria guardada
  /sistema <texto>  → Cambiar el prompt del sistema
  /ayuda            → Mostrar esta lista de comandos
  salir             → Cerrar el chatbot
""")

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
    for m in history:
        prefix = "Tú" if isinstance(m, HumanMessage) else "Bot"
        print(f"{prefix}: {m.content}")
    print()

def mostrar_ayuda():
    print("""
    🧠 Comandos disponibles:
    /historial        → Mostrar historial de conversación
    /limpiar          → Borrar la memoria guardada
    /sistema <texto>  → Cambiar el prompt del sistema en caliente
    /ayuda            → Mostrar esta lista de comandos
    salir             → Cerrar el chatbot
    """)

def es_comando(texto):
    return texto.startswith("/") or texto.lower() in ["salir", "exit", "quit"]

def procesar_comando(texto, history):
    global system_prompt
    if texto.lower() in ["salir", "exit", "quit"]:
        print("💾 Guardando memoria...")
        guardar_memoria(history)
        print("👋 Hasta luego!")
        exit()

    elif texto == "/limpiar":
        history.clear()
        guardar_memoria(history)
        print("🧹 Memoria borrada.")

    elif texto == "/historial":
        mostrar_historial(history)
    
    elif texto == "/ayuda":
        mostrar_ayuda()

    elif texto.startswith("/sistema "):
        system_prompt = texto.replace("/sistema ", "")
        print(f"🔧 Nuevo prompt del sistema: {system_prompt}")

    else:
        print("❓ Comando no reconocido.")

def main():
    global system_prompt
    mostrar_banner()
    chat_history = cargar_memoria()

    while True:
        user_input = input("Tú: ").strip()

        if es_comando(user_input):
            procesar_comando(user_input, chat_history)
            continue

        # Conversación normal
        chat_history.append(HumanMessage(content=user_input))
        chain = prompt_template(system_prompt) | chat
        response = chain.invoke({"messages": chat_history})
        print(f"Bot: {response.content}\n")
        chat_history.append(AIMessage(content=response.content))


if __name__ == "__main__":
    main()
