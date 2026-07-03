

## MODO STREAMLIT (Interfaz Web)

### Instalación e inicio

```bash
streamlit run frontend/app.py
```

El navegador se abrirá automáticamente en `http://localhost:8501`.

---

### 1. Landing Page

![LANDING PAGE](/docs/documentacion_usuario/images/image.png)

Al iniciar el servidor llegarás a la página principal. En la barra lateral derecha encontrarás la navegación entre las distintas secciones del sistema.

![BARRA LATERAL](/docs/documentacion_usuario/images/image-1.png)

---

### 2. Búsqueda por Filtros

![BUSQUEDA POR FILTROS](/docs/documentacion_usuario/images/image-2.png)

Selecciona **Búsqueda por Filtros** en la barra lateral. Aparecerá el panel de parámetros de búsqueda:

![PARAMETROS DE FILTRO](/docs/documentacion_usuario/images/image-3.png)

Puedes combinar uno o varios filtros simultáneamente. Todos son opcionales — deja vacío cualquier campo que no quieras restringir.

| Filtro | Valores válidos | Ejemplo |
|---|---|---|
| Tipo elemental | Cualquiera de los 18 tipos | `water`, `fire`, `grass` |
| Generación | 1 a 9 | `2` |
| HP mínimo | Entero positivo | `50` |
| Ataque mínimo | Entero positivo | `80` |
| Defensa mínima | Entero positivo | `70` |
| Velocidad mínima | Entero positivo | `90` |
| Experiencia base mínima | Entero positivo | `200` |

![BUSQUEDA](/docs/documentacion_usuario/images/image-4.png)

Los resultados se muestran como galería de tarjetas. Haz clic en cualquier tarjeta para ver el detalle completo del Pokémon.

---

### 3. Búsqueda Individual

![BUSQUEDA INDIVIDUAL](/docs/documentacion_usuario/images/image-5.png)

Selecciona **Búsqueda Individual**. Encontrarás el **Pokémon del día** como sugerencia (cambia cada día automáticamente), o puedes buscar directamente por nombre o ID en la barra de búsqueda.

![VISTA AL DETALLE](/docs/documentacion_usuario/images/image-6.png)

La vista de detalle incluye:
- Nombre, ID, tipos, altura, peso y experiencia base
- Stats completas con gráfico de radar
- Descripción de la Pokédex en español
- Habilidades disponibles
- Sprites normal y shiny
- Relaciones de efectividad de combate
![CADENA EVOLUTIVA](/docs/documentacion_usuario/images/image-7.png)

La cadena evolutiva muestra todos los eslabones con los **requisitos para evolucionar** (nivel, objeto, felicidad, etc.). Haz clic en cualquier sprite para navegar al detalle de esa evolución.

![CARTA COLECCIONABLE](/docs/documentacion_usuario/images/image-8.png)

Al final de la página encontrarás la **carta coleccionable** del Pokémon, con su artwork oficial y sus estadísticas principales en formato de tarjeta.

---

## MODO CLI (Terminal)

El CLI tiene dos modos de uso: **interactivo** (con menús) y **directo** (con comandos).

### Inicio

```bash
python cli.py
```

---

### Modo interactivo

Al ejecutar `python cli.py` sin argumentos, primero verás las **alertas automáticas**:

![ALERTAS](/docs/documentacion_usuario/images/image-9.png)

Las alertas informan sobre:
- 🌟 El Pokémon del día
- ⚠️ Anomalías detectadas en el dataset
- 🛡️ Equipos con poca cobertura de tipos
Presiona **ENTER** para continuar al menú principal:

![ENTER](/docs/documentacion_usuario/images/image-10.png)

![MENU INTERACTIVO](/docs/documentacion_usuario/images/image-11.png)

Escribe el número de la opción que desees y presiona ENTER.

> **Campos opcionales:** en módulos con parámetros opcionales (filtros, predicción, simulación), no es necesario completar todos los campos. Presiona ENTER en blanco para omitir ese parámetro y usar el valor por defecto.

![FILTROS](/docs/documentacion_usuario/images/image-13.png)

Para búsquedas que devuelven más de 2 resultados, se desplegará automáticamente un **submenú de navegación**:

![SUBMENU](/docs/documentacion_usuario/images/image-12.png)

| Opción submenú | Acción |
|---|---|
| `[1]` Ver más resultados | Elige cuántos elementos mostrar |
| `[2]` Ver TODOS | Muestra la lista completa |
| `[3]` Buscar por nombre | Filtra por nombre dentro de los resultados |
| `[0]` Volver | Regresa al menú principal |

---

### Modo directo (comandos)

Puedes ejecutar cualquier operación directamente desde la terminal sin entrar al menú interactivo. Los comandos siguen esta estructura:

```bash
python cli.py <comando> [subcomando] [opciones]
```

#### Ver ayuda

```bash
# Ayuda general
python cli.py --help

# Ayuda de un comando específico
python cli.py team --help
python cli.py analytics --help
python cli.py filter --help
```

---

#### 🔍 Pokemon individual

```bash
python cli.py pokemon <nombre_o_id>

# Ejemplos
python cli.py pokemon pikachu
python cli.py pokemon 25
python cli.py pokemon charizard
python cli.py pokemon giratina-altered   # formas alternativas con sufijo completo
```

---

#### 🧬 Árbol evolutivo

```bash
python cli.py evolution <nombre_o_id>

# Ejemplos
python cli.py evolution charmander
python cli.py evolution 1
```

---

#### ⚔️ Efectividad de combate

```bash
python cli.py effectiveness <nombre_o_id>

# Ejemplos
python cli.py effectiveness pikachu
python cli.py effectiveness charizard
```

---

#### 🎛️ Filtros avanzados

Todos los parámetros son opcionales. Combínalos libremente.

```bash
python cli.py filter [--type TIPO] [--gen N] [--hp N] [--attack N]
                     [--defense N] [--speed N] [--base-exp N]

# Solo por tipo
python cli.py filter --type fire

# Por tipo y generación
python cli.py filter --type water --gen 1

# Con stats mínimas
python cli.py filter --type psychic --attack 80 --speed 90

# Filtro completo
python cli.py filter --type dragon --gen 3 --hp 70 --attack 100 --defense 60
```

---

#### 🛡️ Gestión de equipos

```bash
# Crear equipo (hasta 6 IDs separados por espacios)
python cli.py team create "Nombre del Equipo" 1 4 7 25 150 6

# Listar todos los equipos guardados
python cli.py team list

# Ver detalle de un equipo (usar el UUID del equipo)
python cli.py team get eba285df-3e7d-4bdd-ad4f-2b3a7d16dc95

# Eliminar un equipo
python cli.py team delete eba285df-3e7d-4bdd-ad4f-2b3a7d16dc95
```

> **Obtener el UUID:** usa `python cli.py team list` para ver los IDs de todos tus equipos antes de consultarlos o eliminarlos.

---

#### 📊 Analytics

```bash
# Promedios de stats por tipo elemental (los 18 tipos)
python cli.py analytics average

# Top-N Pokemon por métrica
python cli.py analytics top --metric attack --n 10
python cli.py analytics top --metric hp --n 5
python cli.py analytics top --metric speed --n 20

# Métricas disponibles para top: hp | attack | defense | speed | base_exp

# Detección de anomalías estadísticas
python cli.py analytics anomalies

# Predicción de stats por tipo
python cli.py analytics prediction fire
python cli.py analytics prediction water --secondary psychic
python cli.py analytics prediction grass

# Simulación de Pokemon sintéticos
python cli.py analytics simulate --type water --gen 1 --n 10
python cli.py analytics simulate --type fire --gen 3 --n 50 --seed 42
python cli.py analytics simulate --n 100 --type electric --gen 2
```

---

#### 💾 Exportar a CSV

```bash
# Exportar resultado de filtro
python cli.py export filter --type fire
python cli.py export filter --type water --gen 2

# Exportar Top-N
python cli.py export top --metric attack --n 20
python cli.py export top --metric hp --n 50
```

Los archivos se guardan en `data/reports/`:
- `filtro_pokemon.csv` — resultado del filtro aplicado
- `top_n_pokemon.csv` — resultado del ranking Top-N
---

#### 📈 Gráficos ASCII

```bash
# Stats de un Pokemon individual
python cli.py chart pokemon pikachu
python cli.py chart pokemon mewtwo
python cli.py chart pokemon 6

# Comparativa de promedios por tipo
python cli.py chart type --metric avg_attack
python cli.py chart type --metric avg_hp
python cli.py chart type --metric avg_speed
python cli.py chart type --metric avg_defense

# Métricas disponibles: avg_hp | avg_attack | avg_defense | avg_speed
```

---

### Tabla de referencia de comandos

| Operación | Comando directo |
|---|---|
| Ver Pokemon | `python cli.py pokemon pikachu` |
| Ver evoluciones | `python cli.py evolution charmander` |
| Ver efectividad | `python cli.py effectiveness charizard` |
| Filtrar | `python cli.py filter --type fire --gen 1` |
| Crear equipo | `python cli.py team create "Mi Equipo" 1 4 7` |
| Listar equipos | `python cli.py team list` |
| Ver equipo | `python cli.py team get <uuid>` |
| Eliminar equipo | `python cli.py team delete <uuid>` |
| Promedios por tipo | `python cli.py analytics average` |
| Top-N | `python cli.py analytics top --metric speed --n 5` |
| Anomalías | `python cli.py analytics anomalies` |
| Predicción | `python cli.py analytics prediction fire` |
| Simulación | `python cli.py analytics simulate --type water --n 10` |
| Exportar filtro | `python cli.py export filter --type grass` |
| Exportar Top-N | `python cli.py export top --metric hp` |
| Gráfico Pokemon | `python cli.py chart pokemon mewtwo` |
| Gráfico por tipo | `python cli.py chart type --metric avg_attack` |
| Ayuda general | `python cli.py --help` |
| Menú interactivo | `python cli.py` |