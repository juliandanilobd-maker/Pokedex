# FAQ — RESOLUCIÓN DE PROBLEMAS FRECUENTES

---

## ERROR 1 — No se puede conectar con el servidor

### Síntoma
```
ERROR: No se pudo conectar con el servidor local Consejo: Asegúrate de tener levantado uvicorn en el puerto 8000.
```
O bien, al usar `curl` o el navegador:
```
ConnectionRefusedError: [WinError 10061] No se puede establecer una conexión
```

### Causa
El servidor backend no está en ejecución. El CLI intenta conectarse a `http://localhost:8000` pero no hay ningún proceso escuchando en ese puerto.

### Solución
Abre una terminal **separada** en la raíz del proyecto y ejecuta:

```bash
uvicorn backend.main:app --reload --port 8000
```

Espera hasta ver el mensaje:
```
INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Luego vuelve a tu terminal del CLI y reintenta la operación.

### Verificación rápida
```bash
# Comprueba si el puerto 8000 está ocupado
# Windows:
netstat -ano | findstr :8000

# Linux/Mac:
lsof -i :8000
```

Si el puerto aparece como `LISTENING`, el servidor está activo.

---

## ERROR 2 — Pokémon no encontrado (HTTP 404)

### Síntoma
```
DETALLE DEL ERROR RETORNANDO POR FASTAPI (HTTP 404):
{
  "detail": "No se encontro el recurso: pokemon/missing_pokemon.
             Verifica que el nombre o ID sea correcto."
}
```

### Causas frecuentes

**a) Nombre mal escrito o en el idioma incorrecto**

```bash
# Incorrecto
python cli.py pokemon Pikacha
python cli.py pokemon "Charmander"
python cli.py pokemon charizardo   # nombre en español

# ✅ Correcto
python cli.py pokemon pikachu
python cli.py pokemon charmander
python cli.py pokemon charizard
```

**b) Forma alternativa con nombre incompleto**
Algunas formas alternativas requieren el sufijo completo:

```bash
# Incorrecto
python cli.py pokemon giratina

# Correcto — especifica la forma
python cli.py pokemon giratina-altered
python cli.py pokemon giratina-origin
```

**c) ID fuera de rango**
El dataset incluye Pokémon hasta la generación 9. IDs superiores a ~1010 pueden no existir en la PokeAPI.

### Solución
1. Usa el ID numérico en lugar del nombre: `python cli.py pokemon 25`
2. Consulta el nombre exacto en [pokeapi.co](https://pokeapi.co)
3. Usa el filtro para buscar por tipo y encontrar el ID correcto:
   `python cli.py filter --type fire`

---

## ERROR 3 — Parámetro inválido en filtros (HTTP 422)

### Síntoma
```
DETALLE DEL ERROR RETORNANDO POR FASTAPI (HTTP 422):
{
  "detail": [
    {
      "type": "int_parsing_error",
      "loc": ["query", "generation"],
      "msg": "Input should be a valid integer"
    }
  ]
}
```

### Causa
Se pasó un valor en formato incorrecto a uno de los parámetros del filtro. Por ejemplo, escribir `"primera"` en el campo de generación en lugar de `1`.

### Solución

| Parámetro | Formato correcto | Ejemplo |
|---|---|---|
| `generation` | Entero entre 1 y 9 | `1`, `2`, `9` |
| `min_hp` | Entero positivo | `50`, `100` |
| `min_attack` | Entero positivo | `80` |
| `min_defense` | Entero positivo | `70` |
| `min_speed` | Entero positivo | `90` |
| `min_base_exp` | Entero positivo | `200` |
| `pokemon_type` | Cadena en minúsculas | `fire`, `water`, `grass` |

```bash
# Incorrecto
python cli.py filter --gen primera --type Fuego

# Correcto
python cli.py filter --gen 1 --type fire
```

> En el menú interactivo, si dejas un campo vacío y presionas ENTER, ese filtro no se aplica (equivale a "sin restricción").

---

## ERROR 4 — Predicción falla por generaciones insuficientes

### Síntoma
```
DETALLE DEL ERROR RETORNANDO POR FASTAPI (HTTP 404):
{
  "detail": "Solo hay 1 generaciones para tipo 'flying'.
             Se necesitan al menos 2 generaciones para calcular la media móvil."
}
```

### Causa
El algoritmo de predicción usa una **media móvil simple** que necesitadatos de al menos 2 generaciones distintas para el tipo (o combinación
de tipos) solicitado. Algunos tipos tienen muy pocos representantes distribuidos entre generaciones, o la combinación de tipo dual es muy rara.

### Solución

**a) Usa solo el tipo primario** (sin tipo secundario):
```bash
# flying/dragon puede tener pocos datos
python cli.py analytics prediction flying --secondary dragon

# flying solo tiene más representantes
python cli.py analytics prediction flying
```

**b) Prueba tipos con más representantes históricos:**
Los tipos con más Pokémon distribuidos entre generaciones son:
`water`, `normal`, `grass`, `psychic`, `fire`, `bug`, `poison`.

```bash
python cli.py analytics prediction water
python cli.py analytics prediction fire
python cli.py analytics prediction psychic
```

**c) Combinaciones duales que sí funcionan** (suficientes datos):
```bash
python cli.py analytics prediction grass --secondary poison
python cli.py analytics prediction fire --secondary flying
python cli.py analytics prediction water --secondary psychic
```

---

## ERROR 5 — Dataset local vacío o no generado

### Síntoma
```
Anomalía inesperada en el laboratorio:
El dataset local está vacío o no se ha guardado correctamente.
Ejecuta el script ETL antes de continuar.
```

O bien, los endpoints de analytics devuelven listas vacías `[]`.

### Causa
Los servicios `AnalyzerService`, `FilterService`, `PredictorService` y `SimulatorService` trabajan sobre un dataset local en formato JSON/CSV
generado por el script ETL. Si ese archivo no existe o está corrupto, estos servicios no pueden funcionar.

### Solución
Ejecuta el script ETL desde la raíz del proyecto:

```bash
python -m backend.app.data.scripts.dataset_generator
```

Espera a que termine (puede tardar varios minutos en descargar datos de
la PokeAPI). Al finalizar verás algo como:
```
Dataset generado: 1010 Pokemon guardados en data/pokemon_dataset.json
```

Luego reinicia el servidor uvicorn para que cargue el dataset actualizado.

---

## ERROR 6 — Equipo no encontrado al consultar o eliminar

### Síntoma
```
DETALLE DEL ERROR RETORNANDO POR FASTAPI (HTTP 404):
{
  "detail": "No se encontró ningún equipo con ID 'mi-equipo'."
}
```

### Causa
Se está usando el **nombre** del equipo donde se espera el **UUID**, o el equipo fue eliminado previamente.

### Solución

**a) Obtén primero el UUID** listando todos los equipos:
```bash
python cli.py team list
```

La respuesta incluye el campo `"id"` con el UUID completo:
```json
{
  "id": "eba285df-3e7d-4bdd-ad4f-2b3a7d16dc95",
  "name": "Equipo Alpha"
}
```

**b) Usa ese UUID** para consultar o eliminar:
```bash
python cli.py team get eba285df-3e7d-4bdd-ad4f-2b3a7d16dc95
python cli.py team delete eba285df-3e7d-4bdd-ad4f-2b3a7d16dc95
```

> **Nota:** el sistema también acepta el nombre del equipo si es único. Si hay dos equipos con el mismo nombre, deberás usar el UUID para evitar ambigüedad.

---

## ERROR 7 — El CSV exportado está vacío o no se genera

### Síntoma
```
No hay resultados para exportar.
Realiza un filtro con datos primero.
```

### Causa
Se intentó exportar a CSV sin resultados. Esto ocurre cuando:
- El filtro aplicado no devuelve ningún Pokémon.
- Se intentó exportar directamente sin haber realizado una búsqueda previa.

### Solución

Verifica primero que el filtro devuelve resultados usando el módulo `[3]` del menú o el comando directo:

```bash
# Comprueba que hay resultados antes de exportar
python cli.py filter --type fire

# Si hay resultados, exporta
python cli.py export filter --type fire
```

Si el filtro devuelve 0 elementos, amplía los criterios de búsqueda (reduce los valores mínimos o elimina algún parámetro).

---

## TABLA DE REFERENCIA RÁPIDA

| Problema | Código HTTP | Solución rápida |
|---|---|---|
| Servidor no responde | — (timeout) | Ejecutar `uvicorn backend.main:app --reload` |
| Pokémon no existe | 404 | Verificar nombre en inglés y minúsculas |
| Parámetro inválido | 422 | Usar enteros para stats/generación, minúsculas para tipos |
| Predicción sin datos | 404 | Probar con tipo primario solo o tipos más comunes |
| Analytics sin datos | 500 | Regenerar dataset con el script ETL |
| Equipo no encontrado | 404 | Listar equipos primero para obtener el UUID |
| CSV vacío | — (ValueError) | Verificar que el filtro retorna resultados antes de exportar |
| Error interno genérico | 500 | Revisar logs de uvicorn para el traceback completo |