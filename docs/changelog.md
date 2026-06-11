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

## [0.1.0-epsilon] - Cache System

### Funcionalidades añadidas
- Sistema de cache en SQLite.
- Peticiones se buscan primero en cache.
- Se guardan datos en cache.
- Cache expira.

### Arreglado
- Configuraciones globales para cache añadidas.
- Servicio de dependencias modificado, para incluir cache.
- pokeapi_client modificado para trabajar con cache.
- conftest.py creado para instancia una pokeapi_client que llama a la PokeAPI Client, pero que trabaje con un mock cache.
- pokeapi_client_test modificado para trabajar el pokeapi_client de conftest.py.

### CI
- Test para cache y expiración de datos.
- Verificación y linteado con Ruff.

## [0.1.0-dseta] - Backend Testing & Refactored

### Funcionalidades añadidas
- Dependency Injection real.
- Tests de integración y funcional.
- Descripción del codigo con almohadillas.

### Arreglado
#### Inyección de dependencias:
- Refactorizamos el archivo dependencias y rutas para implementar Dependency Injection.
#### Seguridad CORS:
- Implementamos configuración CORS para restringir los metodos HTTP, y permitir solo los necesarios.
#### Ampliación de cobertura de tests:
- Modificamos el test health, a un test server, para validar el enrutamiento, CORS y el levantamiento correcto del servidor.
- Aislamiento de Test Cache, modificamos el test cache para reemplazar el uso del archivo SQLite por una base de datos temporal en memoria local.
- Mejoramos los tests de Pokemon Service usando un Mock Client para simular diferentes respuestas en segundos, y para comprobar su comportamiento frente a errores o datos corruptos.
- Mejoramos el Evolution Service, para comprobar manejo de errores o respuestas corruptas, y permitir escalar los tests.
- Se amplió la cobertura del test evolution para determinar el comportamiento ante distintas ramas.
- Se amplian los tests de Pokemon Parser para testear los diferentes lenguajes permitidos.
#### Modificación de archivos base:
- Modificamos el Evolution Node en models para incluir visibilidad para mejorar la interacción en la interfaz.
- Se mejoro tanto el models como el Evolution Service, para convertir los details en listas, con la finalidad de obtener los diferentes requisitos de evolución, y aumentando la obtención de location y min_affection.
- Se ajustó el Pokemon Parser para prevenir fallos cuando llegan datos vacíos.
#### Cambios extra
- Completar explicación de codigo mediante almohadillas.

### CI
- Pruebas funcionales E2E end to end.
- Pruebas de integracion con DI/Overrides.
- Reporte de cobertura automatizado integrado.

## [0.2.0] - Search Filters
### Funcionalidades añadidas
- Script ETL generador de un dataset local.
- Dataset local.
- Sistema de filtros.
- Tests unitarios, funcionales y de integración

## [0.2.0-alpha] - Dataset generator
### Funcionalidades añadidas
- Script que genera un dataset Pokemon con info resumida.
- Dataset local.

### CI
- Tests unitarios automatizados.

## [0.2.0-beta] - Filter Service
### Funcionalidades añadidas
- Servicio de busqueda por filtros.
- Filtrado por varias estadisticas, tipos y generaciones.
- Combinacion de filtros

### Arreglado
- Subido de caches locales .db a repositorio remoto.
- Actualizacion de gitignore para ignorar .db.

### CI
- Tests unitarios de filter service.
- Verificación y linteado con Ruff.

## [0.2.0-gamma] - Filter Endpoint
### Funcionalidades añadidas
- Filter Service añadido a rutas.

### Arreglado
- Actualización de gitignore para ignorar .json.
- Eliminación de dataset.json subido a repositorios.

## [0.2.0-delta] - CI Testing
### Funcionalidades añadidas
- Automatización del reporte de cobertura de código en el pipeline.
- Umbral de cobertura mínima para bloquear pull requests si disminuye la cobertura de los tests.

### Arreglado
- Aislamiento del Entorno en Windows: corrección del fallo de borrado de bases de datos SQLite, y archivos .pyc temporales en scripts.
- Mocks de sistemas de archivos: refactorizamos pruebas unitarias usando parches pathlib para evitar atributos read-only durante la carga del Dataset.
- Eliminación del código muerto: Corrección del flujo en fetch_with_retry.
- Ajustes de Fixtures Numericos: sincronizamos los assertes de filtrado por estadisticas con valores inyectados con mocks.

### CI
- Pipeline optimizado para ejecutar borrado y purga de los caches previo a tests.
- Bloqueo automatizado del pipeline de GitHub Actions si la cobertura desciende de 90%
- Verificación y linteado con Ruff.

## [0.3.0] - Battle System
### Funcionalidades añadidas
- Motor analítico de efectividad de tipos para el cálculo estrategico de combate.
- Endpoint especializado de efectividad elemental.
- Cobertura de pruebas unitarias, funcionales e integración.

## [0.3.0-alpha] - Type Relations Service
### Funcionalidades añadidas
- Aplicación del type service incorporando el metodo get_damage_relations.
- Consumo e interpretación de los nodos de daño de la PokeAPI.
- Sistema de mapeo y tipado para las matrices de daño por tipo individual.
### CI
- Pruebas unitarias para la extracción de relaciones por tipo.
- Casos de prueba específicos.
- Verificación y linteado con Ruff.

## [0.3.0-beta] - Battle Intelligence Engine
### Funcionalidades añadidas
- Battle Service como núcleo de inteligencia táctica del backend.
- Lógica aritmetica para calcular debilidades, resistencias e inmunidades combinadas, tomando en cuenta los tipos únicos y duales.
- Esquema unificado de salida "debilidades", "resistencias", "inmunidades".

### CI
- Pruebas unitarias para los cálculos aritmeticos y el motor de inteligencia.
- Verificación y linteado con Ruff.

## [0.3.0-gamma] - Battle Endpoint
### Funcionalidades añadidas
- Crear endpoint GET "/pokemon/{identifier}/effectiveness"
- Inyección de dependencias en BattleService.
- Manejo de errores 404 Not Found.

### Arreglado
- Pokemon models modificado.
- Dependencias y rutas modificados para inyección de dependencias y manejo del endpoint BattleService.
### CI
- Verificación y linteado con Ruff.

## [0.3.0-delta] - Testing & refactor Battle Intelligence/routes/client/dependencies
### Funcionalidades añadidas
- Tests de integración.
- Tests funcionales e2e.
- Get type agregado a client.

### Arreglado
- Corrección para uso de Pydantic para atributos de PokemonEffectiveness
- Routes corregido para un mejor manejo de errores.
- Script ETL mejorado para mejorar extracción de información.
- Dataset tests modificados para utilizar un mock dataset.
- Models actualizado para modelar información de efectividad.
- Rutas refactorizado para manejo de errores y uso de models.

### CI
- Tests funcionales e2e y de integración para el endpoint Battle Service.
- Verificación y linteado con Ruff.