# DESCRIPCION DE DEPENDENCIAS

## CLASIFICACION
Clasificamos las dependencias en tres categorías:
1. Tecnología base: lenguaje, framework, servidor.
2. Librerías de terceros: paquetes externos (pip install).
3. Módulos estándar.

## RESUMEN DE DEPENDENCIAS
| Dependencia | Categoría | Versión | Módulo en que se usa |
| :---------: | :-------: | :-----: | :------------------: |
| Python      | Lenguaje base | ≥ 3.10 | Todos |
| FastAPI     | Framework backend | ≥ 0.10.0 | routes, main, dependencies |
| Uvicorn     | Servidor ASGI     | ≥ 0.23   | inicialización del backend |
| Streamlit   | Framework frontend| ≥ 1.30   | frontend                   |
| PokeAPI     | Fuente de datos externa | REST v2 | client, etl           |
| Pandas      | Análisis de datos | ≥ 2.0    | anallyzer, reporter, predictor, simulator
| NumPy       | Cálculos matemáticos | ≥ 1.24| simulator                  |
| httpx       | Cliente HTTP async| ≥ 0.25   | client                     |
| Pydantic    | Validación de datos | ≥ 2.0  | models, config, endpoints  |
| requests    | Cliente HTTP sincrónico | ≥ 2.28 | etl, client cli        |
| argparse    | Librería estándar para CLI | stdlib | cli                 |
| json        | Librería estándar para serializar | stdlib | teams, filters       |
| csv         | Librería estándar para exportación | stdlib | reporter    |
| asyncio     | Librería estándar para concurrencia| stdlib | client, routes, dependencias  |
| time        | Librería estándar como temporización | stdlib | client, cache, simulator |
| random      | Librería estándar para reproducir aleatoridad | stdlib | simulator, alerts |
| logging     | Librería estándar para trazabilidad | stdlib  | logging config, routes, client|

## TECNOLOGIAS BASE
- Python: Lenguaje principal de desarrollo.
- FastAPI: Framework web, soporte nativo que permite manejar multiples requests concurrentes, valida las requests y responses con Pydantic, además de generación de documentación automática, y dependency injection.
- Uvicorn: Servidor necesario para inicializar aplicaciones programadas con FastAPI y permite a la FastAPI gestionar peticiones concurrentes.
- Streamlit: Framework del frontend, permite construir interfaces interactivas en Python, sin necesidad de HTML o CSS, y permite introducir gráficos, tablas y formularios de búsqueda. Adicionalmente permite integrarse con pandas.
- PokeAPI: API REST pública gratuita, sin autenticación necesaria y provee datos estructurados de los 1025 Pokemon.

## LIBRERIAS DE TERCEROS
- Pandas: Permite realizar operaciones vectorizadas sin iterar, tiene métodos nativos de agrupación y agregación, y permiten realizar exportación directa a CSV.
- NumPy: La distribución de los datos es más eficiente y estadísticamente correcta.
- httpx: Permite mantener un pool de conexiones TCP abierto, reutilizable, que permite reducir el tiempo de respuestas.
- Pydantic: Permite definir los modelos de dominio, garantizando siempre se devuelva el tipo y estructura correcta de los datos. Además valida la configuración global en config que permite leer las variables de entorno con tipos forzados y valores por defecto.
- Requests: Utilizado en contextos donde no son necesarias funciones asíncronas, como el script ETL, que ya usa ThreadPool para paralelizar peticiones; y en el cliente del CLI, que al ser una herramienta de la línea de comandos, no es asíncrona.

## MODULOS ESTANDAR
Se prefieren su uso sobre librerías de terceros cuando cumplen la necesidad completamente, disminuyendo la necesidad de dependencias externas

- asyncio: Este módulo permite establecer concurrencia asíncrona basado en el event loop.
- json: Los ficheros JSON son más portables y legibles. Permite leer y escribir CRUD persistente y formatear las respuestas antes de ser mostradas en consola o frontend.
- csv: Módulo de lectura y escritura de ficheros csv. Se usa indirectamente ya que en los reportes se exporta de panda a csv, y directamente en el script ETL.
- time: Módulo de temporizador, usado para establecer la persistencia en caché, y en el rate limiting.
- random: Módulo de generación de aleatoridad.
- logging: Sistema de trazabilidad de eventos del sistema, para registrar errores o fallos del sistema de forma detallada, para hacer debugging y manejo de errores de forma ordenada y acertada.
- argparse: Módulo que permite construir interfaces de línea de comandos, permite parsear argumentos opcionales. Permite manejar los módulos dentro de la propia línea de comandos, sin necesidad de usar el menú interactivo.

## INYECCION DE DEPENDENCIAS
Se utiliza inyección de dependencias para inyectar en los servicios las funciones directamente, facilitando implementaciones sin tocar las clases, testing de manera más sencilla.
Separa la lógica de la infraestructura, reduce el acoplamiento y facilita cambios o mejoras futuras.
