# Pokedex App

## Descripcion

Pokedex App es un sistema modular backend construido con FastAPI, diseñado para consumir la PokeAPI, procesar datos de Pokemon y exponerlos mediante una API REST escalable.

Esta versión v0.4.0 se centra exclusivamente en implementar un frontend que permita al usuario interactuar con la Pokedex, de forma simple y entretenida.

## Estado del proyecto

- Versión: 0.4.0 - Frontend MVP.
- Estado: Funcional con frontend interactuable.
- Enfoque: Creación de una interfaz gráfico de usuario, desacoplada, sencilla y entretenida para el usuario.


## Estructura del proyecto

El proyecto está organizado una arquitectura modular por capas, diseñado para ser escalable y que permita separación de responsabilidades.

```text
Pokedex/
│
├── backend/
├── frontend/
│       └── streamlit_folder/
│                       ├── api/: Cliente HTTP que consume los endpoints del backend.
│                       ├── components/: Componentes visuales (Cards, badges)
│                       ├── pages/: Diseño de paginas secundarias de navegación.
│                       ├── utils/: Constantes de diseño, paletas de colores y estilos CSS.
│                       ├── views/: Orquestación y maquetación de las páginas principales.
│                       └── Pokedex.py: Punto de entrada principal a la aplicación.
├── tests/
└── docs/
```
## Responsabilidad de capas
- backend/: Servidor FastAPI. Contiene las reglas de negocio, el motor analítico de efectividad, parsers de modelos Pydantic y el cliente de persistencia en caché.
- frontend/: Servidor en Streamlit. Se encarga de capturar las interacciones del usuario, renderizar componentes visuales y consumir los datos procesados por el backend.

## Flujo del sistema

Request del cliente --> Streamlit (Frontend) --> FastAPI router (Backend) --> Capa de Servicios --> Caché SQLite --> PokeAPI Client (si no hay cache) --> Parser --> Modelos Pydantic --> Respuesta

### Flujo de búsqueda local con filtros
Request Filtros --> Streamlit (Frontend) --> FastAPI router (Backend) --> Capa de Servicios --> Dataset Local --> Respuesta normalizada

## Funciones implementadas (v0.3.0)

### Arquitectura
- Modular por capas.
- Separación de responsabilidades.
- Sistema preparado para escalar.

### Backend
- Lógica de negocio interna.
- Persistencia de datos.
- Resiliencia de red.

### Frontend
- Diseño y estructura de interfaz de usuario.
- Renderizado de componentes visuales.
- Consumo del backend.

### Calidad
- Tests unitarios con pytest.
- CI básico con GitHub Actions.
- Validación automática en push.
- Cobertura del mayor del 90%.

## Tecnologías
- Lenguaje de programación: Python 3.11
- Framework backend: FastAPI & Uvicorn
- Framework Frontend: Streamlit
- Persistencia de datos: SQLite & JSON estructurado
- Herramientas de calidad: Ruff (Linteado & Formateado) y Pytest (Suite de pruebas y cobertura)
- Clientes de Red: Requests & HTTPAdapter/urlib3

## Limitaciones de esta versón
El frontend en esta fase se encuentra en MVP (Mínimo Producto Viable), la interfaz inicial cubre los flujos iniciales de búsqueda (Detalles de un Pokemon, filtros de búsqueda, evoluciones Pokemon, effectividad en combate), renderizado de tarjetas básicas y paneles de información.

Esta versión no incluye pruebas automatizadas para el frontend (UI Testing o E2E con Playwright/Selenium); las pruebas en el pipeline de CI se limitan a la validación de calidad de código con Ruff para el frontend y cobertura mayor al 90% del backend.

## Contribuciones
¡Me encantaría tu ayuda para mejorar la Pokedex! Cualquier Pull Request es bienvenida. Para cambios importantes abre un Issue primero, para discutir lo que deseas modificar.
