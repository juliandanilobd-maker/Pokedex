# GUÍA DE INTERPRETACIÓN DE RESULTADOS — SISTEMA POKÉDEX

Esta guía explica qué significa cada campo de las respuestas del sistema, cómo leer los gráficos ASCII y cómo actuar ante cada tipo de alerta.

---

## ESTRUCTURA GENERAL DE UNA RESPUESTA

Todas las respuestas del laboratorio siguen el mismo patrón de salida:

```
✅ [HTTP 200] ESTRUCTURA DE DATOS CAPTURADA EXITOSAMENTE:
{ ... }
```

Un `HTTP 200` significa que la petición llegó al backend, fue procesada correctamente y devolvió datos válidos. Cualquier otro código indica un problema (ver sección FAQ).

---

## [1] FICHA INDIVIDUAL DE POKÉMON — `/pokemon/{identifier}`

```json
{
  "id": 25,
  "name": "pikachu",
  "types": ["electric"],
  "stats": {
    "hp": 35,
    "attack": 55,
    "defense": 40,
    "special-attack": 50,
    "special-defense": 50,
    "speed": 90
  },
  "abilities": ["static", "lightning-rod"],
  "height": 4,
  "weight": 60,
  "base_experience": 112,
  "sprite_url": "https://...",
  "sprite_shiny": "https://...",
  "flavor_text_entry": {
    "text": "Levanta su cola para vigilar los alrededores...",
    "language": "es",
    "version": "x"
  }
}
```

| Campo | Significado |
|---|---|
| `id` | Número nacional en la Pokédex. Identifica al Pokémon de forma única. |
| `name` | Nombre en minúsculas, normalizado para uso en la API. |
| `types` | Lista de tipos elementales. Puede tener 1 o 2 valores. Determina debilidades y resistencias. |
| `stats.hp` | Puntos de vida base. Cuanto mayor, más daño puede recibir antes de debilitarse. |
| `stats.attack` | Ataque físico base. Determina el daño de movimientos físicos. |
| `stats.defense` | Defensa física base. Reduce el daño recibido de movimientos físicos. |
| `stats.special-attack` | Ataque especial. Determina el daño de movimientos especiales (rayos, llamas, etc.). |
| `stats.special-defense` | Defensa especial. Reduce el daño de movimientos especiales. |
| `stats.speed` | Velocidad base. El Pokémon más rápido actúa primero en combate. |
| `abilities` | Habilidades disponibles. Pueden otorgar efectos pasivos en combate. |
| `height` | Altura en decímetros (÷10 = metros). Pikachu mide 0.4 m. |
| `weight` | Peso en hectogramos (÷10 = kilogramos). Pikachu pesa 6 kg. |
| `base_experience` | Experiencia base que otorga al ser derrotado. Mayor valor = más difícil de vencer. |
| `sprite_url` | URL del artwork oficial. `null` si no está disponible. |
| `sprite_shiny` | URL del artwork en versión shiny (coloración alternativa). |
| `flavor_text_entry.text` | Descripción del Pokémon extraída de la Pokédex oficial. |
| `flavor_text_entry.language` | Idioma de la descripción (`es` = español). |
| `flavor_text_entry.version` | Juego del que proviene la descripción (`x`, `y`, `sword`, etc.). |

> **Nota:** si `flavor_text_entry` es `null`, significa que no hay descripción disponible en español para ese Pokémon en el dataset actual.

---

## [2] ÁRBOL EVOLUTIVO — `/pokemon/{identifier}/evolution`

```json
{
  "id": 172,
  "name": "pichu",
  "children": [
    {
      "id": 25,
      "name": "pikachu",
      "children": [
        {
          "id": 26,
          "name": "raichu",
          "children": [],
          "evolution_details": [
            {
              "min_level": null,
              "item": "thunder-stone",
              "trigger": "use-item",
              "min_happiness": null,
              "time_of_day": null
            }
          ]
        }
      ],
      "evolution_details": [
        {
          "trigger": "level-up",
          "min_happiness": 220
        }
      ]
    }
  ],
  "evolution_details": null
}
```

La respuesta es un **árbol recursivo**: el nodo raíz es la forma base y `children` contiene sus evoluciones, que a su vez pueden tener sus propias `children`.

| Campo | Significado |
|---|---|
| `id` | ID del Pokémon en ese eslabón de la cadena. |
| `name` | Nombre del Pokémon en ese eslabón. |
| `children` | Lista de evoluciones posibles. Lista vacía `[]` = forma final. |
| `evolution_details` | Condiciones para alcanzar esa evolución (ver tabla abajo). `null` en la forma base. |
| `visibility` | Indica si ese nodo se muestra en la interfaz. |

### Tabla de condiciones de evolución (`evolution_details`)

| Campo | Significado |
|---|---|
| `trigger` | Cómo se desencadena: `level-up` (subir nivel), `use-item` (usar objeto), `trade` (intercambio), `other`. |
| `min_level` | Nivel mínimo requerido. `null` si no aplica. |
| `item` | Objeto necesario (ej. `thunder-stone`, `fire-stone`). `null` si no aplica. |
| `min_happiness` | Felicidad mínima requerida (escala 0–255). `null` si no aplica. |
| `time_of_day` | Momento del día requerido (`day`, `night`). `null` si no aplica. |
| `location` | Lugar específico requerido. `null` si no aplica. |
| `min_affection` | Afecto mínimo en Pokémon-Amie. `null` si no aplica. |

> **Cómo leerlo:** Pichu → Pikachu requiere `level-up` con `min_happiness: 220`
> (alta felicidad). Pikachu → Raichu requiere `use-item` con `thunder-stone`.

---

## [3] FILTROS AVANZADOS — `/filter`

```
🗂️ Estructura: Lista (Contiene 81 elementos)
```

La respuesta es una lista de Pokémon que cumplen **todos** los filtros aplicados simultáneamente (filtrado AND acumulativo).

| Campo por elemento | Significado |
|---|---|
| `id` | ID nacional del Pokémon. |
| `name` | Nombre normalizado. |
| `generation` | Generación a la que pertenece (1–9). |
| `types` | Lista de tipos elementales. |
| `hp`, `attack`, `defense`, `speed` | Stats base individuales. |
| `base_exp` | Experiencia base otorgada al vencerlo. |
| `sprite_url` | URL del artwork oficial. |

> **Cómo actuar:** si el resultado devuelve 0 elementos, los filtros son > demasiado restrictivos. Reduce los valores mínimos o elimina algún filtro para ampliar la búsqueda.

---

## [4] EFECTIVIDAD DE COMBATE — `/pokemon/{identifier}/effectiveness`

```json
{
  "weaknesses_x4": [],
  "weaknesses": ["ground"],
  "resistances": ["electric", "flying", "steel"],
  "resistances_x025": [],
  "immunities": []
}
```

Indica cómo afectan los distintos tipos de ataque al Pokémon consultado,
basándose en su(s) tipo(s) elemental(es).

| Campo | Multiplicador de daño | Significado |
|---|---|---|
| `weaknesses_x4` | ×4 | Doble debilidad. Recibe el cuádruple del daño. Solo ocurre en Pokémon de tipo dual donde ambos tipos son débiles al mismo atacante. |
| `weaknesses` | ×2 | Debilidad simple. Recibe el doble del daño. **Evitar recibir estos ataques.** |
| `resistances` | ×0.5 | Resistencia simple. Recibe la mitad del daño. |
| `resistances_x025` | ×0.25 | Doble resistencia. Recibe un cuarto del daño. |
| `immunities` | ×0 | Inmunidad. No recibe ningún daño de ese tipo. |

> **Ejemplo Pikachu (eléctrico):** es débil a `ground` (tierra), resistente a `electric`, `flying` y `steel`. No tiene doble debilidad ni inmunidades. En combate, evitar enfrentarlo con movimientos de tipo tierra.

---

## [5–8] EQUIPOS POKÉMON — `/teams`

### Crear / Ver detalle

```json
{
  "id": "eba285df-3e7d-4bdd-ad4f-2b3a7d16dc95",
  "name": "Equipo Alpha",
  "members": [ ... ],
  "stats": {
    "total_hp": 360,
    "total_attack": 393,
    "total_defense": 374,
    "total_speed": 430,
    "avg_hp": 60.0,
    "avg_attack": 65.5,
    "avg_defense": 62.33,
    "avg_speed": 71.67,
    "type_coverage": ["fire", "flying", "grass", "poison"]
  },
  "created_at": "2026-07-03T03:01:42.300508+00:00"
}
```

| Campo | Significado |
|---|---|
| `id` | UUID único del equipo. Úsalo para consultar, actualizar o eliminar. |
| `name` | Nombre asignado al equipo. |
| `members` | Lista de hasta 6 Pokémon con sus stats individuales. |
| `stats.total_*` | Suma de la stat correspondiente entre todos los miembros del equipo. |
| `stats.avg_*` | Promedio de la stat entre todos los miembros. Permite comparar equipos de distinto tamaño. |
| `stats.type_coverage` | Unión de todos los tipos presentes en el equipo, ordenados alfabéticamente. |
| `created_at` | Fecha y hora de creación en formato ISO 8601 (UTC). |

### Cómo interpretar las estadísticas de equipo

- **`total_hp` alto** → el equipo aguanta más daño en general.
- **`avg_speed` alto** → el equipo tiende a actuar primero en combate.
- **`type_coverage` amplia** → el equipo puede atacar y defenderse contra más tipos. Un equipo con solo 1–2 tipos en `type_coverage` es estratégicamente vulnerable.

> **Alerta:** si `type_coverage` tiene menos de 3 tipos, el sistema de alertas automáticas lo marcará como equipo con poca cobertura al arrancar el CLI.

---

## [9] PROMEDIOS POR TIPO — `/analytics/average-by-type`

```json
{
  "type_name": "bug",
  "sample_size": 92,
  "avg_hp": 56.58,
  "avg_attack": 68.01,
  "avg_defense": 69.17,
  "avg_speed": 60.15
}
```

| Campo | Significado |
|---|---|
| `type_name` | Tipo elemental analizado. |
| `sample_size` | Número de Pokémon de ese tipo en el dataset (incluyendo duales). |
| `avg_hp` | HP promedio de todos los Pokémon de ese tipo. |
| `avg_attack` | Ataque promedio. |
| `avg_defense` | Defensa promedio. |
| `avg_speed` | Velocidad promedio. |

> **Nota:** un Pokémon de tipo dual (ej. Charizard es fuego/volador) cuenta una vez en cada tipo. Por eso `sample_size` no corresponde al número de Pokémon únicos de ese tipo.

> **Cómo usarlo:** compara `avg_attack` entre tipos para identificar qué tipo elemental tiende a ser más ofensivo, o `avg_hp` para identificar cuál es más resistente por naturaleza.

---

## [10] TOP-N POR MÉTRICA — `/analytics/top`

```json
{
  "id": 242,
  "name": "blissey",
  "types": ["normal"],
  "value": 255,
  "metric": "hp"
}
```

| Campo | Significado |
|---|---|
| `id` | ID del Pokémon en el ranking. |
| `name` | Nombre del Pokémon. |
| `types` | Tipos elementales. |
| `value` | Valor de la métrica consultada para ese Pokémon. |
| `metric` | Estadística por la que se ordenó el ranking (`hp`, `attack`, `defense`, `speed`, `base_exp`). |

> **Cómo leerlo:** el ranking está ordenado de mayor a menor. El primer elemento es el Pokémon con el valor más alto en la métrica elegida. Blissey lidera el ranking de HP con 255 puntos base.

---

## [11] DETECCIÓN DE ANOMALÍAS — `/analytics/anomalies`

```json
{
  "id": 289,
  "name": "slaking",
  "types": ["normal"],
  "stat_total": 510,
  "type_average": 279.75,
  "deviation": 3.07,
  "method": "stddev",
  "reason": "Stat total 510 está 3.07 desviaciones estándar por encima del promedio del tipo 'normal' (279.75)."
}
```

| Campo | Significado |
|---|---|
| `stat_total` | Suma de hp + attack + defense + speed del Pokémon. |
| `type_average` | Promedio del `stat_total` entre todos los Pokémon del mismo tipo primario. |
| `deviation` | Distancia en desviaciones estándar respecto a la media del tipo. Valor positivo = por encima, negativo = por debajo. |
| `method` | Método que detectó la anomalía (ver tabla abajo). |
| `reason` | Explicación en lenguaje natural de por qué se considera anómalo. |

### Métodos de detección

| `method` | Criterio | Cuándo aparece |
|---|---|---|
| `stddev` | El `stat_total` supera ±2 desviaciones estándar respecto a la media de su tipo. | Pokémon muy por encima o por debajo de lo normal **para su tipo**. |
| `percentile` | El `stat_total` está en el 5% superior o inferior del dataset global. | Pokémon extremos a nivel global, no detectados por `stddev`. |

### Cómo interpretar la `deviation`

| Rango de `deviation` | Interpretación |
|---|---|
| `> 3.0` | Anomalía muy pronunciada. El Pokémon es estadísticamente excepcional dentro de su tipo. |
| `2.0 – 3.0` | Anomalía moderada. Supera el umbral estándar (±2σ). |
| `0.0` | Detectado por percentil global, no por desviación de tipo. |
| `< 0` (negativo) | Por debajo de la media de su tipo (Pokémon inusualmente débil). |

> **Slaking con deviation 3.07:** tiene un stat_total de 510, cuando el promedio de los Pokémon de tipo normal es 279.75. Está 3 desviaciones estándar por encima — es  excepcionalmente fuerte para su tipo.

---
## [12–13] EXPORTACIÓN A CSV

Cuando la exportación es exitosa, el sistema imprime:

```
✅ CSV generado exitosamente en: C:\...\data\reports\filtro_pokemon.csv
```

El archivo CSV se guarda en la carpeta `data/reports/` del proyecto. Se puede abrir directamente con Excel, LibreOffice Calc o cualquier editor de texto.

| Archivo | Contenido |
|---|---|
| `filtro_pokemon.csv` | Resultado del último filtro aplicado. Una fila por Pokémon. |
| `top_n_pokemon.csv` | Resultado del último ranking Top-N generado. |

> **Nota:** cada exportación **sobreescribe** el archivo anterior del mismo tipo. Si quieres conservar un resultado, renombra el archivo antes de exportar uno nuevo.

---

## [14] GRÁFICO ASCII — STATS DE UN POKÉMON

```
📊 Stats de Mewtwo
------------------------------------------------------------
hp        | █████████████████████████████████ 106
attack    | ██████████████████████████████████ 110
defense   | ████████████████████████████ 90
speed     | ████████████████████████████████████████ 130
------------------------------------------------------------
```

Cada fila representa una estadística base del Pokémon consultado.

**Cómo leerlo:**
- La **longitud de la barra** es proporcional al valor más alto del Pokémon. La barra más larga siempre ocupa el ancho máximo (40 caracteres).
- El **número al final** es el valor base exacto de esa estadística.
- Comparando las barras entre sí puedes identificar de un vistazo el perfil del Pokémon: Mewtwo es más rápido (`speed: 130`) y más atacante (`attack: 110`) que defensivo (`defense: 90`).

> **Limitación:** el gráfico solo muestra hp, attack, defense y speed. Los stats `special-attack` y `special-defense` no se representan.

---

## [15] GRÁFICO ASCII — PROMEDIO POR TIPO

```
📊 Comparativa de 'avg_hp' por tipo elemental
------------------------------------------------------------
dragon    | ████████████████████████████████████████ 84.07
ice       | ██████████████████████████████████████ 80.08
fighting  | █████████████████████████████████████ 77.75
ground    | █████████████████████████████████████ 77.05
normal    | ████████████████████████████████████ 76.56
dark      | ████████████████████████████████████ 76.28
psychic   | ███████████████████████████████████ 73.76
steel     | ██████████████████████████████████ 70.95
flying    | █████████████████████████████████ 70.36
fire      | █████████████████████████████████ 69.94
water     | █████████████████████████████████ 69.6
rock      | █████████████████████████████████ 68.85
electric  | █████████████████████████████████ 68.68
fairy     | ████████████████████████████████ 67.23
grass     | ███████████████████████████████ 66.13
poison    | ███████████████████████████████ 66.05
ghost     | ███████████████████████████████ 65.71
bug       | ███████████████████████████ 56.58
------------------------------------------------------------
```

**Cómo leerlo:**
- Los tipos aparecen **ordenados de mayor a menor** según la métrica elegida.
- La barra más larga corresponde al tipo con el valor más alto y ocupa
  el ancho máximo (40 caracteres). El resto son proporcionales.
- El número al final es el promedio exacto de la métrica para ese tipo.

**Métricas disponibles:**

| Métrica | Qué compara |
|---|---|
| `avg_hp` | Cuál tipo elemental tiene Pokémon más resistentes en promedio. |
| `avg_attack` | Cuál tipo elemental es más ofensivo en promedio. |
| `avg_defense` | Cuál tipo elemental es más defensivo en promedio. |
| `avg_speed` | Cuál tipo elemental actúa antes en combate en promedio. |

> **Ejemplo:** el tipo `dragon` lidera en HP promedio (84.07) y `bug` es el que tiene menor HP medio (56.58) entre los 18 tipos.

---
## [16] PREDICCIONES — STATS POR TIPO

```
✅ [HTTP 200] ESTRUCTURA DE DATOS CAPTURADA EXITOSAMENTE:

{
  "primary_type": "grass",
  "secondary_type": null,
  "predicted_hp": 67.67,
  "predicted_attack": 81.69,
  "predicted_defense": 75.5,
  "predicted_speed": 60.26,
  "sample_size": 127,
  "generations_used": [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9
  ],
  "window_size": 3,
  "group_avg_hp": 66.13,
  "group_avg_attack": 74.76,
  "group_avg_defense": 71.71,
  "group_avg_speed": 59.69,
  "description": "Predicción basada en media móvil simple (ventana=3) sobre 9 generaciones históricas para tipo 'grass'. Muestra: 127 Pokémon únicos."
}

```

| Campo | Significado |
|---|---|
| `primary_type` | Tipo elemental principal sobre el que se calculó la predicción. |
| `secondary_type` | Tipo secundario aplicado como filtro adicional. `null` si no se especificó. |
| `predicted_hp` | HP predicho para un Pokémon de ese tipo basado en la tendencia histórica. |
| `predicted_attack` | Ataque predicho. |
| `predicted_defense` | Defensa predicha. |
| `predicted_speed` | Velocidad predicha. |
| `sample_size` | Número de Pokémon únicos usados en el cálculo (los de ese tipo en el dataset). |
| `generations_used` | Generaciones con datos disponibles para ese tipo. La predicción se basa en su tendencia. |
| `window_size` | Tamaño de la ventana de la media móvil simple. Siempre entre 2 y 3. |
| `group_avg_hp` | HP promedio histórico global de todos los Pokémon de ese tipo (sin media móvil). |
| `group_avg_attack` | Ataque promedio histórico global. |
| `group_avg_defense` | Defensa promedio histórica global. |
| `group_avg_speed` | Velocidad promedio histórica global. |
| `description` | Resumen textual del cálculo: ventana usada, generaciones y muestra. |

### Cómo leer la predicción

El algoritmo funciona en tres pasos:

1. **Filtra** todos los Pokémon del tipo indicado y calcula el promedio de cada stat por generación. Para `grass` con 9 generaciones disponibles obtiene 9 promedios por stat.

2. **Aplica la media móvil simple (SMA)** con ventana de 3: toma los promedios de cada grupo de 3 generaciones consecutivas y los promedia. Esto suaviza variaciones puntuales y refleja la tendencia reciente.

3. **El último valor** de la SMA es la predicción — representa cómo se espera que sea un Pokémon de ese tipo basándose en las últimas generaciones.

### Diferencia entre `predicted_*` y `group_avg_*`

| | `group_avg_*` | `predicted_*` |
|---|---|---|
| **Qué es** | Promedio histórico total | Predicción por SMA |
| **Cómo se calcula** | Media de todos los Pokémon del tipo | Media móvil sobre promedios por generación |
| **Para qué sirve** | Ver el perfil histórico del tipo | Estimar las stats de un Pokémon nuevo de ese tipo |

> **Ejemplo grass:** el `group_avg_attack` es 74.76 (promedio histórico), pero `predicted_attack` es 81.69, lo que indica que los Pokémon de tipo grass de las últimas generaciones tienden a ser más ofensivos que el promedio histórico global.

### Parámetros disponibles

| Parámetro | Valores válidos | Ejemplo |
|---|---|---|
| `primary_type` | Cualquiera de los 18 tipos en minúsculas | `fire`, `water`, `grass` |
| `secondary_type` | Tipo secundario opcional | `--secondary flying` |

> **Consejo:** si la predicción falla por pocas generaciones, prueba sin tipo secundario. Los tipos con más datos históricos son `water`, `normal`, `grass`, `psychic` y `fire`.
---
## [17] SIMULACION — GENERA POKEMON ALEATORIO

JSON de respuesta:
```
✅ [HTTP 200] ESTRUCTURA DE DATOS CAPTURADA EXITOSAMENTE:

{
  "csv_path": "C:\\Users\\ASUS\\OneDrive\\Documentos\\AB_Programming_&_Coding_Pokedex\\Pokedex\\data\\pokemon_sinteticos.csv",
  "generated_count": 1,
  "total_accumulated": 1,
  "pokemon_type": "water",
  "generation": 1,
  "message": "Se generaron 1 Pokémon sintéticos de tipo 'water' (gen 1) y se añadieron al dataset acumulativo. Total en el fichero: 1 registros."
}

```
Y el CSV generado:
```
id,name,types,generation,hp,attack,defense,speed,is_synthetic,generated_at
SIM-water-gen1-20260703031608-0001,fakemon_water_20260703031608_0001,water,1,85,49,110,58,True,20260703031608

```

| Campo JSON | Significado |
|---|---|
| `csv_path` | Ruta absoluta del archivo CSV donde se acumulan los Pokémon sintéticos. |
| `generated_count` | Cantidad de Pokémon generados en esta ejecución. |
| `total_accumulated` | Total de registros en el CSV incluyendo ejecuciones anteriores (acumulativo). |
| `pokemon_type` | Tipo elemental asignado a los Pokémon generados. |
| `generation` | Generación a la que pertenecen los Pokémon generados. |
| `message` | Resumen textual de la operación. |

### Columnas del CSV generado

| Columna | Significado |
|---|---|
| `id` | Identificador sintético con formato `SIM-{tipo}-gen{N}-{timestamp}-{índice}`. Permite rastrear el origen de cada registro. |
| `name` | Nombre ficticio con formato `fakemon_{tipo}_{timestamp}_{índice}`. |
| `types` | Tipo elemental del Pokémon generado. |
| `generation` | Generación asignada. |
| `hp` | HP generado aleatoriamente usando la distribución normal del tipo real (media ± desviación estándar). |
| `attack` | Ataque generado con la misma distribución estadística del tipo. |
| `defense` | Defensa generada con la misma distribución estadística del tipo. |
| `speed` | Velocidad generada con la misma distribución estadística del tipo. |
| `is_synthetic` | Siempre `True`. Permite filtrar registros sintéticos de datos reales. |
| `generated_at` | Timestamp de generación en formato `YYYYMMDDHHMMSS`. |

### Cómo se generan las stats

El simulador **no genera stats aleatorias sin criterio**. Para cada stat calcula la media (μ) y desviación estándar (σ) de los Pokémon reales de ese tipo en el dataset, y muestrea usando una distribución normal: stat_generado = Normal(μ_tipo, σ_tipo)

Esto garantiza que los Pokémon sintéticos sean **estadísticamente realistas** para el tipo asignado. Un `fakemon_water` tendrá stats similares a los Pokémon de agua reales, no valores arbitrarios. Los valores se limitan al rango válido [1, 255].

### Comportamiento acumulativo

El CSV **no se sobreescribe** entre ejecuciones — cada simulación añade filas al final del archivo existente. El campo `total_accumulated` refleja el total real de registros en el fichero tras la operación.

> **Consejo:** si quieres empezar desde cero, elimina manualmente el archivo `data/pokemon_sinteticos.csv` antes de la siguiente simulación.

### Parámetros disponibles

| Parámetro | Rango válido | Default | Ejemplo |
|---|---|---|---|
| `n` | 1 – 1000 | 10 | `--n 50` |
| `pokemon_type` | 18 tipos en minúsculas | `normal` | `--type water` |
| `generation` | 1 – 9 | 1 | `--gen 3` |
| `seed` | Cualquier entero | `null` | `--seed 42` |

> **Sobre la semilla (`seed`):** si usas la misma semilla con los mismos parámetros, obtendrás exactamente los mismos valores de stats. Útil para reproducir experimentos o comparar resultados.
---
## ALERTAS AUTOMÁTICAS AL INICIAR EL CLI

Al ejecutar `python cli.py` sin argumentos, el sistema evalúa
automáticamente tres condiciones antes de mostrar el menú:

### 🌟 Pokémon del día
```
🌟 Pokemon del día: Ditto (#132) — ¡no te olvides de revisarlo!
```
Se selecciona un Pokémon diferente cada día de forma determinista
(misma semilla basada en la fecha). Es decorativo — no requiere acción.

### ⚠️ Anomalías detectadas
```
⚠️ Se detectaron 107 Pokemon con stats anómalas en el dataset.
   Revisa la opción de análisis de anomalías.
```
Indica cuántos Pokémon están fuera de los rangos estadísticos normales.

**Cómo actuar:** si el número es inusualmente alto (>150) o bajo (<10),
puede indicar que el dataset local está desactualizado o incompleto.
Ejecuta el script ETL para regenerarlo:
```bash
python -m backend.app.data.scripts.dataset_generator
```

### 🛡️ Equipos con poca cobertura de tipos
```
🛡️ Estos equipos tienen poca variedad de tipos y son vulnerables
   estratégicamente: Equipo Fuego.
```
Se activa cuando un equipo guardado tiene menos de 3 tipos distintos
en su `type_coverage`.

**Cómo actuar:** edita el equipo desde la opción `[8]` del menú o con:
```bash
python cli.py team update <team_id>
```
Añade Pokémon de tipos distintos para ampliar la cobertura y reducir
las vulnerabilidades estratégicas.

### ✅ Sin alertas
```
✅ No hay alertas relevantes por el momento.
```
Todo está en orden. El dataset está completo y los equipos son variados.

---

## CÓDIGOS DE ESTADO HTTP — REFERENCIA RÁPIDA

| Código | Significado | Acción recomendada |
|---|---|---|
| `200 OK` | Petición exitosa. | Leer e interpretar los datos devueltos. |
| `201 Created` | Recurso creado correctamente (equipos). | El recurso ya está guardado. |
| `204 No Content` | Eliminación exitosa. | El recurso fue borrado; no hay datos que mostrar. |
| `404 Not Found` | El Pokémon o recurso no existe. | Verificar el nombre o ID. Probar con otro identificador. |
| `422 Unprocessable Entity` | Parámetro inválido (ej. generación "PRIMERA"). | Revisar el formato del parámetro. Usar valores numéricos donde corresponda. |
| `500 Internal Server Error` | Error inesperado en el servidor. | Revisar que uvicorn esté corriendo. Consultar la sección FAQ. |