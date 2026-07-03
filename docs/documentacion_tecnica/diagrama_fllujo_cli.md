# FLUJO DE BUSQUEDA DEL CLI

## OPCIONES PRINCIPALES

- "1": menu_detalle_pokemon,
- "2": menu_arbol_evolutivo,
- "3": menu_filtro_analitico,
- "4": menu_efectividad_combate,
- "5": menu_crear_equipo,
- "6": menu_ver_equipo,
- "7": menu_ver_equipo,
- "8": menu_eliminar_equipo,
- "9": menu_promedio_por_tipo,
- "10": menu_top_n,
- "11": menu_anomalias,
- "12": menu_exportar_filtro_csv,
- "13": menu_exportar_top_csv,
- "14": menu_grafico_pokemon_individual,
- "15": menu_grafico_promedio_tipo,
- "16": menu_predicciones,
- "17": menu_simulaciones,
- "0": Volver

## SUBOPCIONES
Inicialmente, por practicidad se muestran las dos primeras respuestas de la busqueda, con excepción de las opciones 12, 13, 14, 15, 17 que exportan un csv
- "1": Ver más resultados,
- "2": Ver TODOS los resultados,
- "3": Ver un resultado específico

## FLUJO DE USO DE CLI INTERACTIVA
1. Levantamiento del servidor uvicorn, con el siguiente comando: uvicorn backend.main:app --reload.
2. Ejecución del CLI en la raíz, con el siguiente comando: python cli.py.
3. Inicio con alertas automáticas.
4. Presentación del menú interactivo con opciones y sus números.
5. Selección de la opción deseada de acuerdo a las opciones disponibles.
6. En caso de existir más opciones de las presentadas, seleccionar subopciones.
7. Datos obtenidos, o salir del menú.

## VISTAS DEL MENU INTERACTIVO
![ALERTAS AUTOMATICAS](/docs//documentacion_tecnica/images/image.png)
![MENU INTERACTIVO CON OPCIONES](/docs//documentacion_tecnica/images/image-1.png)
![SUBMENU INTERACTIVO](/docs//documentacion_tecnica/images/image-2.png)