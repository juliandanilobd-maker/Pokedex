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

# Release v0.1.0

## Epic 1 - Arquitectura Base

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

### Historia 1.3 - Configurar sistema de dependencias

### Prioridad: ALTA.
### Estado: EN CURSO.

#### Descripción
Como desarrollador, necesito un sistema de dependencias para desacoplar servicios y facilitar testing

### Criterios de aceptación
- [] Uso de dependency injection en FastAPI.
- [] Servicios inyectables (no instanciados globalmente).
- [x] Separacion clara entre clientes, servicios y endpoints.
- [x] Preparado para mocking test.

## Epic 2 - Integración PokeAPI

## Objetivo
Permitir comunicación estable y estructurada con la API externa de Pokemon.

### Historia 2.1 - Crear cliente HTTP

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Como sistema, necesito un cliente HTTP que permita consumir PokeAPI de forma centralizada.

### Criterios de aceptación
- [x] Cliente HTTP único para PokeAPI.
- [x] Manejo de requests GET.
- [x] Timeout y control básico de errores.
- [x] No existe acceso directo a requests fuera del cliente.

### Historia 2.2 - Normalizar identificadores

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción

Como sistema, necesito transformar datos crudos de PokeAPI en modelos internos consistentes.

### Criterios de aceptación
- [x] Parsers implementados para cada Pokemon.
- [x] Datos externos convertidos a modelos internos.
- [x] Campos relevantes normalizados.
- [x] Evitar exposicón directa del JSON externo.

### Historia 2.3 - Manejo de errores

### Prioridad: ALTA.
### Estado: EN CURSO.

#### Descripción

Como sistema, necesito manejar errores de red o API externa para evitar fallos en cascada.

### Criterios de aceptación
- [x] Manejo de Timeouts, 404 y errores 5xx.
- [x] Respuestas controladas al backend.
- [] No se rompe el backend por fallos de PokeAPI

---

## Epic 3 - Cache


## Objetivo
Reducir las llamadas a PokeAPI mediante almacenamiento local eficiente.

### Historia 3.1 - Implementar SQLite

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción

Como sistema, necesito implementar un cache persistente, para reducir las llamadas repetidas a la PokeAPI.

### Criterios de aceptación
- [x] SQLite configurado como almacenamiento.
- [x] Guardado de respuestas de API.
- [x] Recuperación de datos cacheados.
- [x] Persistencia de ejecuciones.

### Historia 3.2 - Integrar cache-first

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

## Epic 4 - Calidad del Software

## Objetivo

Garantizar la estabilidad del backend mediante tests y CI.

### Historia 4.1 - Crear tests unitarios

### Prioridad: ALTA.
### Estado: EN CURSO.

#### Descripción

Como desarrollador, necesito tests unitarios para asegurar el correcto funcionamiento del backend.

### Criterios de aceptación

- [x] Tests para servicios.
- [x] Tests para cliente. 
- [x] Tests para cache.
- [x] Tests para parsers.
- [x] Uso de pytest.
- [] Tests independientes del entorno real.

### Historia 4.2 - Configurar CI con Github Actions

### Prioridad: ALTA.
### Estado: EN CURSO.

#### Descripción

Como desarrollador, necesito automatizar la ejecución de tests en cada push

### Criterios de aceptación
- [x] Worflow en Github actions.
- [x] Ejecución automática de tests.
- [x] Fail si tests no pasan.
- [] Integración con rama develop y main.
