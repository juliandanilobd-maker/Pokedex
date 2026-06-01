# Pokedex App

## Descripcion

Pokedex App es un sistema modular backend construido con FastAPI, diseñado para consumir la PokeAPI, procesar datos de Pokemon y exponerlos mediante una API REST escalable.

Esta versión v0.1.0 se centra exclusivamente en la fundación para el backend, incluyendo arquitectura por capas, integración con API externa, sistema de cache y base de calidad mediante tests.

## Estado del proyecto

- Versión: 0.1.0 - Backend Core.
- Estado: Funcional.
- Enfoque: Arquitectura, API, integracón y cache.


## Estructura del proyecto

El proyecto está organizado una arquitectura modular por capas, diseñado para ser escalable y que permita separación de responsabilidades.

Pokedex/
│
├── backend/
│   └── app/
│       ├── api/
│       ├── services/
│       ├── clients/
│       ├── cache/
│       ├── models/
│       ├── parsers/
│       ├── core/
│       ├── dependencies/
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

## Funciones implementadas (v0.1.0)

### Arquitectura
- Modular por capas.
- Separación de responsabilidades.
- Sistema preparado para escalar.

### Backend
- FastAPI funcional.
- Endpoint health/.
- Estructura de routers lista para expansión.

### Integración externa
- Cliente HTTP para PokeAPI.
- Manejo de errores de API externa.
- Normalización de datos.

### Cache
- Cache persistente con SQLite.
- Estrategia Cache First.
- Reducción de llamadas a API externa.

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



