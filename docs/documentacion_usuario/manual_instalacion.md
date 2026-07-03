# MANUAL DE INSTALACIÓN

## Requisitos previos

- Python 3.11 o superior
- Git
- Conexión a internet (para descargar datos de la PokeAPI en el primer arranque)
---

## 1. Clona el repositorio

```bash
git clone https://github.com/juliandanilobd-maker/Pokedex.git
cd Pokedex
```

---

## 2. Crea y activa el entorno virtual

```bash
# Crear el entorno
python -m venv .venv

# Activar en Windows
.venv\Scripts\activate

# Activar en Linux / macOS
source .venv/bin/activate
```

> Sabrás que está activo cuando veas `(.venv)` al inicio de tu línea de comandos.

---

## 3. Instala las dependencias

### Backend

```bash
cd backend
pip install -r requirements.txt
cd ..
```

### Frontend

```bash
cd frontend
pip install -r requirements.txt
cd ..
```

### Dependencias de desarrollo (solo si vas a ejecutar los tests)

```bash
pip install -r backend/requirements-dev.txt
```

---

## 4. Genera el dataset local

Los módulos de filtros, analytics, predicción y simulación trabajan sobre un dataset local. Es obligatorio generarlo antes del primer uso:

```bash
python -m backend.app.data.scripts.dataset_generator
```

Este proceso descarga datos de la PokeAPI y puede tardar varios minutos. Al finalizar verás un mensaje de confirmación con el número de Pokémon guardados.

> Este paso solo es necesario la primera vez, o cuando quieras actualizar el dataset con nuevos Pokémon.

---

## 5. Levanta el servidor backend

Desde la raíz del proyecto, en una terminal:

```bash
uvicorn backend.main:app --reload --port 8000
```

Espera hasta ver:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Mantén esta terminal abierta durante toda la sesión.

---

## 6. Interfaz web (Streamlit)

En una **segunda terminal**, con el entorno virtual activado:

```bash
streamlit run frontend/streamlit_folder/Pokedex.py
```

El navegador se abrirá automáticamente en `http://localhost:8501`.

---

## 7. Interfaz CLI

En una **segunda terminal** (o tercera si Streamlit ya está corriendo), con el entorno virtual activado:

```bash
# Modo interactivo con menú
python cli.py

# Modo directo con comandos (ejemplos)
python cli.py pokemon pikachu
python cli.py analytics top --metric attack --n 5
python cli.py --help
```

---

## 8. Ejecutar los tests (desarrolladores)

Asegúrate de haber instalado las dependencias de desarrollo (paso 3).
Desde la raíz del proyecto:

```bash
# Suite completa con cobertura
pytest --cov=backend/app --cov-fail-under=90

# Solo tests unitarios
pytest backend/tests/unitary/

# Solo tests de integración
pytest backend/tests/integration/

# Solo tests funcionales E2E (requiere backend activo)
pytest backend/tests/functional/
```

---

## Resumen de terminales necesarias

| Terminal | Comando | Propósito |
|---|---|---|
| 1 | `uvicorn backend.main:app --reload` | Servidor backend (obligatorio) |
| 2 | `streamlit run frontend/streamlit_folder/Pokedex.py` | Interfaz web (opcional) |
| 2 ó 3 | `python cli.py` | Interfaz CLI (opcional) |

---

## Solución de problemas comunes

**`ModuleNotFoundError: No module named 'backend'`**
Asegúrate de ejecutar los comandos desde la raíz del proyecto (`Pokedex/`),
no desde una subcarpeta.

**`ConnectionRefusedError` al usar el CLI**
El servidor backend no está activo. Ejecuta el paso 5 primero.

**Analytics devuelve listas vacías**
El dataset no fue generado. Ejecuta el paso 4.

**`uvicorn: command not found`**
El entorno virtual no está activado. Ejecuta el paso 2 de activación.