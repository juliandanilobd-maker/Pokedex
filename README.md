# Pokédex App

Sistema modular backend construido con **FastAPI**, diseñado para consumir la PokeAPI,
procesar datos de Pokémon y exponerlos mediante una API REST escalable, accesible
desde una interfaz web en Streamlit o desde un CLI interactivo con soporte argparse.

---

## Vistas

![VISTA PRINCIPAL](/docs/images/image.png)
![BUSQUEDA POR FILTROS](/docs/images/image-1.png)
![BUSQUEDA INDIVIDUAL — RECOMENDACIÓN DEL DÍA](/docs/images/image-2.png)
![BUSQUEDA INDIVIDUAL](/docs/images/image-3.png)
![CADENA EVOLUTIVA](/docs/images/image-4.png)
![CARTA COLECCIONABLE](/docs/images/image-5.png)

---

## Descripción

**Pokédex App v1.0.0** es un MVP funcional que entrega:

- Búsqueda individual de Pokémon con detalle completo, cadena evolutiva y carta coleccionable
- Búsqueda por filtros acumulativos (tipo, generación, stats mínimas)
- Motor de efectividad de combate basado en multiplicadores de tipo
- Constructor de equipos Pokémon con estadísticas agregadas y cobertura de tipos
- Motor analítico: promedios por tipo, rankings Top-N y detección de anomalías estadísticas
- Predicción de stats por tipo elemental mediante media móvil simple (SMA)
- Generación de Pokémon sintéticos basada en distribuciones estadísticas del dataset real
- Exportación de resultados a CSV
- Gráficos ASCII de stats en consola
- Alertas automáticas al iniciar el CLI
---

## Inicio rápido

```bash
# 1. Clonar y entrar al proyecto
git clone https://github.com/juliandanilobd-maker/Pokedex.git
cd Pokedex

# 2. Crear y activar entorno virtual
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Linux/macOS

# 3. Instalar dependencias
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

# 4. Generar dataset local (solo la primera vez)
python -m backend.app.data.scripts.dataset_generator

# 5. Levantar el backend
uvicorn backend.main:app --reload --port 8000

# 6a. Interfaz web (segunda terminal)
streamlit run frontend/streamlit_folder/Pokedex.py

# 6b. CLI interactivo (segunda o tercera terminal)
python cli.py
```

Para instrucciones detalladas consulta el [Manual de Instalación](/docs/documentacion_usuario/manual_instalacion.md).

---

## Estructura del proyecto

```text
Pokedex/
│
├── backend/
│   ├── app/
│   │   ├── api/            # Rutas FastAPI (routes.py)
│   │   ├── cache/          # Caché SQLite (cache_manager.py)
│   │   ├── clients/        # Cliente HTTP httpx (pokeapi_client.py)
│   │   ├── core/           # Configuración y constantes
│   │   ├── data/           # Dataset local JSON y script ETL
│   │   ├── dependencies/   # Inyección de dependencias FastAPI
│   │   ├── models/         # Modelos Pydantic
│   │   ├── parsers/        # Transformación de datos de la PokeAPI
│   │   └── services/       # Lógica de negocio por dominio
│   ├── tests/
│   │   ├── unitary/        # Tests unitarios por módulo
│   │   ├── integration/    # Tests de integración de endpoints
│   │   └── functional/     # Tests E2E contra la PokeAPI real
│   ├── main.py
│   ├── requirements.txt
│   └── requirements-dev.txt
│
├── frontend/
│   └── streamlit_folder/
│       └── Pokedex.py      # Aplicación Streamlit
│
├── data/
│   ├── reports/            # CSVs exportados
│   └── pokemon_sinteticos.csv
│
├── docs/
│   └── images/             # Capturas para documentación
│
├── cli.py                  # CLI interactivo + comandos argparse
├── client_cli.py           # Cliente HTTP para el CLI
└── INSTALL.md
```

---

## Flujo del sistema

### Búsqueda desde la API (Streamlit o CLI)

```
Usuario
  └─→ Streamlit / CLI
        └─→ FastAPI Router
              └─→ Servicio de dominio
                    ├─→ Caché SQLite  ──→ (hit) Respuesta inmediata
                    └─→ (miss) PokeAPIClient (httpx)
                                └─→ PokeAPI externa
                                      └─→ Parser → Modelo Pydantic → Respuesta
```

### Búsqueda con filtros y analytics (dataset local)

```
Usuario
  └─→ Streamlit / CLI
        └─→ FastAPI Router
              └─→ Servicio de dominio
                    └─→ Dataset local JSON
                          └─→ Filtrado / Cálculo estadístico → Respuesta
```

---

## Funcionalidades implementadas (v1.0.0)

### Backend
- API REST con FastAPI y validación automática con Pydantic
- Cliente HTTP asíncrono con `httpx` y pool de conexiones
- Caché automática con SQLite y TTL configurable
- Rate limiting para proteger la IP frente a la PokeAPI
- Motor de efectividad de combate con multiplicadores duales (×4, ×2, ×0.5, ×0.25, ×0)
- Motor analítico: promedios por tipo, Top-N, detección de anomalías por desviación estándar y percentil
- Predicción de stats con media móvil simple (SMA, ventana máxima 3)
- Generador de Pokémon sintéticos con distribución normal por tipo
- CRUD de equipos persistido en JSON
- Arquitectura modular por capas con inyección de dependencias
### Frontend
- Interfaz web con Streamlit
- Galería de Pokémon con filtros en tiempo real
- Vista de detalle con gráfico de radar, cadena evolutiva y carta coleccionable
- Pokémon del día determinista (cambia cada 24h)
### CLI
- Menú interactivo con 17 módulos de auditoría
- Modo directo con argparse (todos los endpoints accesibles por comando)
- Submenú de navegación para listas largas (ver más, ver todos, buscar por nombre)
- Alertas automáticas al iniciar (anomalías, equipos débiles, Pokémon del día)
- Exportación a CSV y gráficos ASCII desde consola
### Calidad
- Suite de tests con pytest: unitarios, integración y E2E funcionales
- Cobertura superior al 90% del backend
- CI con GitHub Actions: linting con Ruff y cobertura automática en cada push
---

## Tecnologías

| Categoría | Tecnología |
|---|---|
| Lenguaje | Python 3.11 |
| Backend | FastAPI + Uvicorn |
| Frontend | Streamlit |
| Cliente HTTP | httpx (AsyncClient) |
| Persistencia | SQLite (caché) + JSON (equipos, dataset) |
| Análisis de datos | pandas, numpy |
| Tests | pytest, pytest-cov, pytest-asyncio |
| Calidad de código | Ruff (linting + formatting) |
| CI/CD | GitHub Actions |

---

## Limitaciones de esta versión

- El frontend cubre los flujos principales de búsqueda; las páginas de analytics
  (promedios, anomalías, predicción, simulación) están disponibles únicamente en el CLI.
- No incluye tests automatizados de UI (Playwright/Selenium). Las pruebas de frontend
  en el pipeline CI se limitan a validación de calidad de código con Ruff.
- El dataset local debe generarse manualmente con el script ETL antes del primer uso.
- La predicción requiere al menos 2 generaciones de datos para el tipo consultado.
---

## Contribuciones

¡Las contribuciones son bienvenidas! Para cambios importantes, abre un Issue primero
para discutir lo que deseas modificar. Para correcciones menores, un Pull Request
directo es suficiente.

---

## Licencia

MIT