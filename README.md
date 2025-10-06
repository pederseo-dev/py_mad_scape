# py_mad_scape - Pac-Man Multiplayer

Un juego de Pac-Man multijugador que permite a varios jugadores controlar el juego desde sus dispositivos en la red local usando una API REST.

## 🎮 Características

- **Multijugador en red local**: Hasta 6 jugadores pueden jugar simultáneamente
- **Control remoto**: Los jugadores usan sus dispositivos como joysticks virtuales
- **API REST**: Servidor FastAPI para comunicación entre dispositivos
- **Algoritmo A***: IA para pathfinding de fantasmas
- **Interfaz gráfica**: Visualización con Pygame

## 📋 Requisitos

- Python 3.7 o superior
- Dispositivos conectados a la misma red local
- Dependencias: pygame, fastapi, uvicorn, pydantic, requests

## 🚀 Instalación

### 1. Crear entorno virtual
```bash
python -m venv venv
```

### 2. Activar el entorno virtual
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar las dependencias
```bash
pip install pygame fastapi uvicorn pydantic requests qrcode[pil] Pillow
```

## 🎯 Cómo Jugar

### 1. Ejecutar el servidor del juego
```bash
python main.py
```

### 2. Conectar jugadores
- **Todos los dispositivos deben estar en la misma red WiFi**
- Escanea el código QR que aparece en pantalla
- O visita la URL mostrada en tu navegador
- Ingresa tu nombre de usuario
- Presiona R para agregar jugadores de prueba

### 3. Objetivo del juego
- **Recolecta todas las monedas** (puntos amarillos) del mapa
- **Escapa del fantasma rojo** que te persigue
- El fantasma usa IA para encontrar al jugador más cercano
- Gana el jugador que recolecte más puntos

### 4. Controles
- **Flechas del teclado** o **WASD** para moverte
- **Botones en pantalla** en dispositivos móviles
- El juego inicia automáticamente cuando hay 6 jugadores

### 5. Consejos
- Mantente alejado del fantasma rojo
- Planifica tu ruta para recolectar monedas eficientemente
- Usa las esquinas y pasillos para esconderte

