# REGISTRO DE BUGS — SISTEMA POKÉDEX

## Formato: Descripción · Causa raíz · Solución · Lección aprendida


## BUG-01 — Excepciones HTTP no capturadas tras migración de requests a httpx

### Descripción del bug

Al buscar un Pokémon inexistente en los endpoints **/pokemon/{identifier}**, **/pokemon/{identifier}/evolution** y **/pokemon/{identifier}/effectiveness**, la API devolvía un error <u>HTTP 500 Internal Server Error</u> en lugar del esperado <u>HTTP 404 Not Found</u>.

Los tests funcionales E2E confirmaban el comportamiento incorrecto:

assert response.status_code == 404
AssertionError: assert 500 == 404
detail: "Error interno al procesar el motor analítico: ..."

El bug se reproducía en cualquier petición a la PokeAPI con un nombre o ID que no existiera, por ejemplo /api/v2/pokemon/missing_pokemon/evolution.


**Causa raíz**

El cliente HTTP fue migrado de requests a httpx para soporte asíncrono, pero el bloque try/except de pokeapi_client.py seguía capturando las excepciones del módulo antiguo:
```bash
Código tras la migración — captura excepciones de requests, pero el cliente ahora lanza excepciones de httpx

try:
    response = await self.client.get(url)
    response.raise_for_status()

except requests.exceptions.HTTPError as e:       # nunca se ejecuta
    if e.response.status_code == 404:
        raise ValueError("No se encontro el recurso...")
    raise

except requests.exceptions.ConnectionError as e: # nunca se ejecuta
    raise ConnectionError("No se pudo conectar...") from e

except requests.exceptions.Timeout as e:         # nunca se ejecuta
    raise TimeoutError("La peticion tardo demasiado...") from e
```
Como httpx lanza <u>httpx.HTTPStatusError</u>, <u>httpx.ConnectError</u> y <u>httpx.TimeoutException</u>, ningún except se activaba. La excepción escapaba sin capturar, el router la atrapaba como Exception genérica y devolvía un 500.


**Solución aplicada**

Se actualizaron los bloques except para capturar las excepciones correctas de httpx, manteniendo la misma lógica de traducción:

```bash
Código corregido
import httpx  # se eliminó el import de requests

try:
    response = await self.client.get(url)
    response.raise_for_status()

except httpx.HTTPStatusError as e:
    if e.response is not None and e.response.status_code == 404:
        raise ValueError(
            f"No se encontro el recurso: {endpoint}. "
            "Verifica que el nombre o ID sea correcto."
        ) from e
    raise

except httpx.ConnectError as e:
    raise ConnectionError("No se pudo conectar a la PokeAPI.") from e

except httpx.TimeoutException as e:
    raise TimeoutError(
        "La peticion a la PokeAPI tardo demasiado. "
        "Intenta de nuevo en unos momentos."
    ) from e
```

**Verificación:** los tests test_get_evolution_chain_e2e_not_found y test_e2e_effectiveness_not_found pasaron a verde confirmando el 404. Los tests unitarios de test_pokeapi_client.py también se actualizaron para simular las excepciones de httpx en lugar de las de requests.


**Lección aprendida**

Al migrar una dependencia de transporte HTTP (o cualquier librería externa), hay que auditar todos los bloques except que capturen excepciones específicas de esa librería. Una migración incompleta puede silenciar errores o cambiar el comportamiento de captura sin producir errores de compilación, haciendo que el bug sea difícil de detectar.

**Práctica recomendada:** definir una capa de traducción de excepciones aislada en el cliente (el propio pokeapi_client.py) que convierta excepciones de librería en excepciones genéricas de Python (ValueError, ConnectionError, TimeoutError). Las capas superiores (servicios, routers) solo capturan excepciones estándar y quedan desacopladas de la librería HTTP utilizada.




## BUG-02 — Event loop is closed al reutilizar un httpx.AsyncClient entre tests

### Descripción del bug

Al ejecutar la suite completa de tests, el **test funcional E2E test_e2e_effectiveness_not_found** fallaba con <u>HTTP 500</u> y el siguiente mensaje en el detalle:

```bash
{'detail': 'Error interno al procesar el motor analítico: Event loop is closed'}
```

El mismo endpoint funcionaba correctamente cuando se ejecutaba en aislamiento o en producción. El bug solo se reproducía al correr todos los tests juntos, específicamente cuando test_pokedex_e2e.py se ejecutaba después de otros módulos de test.


**Causa raíz**

En dependencias.py, el cliente HTTP se instanciaba como singleton global a nivel de módulo:

```bash
Se crea una vez al importar el módulo
_cache_instance   = CacheManager()
_client_instance  = PokeAPIClient(cache=_cache_instance)

def get_client() -> PokeAPIClient:
    return _client_instance
```

PokeAPIClient.__init__ crea internamente un **httpx.AsyncClient**, que queda ligado al event loop activo en el momento del import. Pytest crea un event loop distinto para cada módulo de test. Cuando el módulo test_pokedex_e2e.py se ejecutaba, el loop original (con el que se creó el AsyncClient) ya había sido cerrado por los tests anteriores, produciendo el error <u>RuntimeError: Event loop is closed</u>.

Adicionalmente, get_client era una función síncrona (def), lo que hacía que FastAPI la ejecutara en un threadpool sin event loop activo, impidiendo detectar el cambio de loop con **asyncio.get_running_loop()**.


**Solución aplicada**

Se convirtió get_client en una función asíncrona y se añadió detección del event loop activo para recrear el cliente cuando cambia:

```bash
Código corregido en dependencias.py
import asyncio

_cache_instance: CacheManager          = CacheManager()
_client_instance: PokeAPIClient | None = None
_client_loop: asyncio.AbstractEventLoop | None = None

async def get_client() -> PokeAPIClient:
    global _client_instance, _client_loop

    current_loop = asyncio.get_running_loop()

    if _client_instance is None or _client_loop is not current_loop:
        _client_instance = PokeAPIClient(cache=_cache_instance)
        _client_loop     = current_loop

    return _client_instance
```

Al ser async def, FastAPI ejecuta la función directamente en el event loop activo (no en threadpool), lo que permite detectar correctamente si el loop cambió y recrear el AsyncClient con el loop correcto.

**Verificación:** el test **test_e2e_effectiveness_not_found** pasó a verde en todas las ejecuciones de la suite completa, independientemente del orden de los módulos de test.


**Lección aprendida**

Los objetos asíncronos como **httpx.AsyncClient** o **asyncio**. Que están ligados al event loop en el que se crean y no pueden usarse desde un loop distinto. Instanciarlos como singletons globales a nivel de módulo es un antipatrón en entornos de test.

**Práctica recomendada:** gestionar el ciclo de vida de los clientes asíncronos mediante el mecanismo lifespan de FastAPI, que garantiza que se creen y destruyan dentro del mismo event loop de la aplicación. Para entornos de test, usar dependencias async permite que FastAPI resuelva la inyección siempre dentro del loop correcto.



## BUG-03 — Servicios fake síncronos en tests de integración causaban error de await

### Descripción del bug

Los tests de integración **test_integration_pokemon_success**, **test_integration_evolution_success** y **test_integration_effectiveness_success** fallaban con <u>HTTP 500</u> en lugar de <u>HTTP 200</u>:

```bash
AssertionError: assert 500 == 200

detail: "Error interno al procesar el motor analítico: object PokemonDetail can't be used in 'await' expression"
```

El router sí recibía los datos correctos del fake, pero explotaba al intentar procesarlos.


**Causa raíz**

Al migrar los servicios reales a async def, los métodos de los servicios fake usados en tests seguían siendo síncronos:

```bash
Fake síncrono — el router hace await sobre él

class FakePokemonService:
    def get_pokemon_detail(self, identifier: str) -> PokemonDetail:
        return PokemonDetail(id=25, name="pikachu", ...)

class FakeEvolutionService:
    def get_evolution_tree(self, identifier: str) -> EvolutionNode:
        return EvolutionNode(id=1, name="bulbasaur", ...)
```

El router llamaba await **pokemon_service.get_pokemon_detail(identifier)**. Cuando el método es síncrono, Python no devuelve una corrutina sino directamente el objeto PokemonDetail. Hacer await sobre un objeto que no es una corrutina lanza TypeError, que el router capturaba como Exception genérica y convertía en 500.

El bug afectaba solo a **FakePokemonService** y **FakeEvolutionService** porque sus métodos reales son async def. **FakeBattleService** no se veía afectado porque calculate_effectiveness en el servicio real también es síncrono.


**Solución aplicada**

Se añadió async def a los métodos de los fakes que corresponden a métodos asíncronos en el servicio real:

```bash
Fakes corregidos
class FakePokemonService:
    async def get_pokemon_detail(self, identifier: str) -> PokemonDetail:
        if identifier in ("25", "pikachu"):
            return PokemonDetail(id=25, name="pikachu", ...)
        raise ValueError(f"Pokemon {identifier} no existe en la base de datos")

class FakeEvolutionService:
    async def get_evolution_tree(self, identifier: str) -> EvolutionNode:
        if identifier == "1":
            return EvolutionNode(id=1, name="bulbasaur", ...)
        raise ValueError("Cadena evolutiva no encontrada")

# FakeBattleService NO se modifica — calculate_effectiveness es síncrono
class FakeBattleService:
    def calculate_effectiveness(self, types: list[str]) -> dict:
        ...
```
**Verificación:** los tres tests pasaron a verde con <u>HTTP 200</u> y los datos correctos en el body de la respuesta.


**Lección aprendida**

Los objetos fake o mock usados en tests de integración deben replicar exactamente la misma firma que el servicio real: si el método real es async def, el fake también debe serlo. Un fake síncrono que sustituye a un método asíncrono pasa la inyección de dependencias sin errores pero falla en tiempo de ejecución cuando el caller hace await.

**Práctica recomendada:** definir un protocolo (typing.Protocol) o clase base abstracta para cada servicio, de modo que los fakes estén obligados a implementar la misma firma. Alternativamente, usar **unittest.mock.AsyncMock** en lugar de clases fake manuales para métodos asíncronos, ya que **AsyncMock** es awaitable por defecto:

```bash
pythonfrom unittest.mock import AsyncMock

pokemon_service_mock = AsyncMock()
pokemon_service_mock.get_pokemon_detail.return_value = PokemonDetail(...)
```


## BUG-04 — parse_pokemon_description recibía una corrutina en lugar de un dict

### Descripción del bug

El test unitario test_get_pokemon_detail_success fallaba con el siguiente traceback:

```bash
TypeError: 'coroutine' object is not iterable

app\parsers\pokemon_parser.py:94: in parse_pokemon_description
    for entry in entries:
```

El servicio **PokemonService.get_pokemon_detail** fallaba al intentar parsear la descripción del Pokémon, aunque los datos del mock eran correctos.


**Causa raíz**

En el test, client_mock era un **AsyncMock** completo. Al configurar solo el retorno de get_pokemon, get_species quedaba como un **AsyncMock** sin valor de retorno configurado:

```bash
Solo se mockea get_pokemon, get_species queda como AsyncMock vacío
client_mock = AsyncMock()
client_mock.get_pokemon.return_value = { "id": 25, "name": "pikachu", ... }

# En pokemon_service.py:
species_data = await self.client.get_species(pokemon_id)
# species_data es ahora un MagicMock, no un dict

flavor_text = parse_pokemon_description(species_data)
# parse_pokemon_description intenta iterar species_data.get("flavor_text_entries")
# → TypeError: 'coroutine' object is not iterable

AsyncMock() sin return_value configurado devuelve otro MagicMock al ser awaited, que no es un diccionario iterable.
```

**Solución aplicada**

Se añadió la configuración del retorno de get_species en el test, con un diccionario válido (lista vacía de flavor texts):

```bash
Test corregido
client_mock = AsyncMock()

client_mock.get_pokemon.return_value = {
    "id": 25, "name": "pikachu",
    "types": [{"type": {"name": "electric"}}],
    ...
}

# Se configura también get_species para que devuelva un dict válido
client_mock.get_species.return_value = {
    "flavor_text_entries": []   # lista vacía → flavor_text = None
}

service = PokemonService(client_mock)
pokemon = await service.get_pokemon_detail("pikachu")
```

**Verificación:** el test pasó a verde y **pokemon.flavor_text_entry** resultó None (comportamiento esperado con lista vacía).


**Lección aprendida**

Al usar AsyncMock para testear servicios que realizan múltiples llamadas al cliente, hay que configurar el return_value de todas las llamadas que el servicio realiza internamente, no solo la principal. Un AsyncMock sin return_value no lanza error al ser llamado — devuelve silenciosamente un objeto que puede romper código posterior de formas difíciles de rastrear.

**Práctica recomendada:** al escribir tests unitarios para un servicio, revisar el código fuente del método bajo test y listar todas las llamadas al cliente que realiza. Configurar un return_value explícito para cada una, incluso si el valor es vacío ({}, []). Esto hace los tests más expresivos y evita fallos silenciosos por mocks incompletos.