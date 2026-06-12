# Backlog

## Prioridades usadas para el backlog:

- Alta: Fundamental para el funcionamiento de la app.
- Media: Mejora importante de la app.
- Futuro: Funcionalidades para futuras fases.

## Estados de las actividades en el backlog:

- Completado: Actividad terminada.
- En curso: Se encuentra en desarrollo.
- Pendiente: En espera, falta desarrollar.
- Futuro: Proximas funcionalidades, a largo plazo.

### DOD (Definition of Done): Definición de completado:
Una actividad se considera completada cuando:
- El código funciona correctamente.
- Cumple criterios de aceptación.
- No se generan errores.
- Se integra con la nueva arquitectura.
- Se prueba manualmente.
- Mantiene el estilo modular por capas del proyecto.
---
# Release v0.1.0

# Epica 1 - Arquitectura Base

## Objetivo
Construir una base de arquitectura que divida responsabilidades frontend/backend y la arquitectura basica modular por capas.

## Historia 1.1 - Crear una arquitectura modular por capas para el backend y frontend

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Como estudiante de primer año, busco una arquitectura modular por capas para que el proyecto pueda ser desarrollado de forma ordenada, que tenga posibilidad de escalar y que se pueda mantener.

### Criterios de aceptación
- [x] Crear carpeta backend/app.
- [x] Crear modulos:
    - api.
    - cache.
    - clients.
    - core.
    - data.
    - dependencies.
    - models.
    - parsers.
    - services.
    - utils.

## Historia 1.2 - Configurar FastAPI

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Como desarrollador necesito un backend FastAPI funcional para nuestros endpoints REST.

### Criterios de aceptación
- [x] main.py inicializa FastAPI.
- [x] Se ha creado el endpoint /health.
- [x] Routers registrados correctamente.
- [x] Uvicorn levanta el servidor.

## Historia 1.3 - Configurar sistema de dependencias

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Como desarrollador, necesito un sistema de dependencias para desacoplar servicios y facilitar testing

### Criterios de aceptación
- [x] Uso de dependency injection en FastAPI.
- [x] Servicios inyectables (no instanciados globalmente).
- [x] Separacion clara entre clientes, servicios y endpoints.
- [x] Preparado para mocking test.

---
# Epica 2 - Integración PokeAPI

## Objetivo
Permitir comunicación estable y estructurada con la API externa de Pokemon.

## Historia 2.1 - Crear cliente HTTP

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Como sistema, necesito un cliente HTTP que permita consumir PokeAPI de forma centralizada.

### Criterios de aceptación
- [x] Cliente HTTP único para PokeAPI.
- [x] Manejo de requests GET.
- [x] Timeout y control básico de errores.
- [x] No existe acceso directo a requests fuera del cliente.

## Historia 2.2 - Servicios
### Prioridad: ALTA.
### Estado: COMPLETADO.
#### Descripción
Como sistema, necesito una capa de servicio lógica que procese la info obtenida desde la PokeAPI por client, y que envíe los datos a ser parseados

### Criterios de aceptación
- [x] Crear Pokemon Service.
- [x] Crear Evolution Service.
- [x] Crear los endpoints 'pokemon/{identifier}' y 'pokemon/{identifier}/evolution'.
- [x] Mapear los parámetros de consulta de FastAPI hacia los argumentos de los Pokemon y Evolution Service.
- [x] Solo los servicios se conectan directamente con el client.
- [x] Servicios sirven de puente entre client y parsers.
- [x] Servicios devuelven datos parseados y modelados.

## Historia 2.3 - Normalizar identificadores

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción

Como sistema, necesito transformar datos crudos de PokeAPI en modelos internos consistentes.

### Criterios de aceptación
- [x] Parsers implementados para cada Pokemon.
- [x] Datos externos convertidos a modelos internos.
- [x] Campos relevantes normalizados.
- [x] Evitar exposicón directa del JSON externo.


## Historia 2.4 - Manejo de errores

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción

Como sistema, necesito manejar errores de red o API externa para evitar fallos en cascada.

### Criterios de aceptación
- [x] Manejo de Timeouts, 404 y errores 5xx.
- [x] Respuestas controladas al backend.
- [x] No se rompe el backend por fallos de PokeAPI.

---

# Epica 3 - Cache


## Objetivo
Reducir las llamadas a PokeAPI mediante almacenamiento local eficiente.

## Historia 3.1 - Implementar SQLite

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción

Como sistema, necesito implementar un cache persistente, para reducir las llamadas repetidas a la PokeAPI.

### Criterios de aceptación
- [x] SQLite configurado como almacenamiento.
- [x] Guardado de respuestas de API.
- [x] Recuperación de datos cacheados.
- [x] Persistencia de ejecuciones.

## Historia 3.2 - Integrar cache-first

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción

Como sistema necesito priorizar datos en cache antes de consultar la API externa.

### Criterios de aceptación
- [x] Primero se consulta a cache.
- [x] Si no existe cache se consulta a PokeAPI.
- [x] Se guarda info consultada a PokeAPI en cache.
- [x] Lógica centralizada en capa de cache service.

---

# Epica 4 - Calidad del Software

## Objetivo

Garantizar la estabilidad del backend mediante tests y CI.

## Historia 4.1 - Crear tests

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción

Como desarrollador, necesito tests unitarios para asegurar el correcto funcionamiento del backend.

### Criterios de aceptación

- [x] Tests unitarios para servicios.
- [x] Tests unitarios para cliente.
- [x] Tests unitarios para cache.
- [x] Tests unitarios para parsers.
- [x] Tests de integración y funcionales E2E.
- [x] ≥90% de cobertura.
- [x] Uso de pytest.
- [x] Tests independientes del entorno real.

## Historia 4.2 - Configurar CI con Github Actions

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción

Como desarrollador, necesito automatizar la ejecución de tests en cada push

### Criterios de aceptación
- [x] Worflow en Github actions.
- [x] Ejecución automática de tests.
- [x] Fail si tests no pasan.
- [x] Integración con rama develop y main.

---
# Release v0.2.0
# Epica 5 - Motor de búsqueda y filtrado local

## Objetivo
Permitir la consulta, filtrado por estadisticas y generaciones de manera local, reduciendo los tiempos de espera por peticiones, la latencia y eliminando la dependencia de la API para consultas masivas de filtros.

## Historia 5.1 - Desarrollar Script ETL y Dataset Local
### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Como sistema, es más sencillo extraer una gran cantidad de datos de manera local. Como desarrollador, necesito un script ETL automatizado que permita extraer los datos de la PokeAPI, limpiarlos, resumirlos, y guardarlos en formato JSON de manera local.

### Criterios de aceptación
- [x] Crear el script ETL en 'backend/app/data/scripts/dataset_generator.py'.
- [x] Extracción de la info esencial para los filtros de busqueda.
- [x] Guardar el dataset en 'backend/app/data/pokemon_dataset.json'

## Historia 5.2 - Servicio de filtros
### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Como sistema, necesito una capa de servicio lógica que procese el dataset JSON local.

### Criterios de aceptación
- [x] Crear el Filter Service.
- [x] Implementar filtrado por tipo, generación, base_exp, hp, attack, defense, speed.
- [x] Combinar varios filtros en una misma busqueda.

## Historia 5.3 - Exponer Endpoint de filtrado
### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Como sistema, necesito un endpoint accesible mediante parámetros de consulta para brindar el servicio de filtro de busqueda por filtros.

### Criterios de aceptación
- [x] Crear el endpoint '/filter'.
- [x] Mapear los parametros de consulta hacia los argumentos de Filter Service.

---
# Epica 6 - Calidad del Software

## Objetivo

Garantizar la estabilidad del servicio de filtros mediante tests y CI.

## Historia 6.1 - Crear tests

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción

Como desarrollador, necesito tests unitarios para asegurar el correcto funcionamiento del servicio.

### Criterios de aceptación

- [x] Tests unitarios para el script ETL y el dataset local.
- [x] Tests unitarios para los diferentes filtros.
- [x] Tests unitarios para asegurar el endpoint filter.
- [x] Tests de integración y funcionales E2E, que verifiquen llamadas reales.
- [x] ≥90% de cobertura.
- [x] Uso de pytest.
- [x] Tests independientes del entorno real.

## Historia 6.2 - Configurar CI con Github Actions

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción

Como desarrollador, necesito automatizar la ejecución de tests en cada push

### Criterios de aceptación
- [x] Worflow en Github actions.
- [x] Ejecución automática de tests.
- [x] Fail si tests no pasan.
- [x] Integración con rama develop y main.

---
# Release v0.3.0

# Epica 7 - Motor de Inteligencia de Batalla
## Objetivo
Agregar análisis estrategico de combate al backend, permitiendo interpretar las debilidades, resistencias e inmunidades elementales de los Pokemon de manera dinámica.

## Historia 7.1 - Ampliar Type Service con matrices de daño
### Prioridad: ALTA.
### Estado: COMPLETADO.
#### Descripción
Como sistema, necesito extraer y procesar las relaciones de daño directo de cada tipo elemental desde la PokeAPI, para servir de base al motor de combate.
### Criterios de aceptación
- [x] Implementar la función "get_damage_relations".
- [x] Consumir los nodos de daño de la PokeAPI.
- [x] Mapear y normalizar las respuestas a modelos internos.
- [x] Manejo de errores.

## Historia 7.2 - Desarrollar el algoritmo de efectividad combinada
### Prioridad: ALTA.
### Estado: COMPLETADO.
#### Descripción
Como usuario, necesito que la Pokedex calcule y combina matematicamente las eficacias de daño para los diferentes tipos de Pokemon.
### Criterios de aceptación
- [x] Crear el servicio "BattleService".
- [x] Implementar el algoritmo multiplicador para combinar matrices de daño en Pokemons duales.
- [x] Resolver conflictos de efectividad.
- [x] Garantizar que las inmunidades absolutas anulen cualquier debilidad secundaria.
- [x] Estructurar las salidas en un formato unificado.

## Historia 7.3 - Exponer Endpoints del sistema de combate
### Prioridad: ALTA.
### Estado: COMPLETADO.
#### Descripción
Como desarrollador, para exponer al frontend los servicios, necesito un endpoint especializadoy aislado para consumir.

### Criterios de aceptación
- [x] Crear el endpoint GET "pokemon/{identifier}/effectiveness"
- [x] Implementar inyección de dependencias.
- [x] Validar los parametros de consultas.

---
# Epica 8 - Calidad del Software

## Objetivo

Garantizar la estabilidad del servicio de filtros mediante tests y CI.

## Historia 8.1 - Crear tests

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción

Como desarrollador, necesito tests unitarios para asegurar el correcto funcionamiento del servicio.

### Criterios de aceptación

- [x] Tests unitarios para extracción de matrices.
- [x] Tests unitarios para el motor analítico.
- [x] Tests de integración funcionales E2E para el endpoint.
- [x] ≥90% de cobertura.
- [x] Uso de pytest.
- [x] Tests independientes del entorno real.

## Historia 8.2 - Configurar CI con Github Actions

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción

Como desarrollador, necesito automatizar la ejecución de tests en cada push

### Criterios de aceptación
- [x] Worflow en Github actions.
- [x] Ejecución automática de tests.
- [x] Fail si tests no pasan.
- [x] Integración con rama develop y main.

---
# Release v0.4.0
# Epica 9 - Arquitectura base del Frontend

## Objetivo
Configurar el entorno base del servidor Streamlit y definir la lógica de inicialización globaal de la aplicación.

## Historia 9.1 - Inicialización del entorno y sistema de enrutamiento nativo

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Como desarrollador, necesito un punto de entrada centralizado y establecer los parámetros globales de la interfaz (layouts, títulos, íconos) para permitir que el sistema reconozca las paginas de navegación y un entorno visual consistente.

### Criterios de aceptación
- [x] Implementar configuración en el archivo raíz, definiendo títulos y modo ancho completo y el icono oficial.
- [x] Configurar el enrutamiento nativo multipágina de Streamlit.
- [x] Inyectar la lógica de inicialización del archivo principal.
- [x] Asegurar que al ejecutar el archivo principal, la barra de navegación reconozca las subpáginas sin romper las rutas de importación.

## Historia 9.2 - Maquetación básica de la vista home y almacenamiento de estado
### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Como usuario, me gustaría acceder a una página de inicio limpia, que establezca el marco principal de la aplicación y preserve las variables.

### Criterios de aceptación
- [x] Diseñar el layout estructural de la página de inicio.
- [x] Configurar el diccionario global para incializar y mantener la sesión del usuario durante la navegación.
- [x] Aegurar que la vista principal responda y renderice correctamente el sistema.

---
# Epica 10 - Cliente HTTP de Integración
## Objetivo
Centralizar e implementar el consumo de los endpoints del backend.

## Historia 10.1 - Desarrollar el API Client del Frontend
### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Como sistema frontend, necesito un cliente HTTP unificado para encapsular la comunicación con el backend y gestionar los errores o fallos.

### Criterios de aceptación
- [x] Crear el cliente base utilizando requests.
- [x] Implementar la función de control de salud, consumiendo el endpoint '/health' del backend.
- [x] Añadir comportamiento defensivo para manejo de errores.

---
# Epica 11 - Componentes Visuales
## Objetivo
Desarrollar componentes de interfaz de usuario desacoplados y reutilizables para modularizar la presentación visual de la información.

## Historia 11.1 - Componentes de cartas básicas y  emblemas elementales
### Prioridad: MEDIA.
### Estado: COMPLETADO.

#### Descripción
Como usuario, me gustaría visualizar resumenes, imagenes y diseños de los Pokemon, para identificar e interactuar con la información

### Criterios de aceptación
- [x] Crear el fichero que aloje el renderizado de un Pokemon.
- [x] Crear el fichero que inyecte estilos CSS condicionales en base a la paleta de colores de cada tipo elemental.
- [x] Los componentes reciben los datos en forma de texto plano, manteniendose desacoplados de la lógica del backend.

## Historia 11.2 - Paneles detallados de estadísticas/características y motor de combate
### Prioridad: MEDIA.
### Estado: COMPLETADO.

#### Descripción
Como usuario, me gustaría observar un desglose analítico de estadisticas, caracteristicas y efectividades en combate de un Pokemon.

### Criterios de aceptación
- [x] Crear el fichero que aloje gráficos para mostrar HP, Ataque, Defensa y Velocidad.
- [x] Construir un componente de visualización de vista al detalle de un Pokemon.
- [x] Construir un componente de visualización de efectividad en combate.
- [x] Construir un componente de visualización del árbol evolutivo.
---
# Epica 12 - Motor de búsqueda y filtros en UI
## Objetivo
Orquestar los componentes visuales y las interacciones del usuario para buscar mediante filtros, busqueda individual.

## Historia 12.1 - Pantallas de busqueda
### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Como usuario, quiero buscar cualquier Pokemon por su nombre o ID para buscar directamente su información.

### Criterios de aceptación
- [x] Diseño e implementación de páginas Home, busqueda individual y busqueda por filtros.
- [x] Implementar un control de entrada de texto.
- [x] Validar la cadena ingresada por el usuario, saneando faltas de ortografía, minúsculas, mayúsculas, etc.
- [x] Redirigir el flujo de control hacia la vista de detalles al confirmar una búsqueda válida.


---
# Epica 13 - Vista al detalle y cobertura de calidad

## Objetivo
Garantizar una adecuada integración de la vista de los diferentes Pokemon y asegurar los estándares de calidad mediante la integración continua.

## Historia 13.1 - Construir la Pantalla de Detalle
### Prioridad: ALTA.
### Estado: PENDIENTE.

#### Descripción
Como usuario, quiero ver la información del Pokemon reunida al ingresar a su detalle

### Criterios de aceptación
- [] Desarrollar la lógica de orquestación.
- [] Consumir adecuadamente los endpoints del backend.
- [] Asegurar que el flujo permita retirnar a la Home de forma limpia.

## Historia 13.2 - Integración y calidad del Frontend
### Prioridad: ALTA.
### Estado: EN CURSO.

#### Descripción
Como desarrollador, necesito que las herramientas automatizadas de nuestro CI validen la cálidad del código.

### Criterios de aceptación
- [x] Modificar el workflow para incluir el frontend unicamente para linteo y formateo con Ruff.
- [] Asegurar que el pipeline complete adecuadamente, pasan los tests del backend y el linteado/formateo del frontend.
