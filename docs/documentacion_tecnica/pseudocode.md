INICIO
CARGAR pagina_principal:

    MOSTRAR columna_izquierda:
        panel_filtros (tipo, generación, hp, attack, defense, speed, base_exp)
        enlaces_navegacion (Galería, Constructor de Equipos, Comparador)

    MOSTRAR area_principal:
        barra_busqueda
        galeria_pokemon ← LLAMAR api_get_filtered(sin_filtros)
                         MOSTRAR primeros 150 resultados como tarjetas

# ── Búsqueda individual ────────────────────────────────────────────────

SI usuario escribe en barra_busqueda:
    identifier ← entrada del usuario (nombre o ID)
    LLAMAR api_get_pokemon(identifier)
    NAVEGAR a pagina_detalle(identifier)

# ── Página de detalle ──────────────────────────────────────────────────

EN pagina_detalle(identifier):

    pokemon     ← LLAMAR api_get_pokemon(identifier)
    evolucion   ← LLAMAR api_get_evolution(identifier)
    efectividad ← LLAMAR api_get_effectiveness(identifier)

    MOSTRAR en tres columnas:

        COLUMNA 1:
            nombre, id
            sprite_frontal
            sprite_shiny (toggle)
            flavor_text
            tipos (badges)
            altura, peso, base_exp

            SECCIÓN cadena_evolutiva:
                PARA CADA nodo EN evolucion:
                    MOSTRAR sprite + nombre + requisito_evolucion
                    SI usuario hace clic en sprite:
                        NAVEGAR a pagina_detalle(nodo.name)

            SECCIÓN carta_pokemon:
                MOSTRAR sprite + stats + tipos en formato carta coleccionable

        COLUMNA 2:
            grafico_radar(hp, attack, defense, speed, base_exp)

        COLUMNA 3:
            MOSTRAR relaciones_daño desde efectividad:
                weaknesses_x4   → rojo intenso
                weaknesses      → rojo
                resistances     → verde
                resistances_x025→ verde intenso
                immunities      → gris

    BOTÓN "Volver a galería":
        NAVEGAR a pagina_principal

# ── Filtros en galería ─────────────────────────────────────────────────

SI usuario aplica filtros:
    params ← {tipo, generacion, min_hp, min_attack, min_defense,
              min_speed, min_base_exp}
    resultados ← LLAMAR api_get_filtered(params)
    ACTUALIZAR galeria_pokemon con resultados

# ── Constructor de equipos (ACTUALMENTE UNICAMENTE EN CLI)─────────────────────────────────────────────

EN pagina_constructor_equipos:

    MOSTRAR barra_busqueda + panel_filtros
    equipo_actual ← lista vacía (máximo 6)

    SI usuario busca y selecciona un Pokemon:
        SI longitud(equipo_actual) < 6:
            AGREGAR pokemon a equipo_actual
            ACTUALIZAR panel_equipo:
                stats_agregadas (suma y promedio de hp, attack, defense, speed)
                cobertura_tipos (union de todos los tipos del equipo)
        SINO:
            MOSTRAR advertencia "Equipo completo (máximo 6 Pokemon)"

    SI usuario da nombre al equipo y pulsa guardar:
        LLAMAR api_create_team(nombre, ids_pokemon)
        MOSTRAR confirmación

# ── Comparador de Pokemon (FUTURO)──────────────────────────────────────────────

EN pagina_comparador:

    MOSTRAR dos barras de búsqueda (Pokemon A vs Pokemon B)

    SI ambos Pokemon seleccionados:
        pokemon_a ← LLAMAR api_get_pokemon(identifier_a)
        pokemon_b ← LLAMAR api_get_pokemon(identifier_b)

        MOSTRAR tabla_comparativa:
            PARA CADA stat EN [hp, attack, defense, speed, base_exp]:
                RESALTAR el valor mayor entre pokemon_a y pokemon_b

        MOSTRAR grafico_radar_comparativo:
            curva_a (azul) vs curva_b (rojo) sobre los mismos ejes
FIN

# ALGORITMO DE DETECCION DE ANOMALIAS
# ── Paso 1: calcular stat_total para cada Pokemon ──────────────────────

PARA CADA pokemon EN dataset:
    pokemon.stat_total ← pokemon.hp + pokemon.attack
                       + pokemon.defense + pokemon.speed

anomalias ← diccionario vacío  # clave: pokemon.id

# ── Paso 2: detección por desviación estándar (por tipo) ──────────────

grupos ← agrupar dataset por tipo_primario (types[0])

PARA CADA (tipo, pokemon_del_tipo) EN grupos:

    SI longitud(pokemon_del_tipo) < 2:
        CONTINUAR  # no se puede calcular desviación con un solo elemento

    totales ← [p.stat_total PARA p EN pokemon_del_tipo]
    media   ← promedio(totales)
    std     ← desviacion_estandar(totales)

    SI std == 0:
        CONTINUAR  # todos tienen el mismo stat_total, no hay anomalía

    PARA CADA pokemon EN pokemon_del_tipo:

        desviacion ← (pokemon.stat_total - media) / std

        SI valor_absoluto(desviacion) >= umbral_desviacion:

            direccion ← "por encima" SI desviacion > 0 SINO "por debajo"

            anomalias[pokemon.id] ← AnomalyEntry(
                id          = pokemon.id,
                name        = pokemon.name,
                types       = pokemon.types,
                stat_total  = pokemon.stat_total,
                type_average= redondear(media, 2),
                deviation   = redondear(desviacion, 2),
                method      = "stddev",
                reason      = "Stat total {stat_total} está {|desviacion|} "
                              "desviaciones estándar {direccion} de la media "
                              "del tipo '{tipo}' ({media})"
            )

# ── Paso 3: detección por percentil (global) ──────────────────────────

todos_los_totales ← ordenar([p.stat_total PARA p EN dataset])
n                 ← longitud(todos_los_totales)

indice_inferior ← max(0, entero(n * umbral_percentil) - 1)
indice_superior ← min(n - 1, entero(n * (1 - umbral_percentil)))

corte_inferior  ← todos_los_totales[indice_inferior]
corte_superior  ← todos_los_totales[indice_superior]
media_global    ← promedio(todos_los_totales)

PARA CADA pokemon EN dataset:

    SI pokemon.id YA ESTÁ EN anomalias:
        CONTINUAR  # ya detectado por stddev, no duplicar

    SI pokemon.stat_total <= corte_inferior
    O  pokemon.stat_total >= corte_superior:

        etiqueta ← "inferior al {umbral_percentil*100}%"
                    SI pokemon.stat_total <= corte_inferior
                    SINO "superior al {(1-umbral_percentil)*100}%"

        anomalias[pokemon.id] ← AnomalyEntry(
            id          = pokemon.id,
            name        = pokemon.name,
            types       = pokemon.types,
            stat_total  = pokemon.stat_total,
            type_average= redondear(media_global, 2),
            deviation   = 0.0,
            method      = "percentile",
            reason      = "Stat total {stat_total} en percentil {etiqueta}"
        )

# ── Paso 4: ordenar por desviación absoluta descendente ───────────────

resultado ← ordenar(
    valores(anomalias),
    clave = |entry.deviation|,
    orden = descendente
)

RETORNAR resultado

# ALGORITMO DE PREDICCIONES
# ── Paso 1: normalizar entrada ─────────────────────────────────────────

tipo_primario ← tipo_primario.minúsculas().strip()

# ── Paso 2: filtrar por tipo primario ─────────────────────────────────

candidatos ← [p PARA p EN dataset SI tipo_primario EN p.types]

SI candidatos está vacío:
    LANZAR ValueError("No se encontraron Pokemon de tipo '{tipo_primario}'")

# ── Paso 3: filtrar por tipo secundario (opcional) ────────────────────

SI tipo_secundario NO ES nulo:
    tipo_secundario ← tipo_secundario.minúsculas().strip()
    candidatos ← [p PARA p EN candidatos SI tipo_secundario EN p.types]

    SI candidatos está vacío:
        LANZAR ValueError(
            "No hay Pokemon de tipo '{tipo_primario}'/'{tipo_secundario}'"
        )

# ── Paso 4: calcular promedio de stats por generación ─────────────────

grupos_por_gen ← agrupar candidatos por generation

stats_por_gen ← diccionario ordenado por generación:
    PARA CADA (gen, pokemon_de_gen) EN grupos_por_gen:
        stats_por_gen[gen] ← {
            "hp":      promedio([p.hp      PARA p EN pokemon_de_gen]),
            "attack":  promedio([p.attack  PARA p EN pokemon_de_gen]),
            "defense": promedio([p.defense PARA p EN pokemon_de_gen]),
            "speed":   promedio([p.speed   PARA p EN pokemon_de_gen]),
        }

SI longitud(stats_por_gen) < 2:
    LANZAR ValueError(
        "Solo hay {longitud(stats_por_gen)} generación(es). "
        "Se necesitan al menos 2 para calcular la media móvil."
    )

# ── Paso 5: aplicar media móvil simple (SMA) ──────────────────────────
#
# La SMA de ventana W sobre una serie [x1, x2, ..., xN] produce:
#   SMA[i] = promedio(x[i-W+1], ..., x[i])   para i >= W-1
#
# Solo los últimos (N - W + 1) valores son válidos (no nulos).
# Usamos el último valor válido como predicción.

ventana ← min(VENTANA_MAXIMA, longitud(stats_por_gen))
series  ← lista de valores de stats_por_gen (ordenados por generación)

sma ← lista vacía
PARA i DESDE ventana-1 HASTA longitud(series)-1:
    ventana_actual ← series[i-ventana+1 .. i]   # slice de W elementos
    sma.agregar({
        stat: promedio([v[stat] PARA v EN ventana_actual])
        PARA stat EN [hp, attack, defense, speed]
    })

prediccion ← último elemento de sma   # valor más reciente de la SMA

# ── Paso 6: calcular métricas de contexto ─────────────────────────────

promedio_grupo ← {
    stat: promedio([p[stat] PARA p EN candidatos])
    PARA stat EN [hp, attack, defense, speed]
}

ids_unicos       ← conjunto({p.id PARA p EN candidatos})
generaciones     ← lista ordenada(claves de stats_por_gen)

# ── Paso 7: construir y retornar resultado ────────────────────────────

RETORNAR PredictionResult(
    primary_type     = tipo_primario,
    secondary_type   = tipo_secundario,
    predicted_hp     = prediccion["hp"],
    predicted_attack = prediccion["attack"],
    predicted_defense= prediccion["defense"],
    predicted_speed  = prediccion["speed"],
    sample_size      = longitud(ids_unicos),
    generations_used = generaciones,
    window_size      = ventana,
    group_avg_hp     = promedio_grupo["hp"],
    group_avg_attack = promedio_grupo["attack"],
    group_avg_defense= promedio_grupo["defense"],
    group_avg_speed  = promedio_grupo["speed"],
    description      = "Predicción basada en SMA (ventana={ventana}) "
                       "sobre {longitud(generaciones)} generaciones "
                       "para tipo '{tipo_primario}'. "
                       "Muestra: {longitud(ids_unicos)} Pokemon únicos."
)