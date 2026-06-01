# Roadmap - Pokedex
## Visión del Proyecto

Pokedex es una aplicación web desarrollada sobre una arquitectura modular por capas que permite consultar información de Pokémon utilizando PokeAPI como fuente principal de datos.

El desarrollo se organiza mediante versiones incrementales, donde cada release agrega funcionalidades específicas y consolida la calidad del software mediante pruebas automatizadas y documentación.

---
# Versión 0.1.0 - Backend Foundation
## Objetivo

Construir un backend funcional y testeado capaz de consultar información Pokémon desde PokeAPI.

---
## Funcionalidades
### Arquitectura
- Arquitectura modular por capas.
- Separación de responsabilidades.
- Sistema de dependencias.
### Backend
- FastAPI configurado.
- Endpoint Health Check.
- Cliente HTTP para PokeAPI.
- Parsers de datos.
- Modelos internos.
### Cache
- Cache persistente SQLite.
- Estrategia Cache First.
### Calidad
- Tests unitarios.
- GitHub Actions para ejecución automática de pruebas.
### Entregables
- Backend funcional.
- Cobertura de pruebas inicial.
- Documentación técnica base.

---
# Versión 0.2.0 - Search & Filtering
## Objetivo

Optimizar consultas mediante un sistema local de búsqueda y filtrado.

---
## Funcionalidades
### Dataset Local
- Script ETL.
- Dataset JSON generado automáticamente.
### Filtros
- Filtro por tipo.
- Filtro por generación.
- Filtro por HP.
- Filtro por ataque.
- Filtro por defensa.
- Filtro por experiencia base.
- Filtro por velocidad.
### Backend
- Endpoint de filtrado.
### Entregables
- Sistema de filtros operativo.
- Reducción de llamadas a PokeAPI.

---
# Versión 0.3.0 - Evolution & Battle Logic
## Objetivo

Incorporar información estratégica y evolutiva.

---
## Funcionalidades
### Evoluciones
- Endpoint de evolución.
- Parser de evoluciones.
- Árbol evolutivo.
### Sistema de Tipos
- Debilidades.
- Resistencias.
- Inmunidades.
- Multiplicadores de daño.
### Entregables
- Motor de relaciones de combate.
- Sistema evolutivo completo.

---
# Versión 0.4.0 - Frontend MVP
## Objetivo

Crear una interfaz gráfica funcional para consumir el backend.

---
## Funcionalidades
### Streamlit
- Página principal.
- Búsqueda de Pokémon.
- Vista detallada.
### Integración
- Backend Client.
- Manejo de errores visuales.
### Entregables
- Primera interfaz de usuario funcional.

---
# Versión 0.5.0 - Advanced UI
## Objetivo

Mejorar la experiencia visual del usuario.

---
## Funcionalidades
### Componentes
- Pokémon Card.
- Radar Chart.
- Evolution Chain.
- Combat Effectiveness.
### Experiencia
- Pokémon del día.
- Pokémon aleatorios.
- Mejoras visuales.
### Entregables
- Interfaz enriquecida.

---
# Versión 1.0.0 - Stable Release
## Objetivo

Publicar una versión estable y completa del proyecto.

---
## Funcionalidades
### Backend
- Cache.
- Filtros.
- Evoluciones.
- Relaciones de combate.
### Frontend
- Navegación multipágina.
- Componentes reutilizables.
- Diseño consolidado.
### Calidad
- Tests automatizados.
- CI/CD completo.
- Documentación final.
### Entregables
- Release estable.
- Proyecto listo para portafolio.
- Base para futuras extensiones.

---
# Futuras versiones
## Versión 1.1.0
Comparador de Pokémon.
## Versión 1.2.0
Constructor de equipos.
## Versión 2.0.0
Migración a React + TypeScript.
## Versión 3.0.0
Sistema de usuarios.
Favoritos.
Base de datos persistente.
## Versión 4.0.0
Recomendaciones mediante IA.
Simulador de combate.