# 🧠 Agentes IA con LangChain y Ollama

Este repositorio contiene una colección de **agentes conversacionales de inteligencia artificial** desarrollados con **[LangChain](https://www.langchain.com/)** y ejecutados de forma **local usando [Ollama](https://ollama.com/)** con modelos como **Mistral**.

Cada agente está diseñado con una **personalidad, propósito y comportamiento diferente**, ideal para experimentar con interfaces conversacionales inteligentes, automatización o asistentes personalizados sin depender de APIs externas.

---

## 🚀 Tecnologías utilizadas

- **🧠 LangChain** – Para construir cadenas de procesamiento de lenguaje natural.
- **🧱 LangChain Core / Community / Ollama** – Integración modular y flexible con distintos modelos locales.
- **🗣️ Ollama** – Plataforma para ejecutar modelos LLM de manera local.
- **🧠 Mistral 7B** – Modelo rápido, liviano y efectivo para tareas conversacionales.
- **🐍 Python 3.10+** – Lenguaje base para scripting y desarrollo del agente.
- **JSON** – Para almacenamiento persistente del historial o configuraciones.

---

## 📁 Estructura del repositorio

```bash
📦 agentes-ia/
├── 1-Agente/           → Asistente simple
├── 2-Agente/           → Agente conversacional con memoria
├── 3-Agente/           → Asistente conversacional con personalidad peruana, memoria y comandos 
├── README.md           → Este archivo
```

> 🔧 Cada carpeta contiene su propio archivo `.py`, sus prompts, lógica y módulos necesarios.

---

## 🛠️ Instalación y ejecución

### 1. Instala dependencias de Python

```bash
pip install langchain langchain-core langchain-community langchain-ollama
```

### 2. Asegúrate de tener Ollama y el modelo descargado

```bash
ollama run mistral
```

> Puedes reemplazar `mistral` por otro modelo compatible (`llama2`, `gemma`, etc.)

### 3. Ejecuta el agente que desees

```bash
cd AgentesPy
cd 1-Agente
python 1-Agente.py
```

---

## 🧪 Próximas mejoras (roadmap)

- [ ] Interfaz gráfica (Streamlit / Gradio)
- [ ] Memoria a largo plazo y recordatorios
- [ ] Integración con APIs externas
- [ ] Agentes colaborativos entre sí

---

## 👨‍💻 Autor

Este proyecto está siendo desarrollado por [Matías Palomino Luna](https://github.com/jmatias2411) como exploración práctica de agentes IA locales y personalizables.

---

## 📄 Licencia

Este repositorio se distribuye bajo la licencia MIT. Puedes usarlo, modificarlo o expandirlo libremente.
