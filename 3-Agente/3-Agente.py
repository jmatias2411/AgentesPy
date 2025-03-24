import os
import json
from datetime import datetime
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

CREADOR = "Matías"
MEMORY_FILE = "memoria.json"
MODELO = "mistral"

# Inicializa el modelo Ollama
try:
    chat = ChatOllama(model=MODELO)
except Exception as e:
    print(f"❌ Error al cargar el modelo Ollama '{MODELO}': {e}")
    exit()

# Prompt con personalidad clara
system_prompt = (
    "Responde como un asistente conversacional con estilo amigable y relajado. "
    "Tu personalidad es cercana y natural, sin sonar como una máquina. "
    "Habla con un toque peruano y termina tus frases con 'pe’' cuando suene natural."
)

# Generador de cadena de conversación
def generar_cadena():
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages")
    ])
    return prompt | chat

# Banner decorativo
def mostrar_banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(f"""
           
 ________  ________  _______   ________   _________  _______                              ________     
|\   __  \|\   ____\|\  ___ \ |\   ___  \|\___   ___\\  ___ \                            |\_____  \    
\ \  \|\  \ \  \___|\ \   __/|\ \  \\ \  \|___ \  \_\ \   __/|         ____________      \|____|\ /_   
 \ \   __  \ \  \  __\ \  \_|/_\ \  \\ \  \   \ \  \ \ \  \_|/__      |\____________\          \|\  \  
  \ \  \ \  \ \  \|\  \ \  \_|\ \ \  \\ \  \   \ \  \ \ \  \_|\ \     \|____________|         __\_\  \ 
   \ \__\ \__\ \_______\ \_______\ \__\\ \__\   \ \__\ \ \_______\                           |\_______\
    \|__|\|__|\|_______|\|_______|\|__| \|__|    \|__|  \|_______|                           \|_______|
                                                                                                                                                                                                                                                                                                         

  💬 Modelo: {MODELO}   |   🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
  (GitHub: https://github.com/jmatias2411/AgentesPy.git)
""")
    mostrar_ayuda()

def mostrar_ayuda():
    print("""
🧠 Comandos disponibles:
  /historial        → Mostrar historial de conversación
  /limpiar          → Borrar la memoria guardada
  /sistema <texto>  → Cambiar el prompt del sistema en caliente
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
        print(f"🔧 Nuevo prompt del sistema actualizado:\n{system_prompt}")

    else:
        print("❓ Comando no reconocido. Escribe /ayuda para ver la lista.")

def main():
    global system_prompt
    mostrar_banner()
    chat_history = cargar_memoria()
    cadena = generar_cadena()  # solo una vez

    while True:
        user_input = input("Tú: ").strip()

        if es_comando(user_input):
            procesar_comando(user_input, chat_history)
            cadena = generar_cadena()  # regenerar si el prompt ha cambiado
            continue

        chat_history.append(HumanMessage(content=user_input))
        response = cadena.invoke({"messages": chat_history})
        print(f"Bot: {response.content}\n")
        chat_history.append(AIMessage(content=response.content))

if __name__ == "__main__":
    main()
