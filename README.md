# Pokedex App

## Descripcion

Pokedex App es un sistema modular backend construido con FastAPI, diseñado para consumir la PokeAPI, procesar datos de Pokemon y exponerlos mediante una API REST escalable.

Esta versión v0.3.0 se centra exclusivamente en implementar un sistema inteligente de calculo de daños de acuerdo a los tipos Pokemon.

## Estado del proyecto

- Versión: 0.3.0 - Battle Inteligence.
- Estado: Funcional con motor de análisis de efectividad elemental y lógica de daño.
- Enfoque: Extracción de matrices de daño, cálculo de efectividad en tipos duales.


## Estructura del proyecto

El proyecto está organizado una arquitectura modular por capas, diseñado para ser escalable y que permita separación de responsabilidades.

Pokedex/
│
├── backend/
│   └── app/
│       ├── api/
│       ├── services/
│       │       ├──PokemonService
│       │       ├──EvolutionService 
│       │       ├──FilterService 
│       │       └──BattleService # Nueva capa lógica para v0.3.0
│       ├── data/
│       │       ├──scripts/ dataset_generator # Script ETL
│       │       └──pokemon_dataset # Dataset local  
│       ├── clients/
│       │       └──PokeAPIClient
│       ├── cache/
│       │       └──CacheManager
│       ├── models/
│       │       └──PokemonModels # Estructuras Pydantic de datos y efectividad
│       ├── parsers/
│       │       └──Pokemon/Evolution/TypeParser
│       ├── core/
│       │       └──config
│       ├── dependencies/
│       │       └──dependencias
│       └── utils/
│
├── tests/
└── docs/

## Responsabilidad de capas
- api/: Endpoints REST.
- services/: Lógica de negocio.
- clients/: Comunicación con PokeAPI.
- cache/: Sistema de almacenamiento local (SQLite).
- models/: Modelos internos del sistema.
- parsers/: Transformación de datos externos.
- core/: Configuración base del sistema.
- dependencies/: Inyección de dependencias.
- utils/: Utilidades generales.

## Flujo del sistema

Request del cliente --> FastAPI router --> Capa de Servicios --> Capa de cache --> PokeAPI Client (si no hay cache) --> Parser pasa a Modelos internos --> Respuesta

### Flujo de bósqueda local (v0.2.0)
Request Filtros --> FastAPI router --> Capa de servicios --> Dataset Local --> Respuesta normalizada

## Funciones implementadas (v0.3.0)

### Arquitectura
- Modular por capas.
- Separación de responsabilidades.
- Sistema preparado para escalar.

### Backend
- Motor analítico de efectividad.
- Nuevo endpoint.
- Algoritmo de resolución matemática para efectividad.

### Integración externa
- Amplicación de servicios.
- Manejo de errores controlado.

### Cache
- Persistencia con SQLite para datos crudos de PokeAPI.
- Para el sistema de filtros, el cache se configura el dataset local.

### Calidad
- Tests unitarios con pytest.
- CI básico con GitHub Actions.
- Validación automática en push.

## Tecnologías
- Python 3.11
- FastAPI
- Uvicorn
- SQLite
- Pytest
- Requests
- PokeAPI
- Ruff

## Limitaciones de esta versón
Esta versión no incluye el frontend, ya que el enfoque es exclusivamente backend core.

El frontend Streamlit, será incorporado en futuras versiones (≥ v0.4.0)

## Contibuciones
Me encantaría tu ayuda para mejorar el código, cualquier pull es bienvenido, para cambios importantes abre un issue por favor.



