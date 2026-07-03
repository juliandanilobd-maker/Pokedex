# REGISTRO DE CONVENCIONES DE CODIGO
Para esta aplicación se usaron las convenciones de código PEP8

## NORMAS DE NOMBRADO
1. Variables y funciones: snake_case.
2. Clases: PascalCase.
3. Constantes: UPPER_SNAKE_CASE.
4. Endpoints usan el mismo nombre del servicio que orquestan.
5. Parámetros de entrada se normalizan siempre con la función _normalize_identifier.

## ESTILO DE CODIGO
1. Uso de normas PEP8:
    -   Máximo 88 caracteres por línea.
    -   Dos líneas en blanco entre clases o funciones de nivel superior, una línea entre métodos de una clase.
2. Uso de docstrings con descripción de Args y Returns.
3. Uso de Type Hints en todas las funciones.
4. Imports organizados en bloques:
    -   Primero stdlib.
    -   Segundo librerías de terceros.
    -   Tercero imports internos.
5. Comentarios en líneas con lógica compleja.

## ESTRUCTURA DEL PROYECTO
- api/ contiene las rutas que orquestan las llamadas a los servicios.
- config/ contiene las instancias globales de configuración y las variables de entorno.
- clients/ hace peticiones HTTP, no contiene lógica.
- services/ contiene la lógica de negocio, no hace peticiones HTTP.
- parsers/ transforma datos externos al modelo interno.
- models/ define las estructuras de los diferentes datos obtenidos.
- dependencies/ ensambla servicios.

## PATRONES DE PROGRAMACIóN
- Inyección de dependencias en todos los endpoints usando Depends() de FastAPI.
- Funciones async en todas las llamadas a PokeAPI.
- Excepciones personalizadas con mensajes orientativos para encontrar el error.
- Valores por defecto seguros, en caso de fallas al momento de obtener datos solicitados, se usa un fallback seguro.
- Dataset loader como parametro inyectado, facilitando el testing en los servicios Analyzer, Predictor, Team y Simulator.
- Programación Orientada a objetos.
