# Changelog

Todas las modificaciones relevantes del proyecto serán registradas aquí.

## [0.1.0] - Backend Core

### Funcionalidades añadidas
- FastAPI
- SQLite Cache
- PokeAPI Client
- Parsers
- Models
- Tests Unitarios

## [0.1.0-alpha] - FastAPI Core

### Funcionalidades añadidas
- Inicialización de FastAPI
- Configuración de base de CORS.
- Registro centralizado de routers.
- Endpoint GET /health.
- Archivo core/config.py.
- Primer test automatizado para health endpoint.

### Arreglado
- Uso de httpx2.
- Uso de ConfigDict en Pydantic.
- Uso de lifespan en lugar de on_event.

### CI
- Integración inicial con Github Actions.
- Verificación automática con Ruff

## [0.1.0-beta] - PokeAPI Client

### Funcionalidades añadidas
- Cliente HTTP único.
- Constructor de URL's.
- Manejo de requests GET.
- Manejo de Timeout y errores básico.
- Manejo de 404, 5xx.

### Arreglado
- .yml modificado para ejecutar job en push a develop y main.
- config.py modificado agregando Base url y constante timeout.
- BASE_URL modificado declarandose como constante de clase, utilizando, ClassVar de typing.
- MockResponse construido con mismos atributos de la clase PokeAPI Client.

### CI
- Integración con Github Actions, test unitario para pokeapi_client.
- Verificacion con Ruffs.

## [0.1.0-gamma] - Models & Parsers

### Funcionalidades añadidas
- Models estándar unificados para la app.
- Parsers para pokemon, tipos y evoluciones.

### Arreglado
- Parsers obtiene children y datos de los diferentes nodos de evolución.

### CI
- Tests para parsers.
- Verificación y linteado con Ruff.

## [0.1.0-delta] - Services Layer

### Funcionalidades añadidas
- Pokemon Service obtiene los datos básicos de un Pokemon.
- Evolution Service obtiene los datos de las diferentes evoluciones de un Pokemon.
- Rutas añadidas.

### Arreglado
- Endpoint Health arreglado y añadido a routes.py.

### CI
- Tests para services.
- Verificación y linteado con Ruff.