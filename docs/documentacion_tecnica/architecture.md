# Arquitectua proyecto - Pokedex

## Objetivo general

Este proyecto se centra en crear una Pokedex, aplicacion web modular, escalable, y sostenible que permita la busqueda de datos Pokemon en base a PokeAPI, una API publica que recoge informacion general y especifica de todos los Pokemones.

La arquitectura y diseño se estructuraron para realizar una separacion logica, de responsabilidades, establecer una arquitectura por capas, que permita un manejo adecuado de errores, nuevas funcionalidades y escalabilidad en cache, base de datos y frontend

## Diagrama de arquitectura

```text
Flujo del aplicativo web

Flujo Principal

1. A[Usuario] ── Interactua con ──> B[Frontend-Streamlit]
2. B[Frontend-Streamlit] ── Se conecta a su ──> C[Backend-Client]
3. C[Backend-Client] ── Hace HTTP request ──> D[Backend-FastAPI]
4. E[Backend-FastAPI] ── mira en ──> F[Routes]
5. F[Routes] ── Dirige a ──> G[Services]

Flujo interno Backend

1. G[Services] ── Llama a ──> H[Cache-Manager]
        │                            └── Consulta a ──> I[Cache]
        ├── Consulta a ──> J[Dataset]
        │
        └── Llama a ──> K[PokeAPI-Client]
                                └── Consulta a ──> L[PokeAPI]

Flujo de transformación de datos

1. L[PokeAPI] ── Envía la info a ──> K[PokeAPI-Client]
2. K[PokeAPI-Client] ── Envía datos JSON a ──> G[Services]
3. G[Services] ── Pasa datos ──> M[Parsers]
        └──G[Services] ── Utiliza ──>  N[Models]
4. M[Parsers] ── Construye instancias de ──> N[Models]

Flujo de persistencia de datos

1. G[Services] ── Envía info a ──> H[Cache-Manager]
2. H[Cache-Manager] ── guarda datos ──> I[Cache]

Estructura principal
    pokedex/
        │
        ├──backend/
        │
        ├──frontend/
        │
        ├──tests/
        │
        ├──docs/
        │
        ├──data/
        │
        ├──client_cli.py
        │
        ├──cli.py
        │
        ├──README.md
        │
        ├──.toml
        │
        └──.gitignore


- backend/: el backend se construyo mediante Fastapi y con una arquitectura modular por capas
        │
        └──app/
            │
            │       **RESPONSABILIDADES:** Orquestador.
            │           - Iniciar aplicacion.
            │           - Registrar routers, conecta las rutas en un archivo separado.
            │           - Configura middlewares (CORSMiddleware).
            │           - Configura un endpoint /health para verificar que el sistema esta en funcionamiento.
            │           - Levanta el servidor (inicalizar par empezar con las peticiones).
            │
            │
            ├──api/
            │
            │       **RESPONSABILIDADES:** Controlador de la entrada a la Pokedex.
            │           - Define los endpoints de API: expone la Pokedex al frontend y defino URLs de acceso.
            │           - Validar parametros: Valida inputs, y define filtros de consulta.
            │           - Llamar a services: delega la logica a los diferentes services.
            │           - Retomar respuestas JSON.
            │           - Maneja los errores HTTP: levanta errores internos y mantiene a la app en funcionamiento.
            │
            │
            ├──clients/
            │
            │       **RESPONSABILIDADES:** Llamadas inteligentes a API.
            │            - Se comunica con la PokeAPI (publica externa): hace las HTTP request, obtiene los datos │pokemon.
            │           - Rate limiting: establece un limite de peticiones.
            │           - Evitar llamadas repetidas.
            │           - Normaliza inputs: Errores en mayusuclas o minusculas, queries.
            │           - Abstraccion de endpoints y metodos semanticos a los diferentes dominios Pokemon.
            │
            │
            ├──services/
            │
            │       **RESPONSABILIDADES:** Que puede hacer mi app (tipos, evoluciones, stats, sprites, etc)
            │           - Maneja las llamadas a PokeAPIClient: pide los datos.
            │           - Define diferentes usos y detalles de Pokemones: establece que datos o acciones podemos realizar con nuestra Pokedex.
            │           - Pide la cadena evolutiva de un Pokemon desde PokeAPI: resuelve URLs encadenadas.
            │           - Construye el arbol de evoluciones.
            │           - Limpia y ordena los datos de una evolucion.
            │           - Cargar el dataset local.
            │           - Aplica los filtros de busqueda configurados.
            │           - Optimiza la consulta para los filtros, evitando hacer varios llamados a la API, haciendo un dataset con datos basicos.
            │           - Obtiene datos de tipos desde client.
            │           - Muestra la dinamica de las interacciones de daño recibido entre Pokemones.
            │           - Genera alertas, predicciones, y datos simulados.
            │
            │
            ├──parsers/
            │
            │       **RESPONSABILIDAD**: primera capa de parser
            │           - Adapta los JSON externos en un modelo interno configurado.
            │           - Limpia y normaliza datos.
            │           - Selecciona la informacion relevante.
            │           - Encapsula los datos externos para entregar una estructura unitaria a la app.
            │           - Parsear JSON, navega estructuras anidadas.
            │           - Limpia info irrelevante.
            │           - Crea una estructura apropiada para el frontend.
            │           - Transforma datos externos a un diseño interno.
            │           - Toma las relaciones de daño.
            │           - Simplifica datos y encapsula info externa.
            │
            │
            ├──models/
            │
            │       **RESPONSABILIDAD:** lenguaje interno de nuestra Pokedex.
            │           - Define como se vera un Pokemon en nuestra app.
            │           - Representa varios dominios Pokemon(datos resumidos, datos completos, relaciones de tipos, nodo evolutivo).
            │           - Estandariza los datos, evita inconsistencias.
            │           - Separa el dominio de JSON externo, nuestra app ya no depende de datos JSON de la API externa, sino de nuestro models.
            │
            │
            ├──cache/
            │
            │       **RESPONSABILIDAD:** adapta nuestra infraestructura de datos.
            │           - Inicializa infraestructura de la cache, es decir, si no hay datos, crea la base de datos y define el esquema cache.
            │           - Guarda datos en la cache.
            │           - Obtiene datos desde la cache.
            │           - Manejo del Time to Live (ttl).
            │
            │
            ├──core/
            │
            │       **RESPONSABILIDAD**: centro de la configuracion de la app.
            │           - Define configuracion global: metadatos, identificadores globales.
            │           - Configura nuestra PokeAPI, como se estructura, dependencias externas.
            │           - Configura el desempeño de la app, comportamiento del sistema.
            │           - Define storage local, configura CORS.
            │           - Configuracion externa.
            │           - Constantes de integracion, define endpoints, centraliza dependencias.
            │           - Contiene las reglas fijas de performance.
            │           - Reglas: idiomas aceptados.
            │
            │
            ├──data/
            │     └──seeds/
            │
            │       **RESPONSABILIDAD**: script ETL (Extraer, Transformar y Cargar(Load)) y dataset local
            │           - Extrae un gran volumen de datos de la API externa.
            │           - Itera y extrae datos necesarios.
            │           - Normaliza los datos.
            │           - Crea un dataset local.
            │           - Manejo de errores por intentos y rate control.
            │           - Contiene datos Pokemones de acuerdo a los filtros de nuestra app.
            │           - Brinda los datos de forma resumida y modelada para presentar los datos cuando se coloque un filtro de busqueda.
            │
            │
            ├──utils/
            │
            │      **RESPONSABILIDAD**: paleta de colores y reglas del combate Pokemon.
            │          - Mapea los tipos de Pokemon y los empareja con un color.
            │          - Estandariza los colores en nuestro frontend.
            │          - Diccionario global de colores.
            │          - Define las reglas de combate.
            │          - Calcula la efectividad de los tipos.
            │          - Combina los efectos de multiples tipos y clasifica los resultados.
            │
            │
            ├──dependencies/
            │
            │      **RESPONSABILIDAD**
            │          - Crea infraestructura base.
            │          - Conecta el cliente con la cache.
            │          - Ensambla la logica de la app e inyecta infraestructura en services.
            │          - Centraliza instancias globales.
            └──


- frontend/: aqui se presenta la arquitectura de nuestro frontend, esta sera nuestra capa de presentacion al cliente, el que orquesta la interfaz de usuario.
        │
        └──streamlit/
                   ├──Pokedex.py:
                   │
                   │       **RESPONSABILIDADES:**
                   │           - Funciona de ancla o punto principal de nuestro frontend.
                   │
                   │
                   ├──api/
                   │
                   │       **RESPONSABILIDADES**: es el http client del frontend.
                   │           - Conecta Streamlit con nuestra API interna en el backend.
                   │           - Encapsula HTTP requests.
                   │           - Abstrae endpoints.
                   │
                   │
                   ├──clients/
                   │
                   │       **RESPONSABILIDAD**: Llamadas inteligentes a API.
                   │           - Se comunica con la PokeAPI (publica externa): hace las HTTP request, obtiene los datos │pokemon.
                   │           - Rate limiting: establece un limite de peticiones.
                   │           - Evitar llamadas repetidas.
                   │           - Normaliza inputs: Errores en mayusuclas o minusculas, queries.
                   │           - Abstraccion de endpoints y metodos semanticos a los diferentes dominios Pokemon.
                   │
                   │
                   ├──components/
                   │
                   │       **RESPONSABILIDAD**: representa las diferentes funcionalidades de la app.
                   │           - Representa en la UI las interacciones de resistencia y debilidades de los Pokemones.
                   │           - Representa en la UI el arbol de evoluciones de un Pokemon.
                   │           - Incluye dentro de la representacion los requisitos para su evolucion.
                   │           - Renderiza una carta, representacion visual del Pokemon.
                   │           - Representa los stats de un Pokemon en un grafico tipo radar.
                   │           - Renderiza una insignia de acuerdo al tipo del Pokemon seleccionado.
                   │
                   │
                   │
                   ├──pages/
                   │
                   │       **RESPONSABILIDADES:** Presente en diferentes páginas, todas las funcionalidades de la app.
                   │           - Compara las stats.
                   │           - Muestra las diferencias entre Pokemones.
                   │           - Pagina inicial de interacicon del usuario.
                   │           - Contiene las barras y filtros de busqueda.
                   │           - Es la pagina a traves de la cual se navega en nuestra app.
                   │           - Ensambla la interfaz del usario a detalle.
                   │           - Establece una logica en la UI de seleccion de Pokemones.
                   │           - Aloja la Home page, pagina de busqueda por filtros, pagina de busquedas individuales, constructor de equipos y comparador Pokemon
                   │
                   │
                   │
                   ├──utils/
                   │
                   │       **RESPONSABILIDADES:** Se presentan todos los assets necesarios para construir una app con un diseño agradable.
                   │           - Constantes de integracion, define endpoints, centraliza dependencias.
                   │           - Contiene las reglas fijas de performance.
                   │           - Reglas: idiomas aceptados.
                   │           - Mapea los tipos de Pokemon y los empareja con un color.
                   │           - Estandariza los colores en nuestro frontend.
                   │           - Diccionario global de colores.
                   │           - Contiene funciones que se llaman para su uso en el frontend
                   │
                   └──views/
                      │
                      │    **RESPONSABILIDADES:** Se encuentra la configuracion del renderizado de todas las paginas de la app.
                      │        - Tiene el renderizado y el diseño de la pagina Home, busqueda individual, comparador de Pokemons y constructor de equipos.
                      └──

- docs/: Contiene los archivos api_design.md, architecture.md, backlog.md, changelog.md, psuedocode.md, roadmap.md.
- tests/: en esta carpeta yacen los tests, unitarios, de integracion y funcionales para la aplicacion y la aseguracion de la calidad del codigo.
- data/: Contiene los archivos csv generados como parte del servicio de reportes.
- client_cli.py: Es el módulo que contiene el client que utilizará el cli, para una consolo interactiva
- cli.py: Contiene el modulo cli, con un menu interactivo
```

# Tecnologias que usa la app

- Python ---> El lenguaje principal de programacion de la app.
- Fastapi ---> Backend de nuestra API.
- Streamlit ---> Frontend actual.
- PokeAPI ---> Fuente de datos externa.
- Uvicorn ---> Servidor ASGI.

## Librerías utilizadas
- Pandas.
- Numpy.
- httpx.
- pydantic.
- requests.

## Módulos estándar de python
- argparse.
- json.
- csv.
- asyncio.
- time.
- random.
- logging.
- argparse.

# Flujo de datos

1. Usuario realiza una busqueda en la interfaz de usuario (frontend).
2. Streamlit llama al backend, a nuestra FastAPI.
3. FastAPI recibe la peticion mediante routes.py.
4. Routes.py llama al Services correspondiente.
5. Services consulta inicialmente la cache.
6. Si no existe la informacion en la cache ---> se hace el llamado a la API externa.
7. Se recibe la respuesta y se parsean los datos.
8. Los datos parseados se transforman en un Models interno.
9. Se almacenan los datos en la cache.
10. Se envia la respuesta a frontend.
11. Frontend muestra los datos de acuerdo al diseño escrito.
12. Usuario ve la respuesta de su busqueda en UI.