# py_mad_scape - Pac-Man Multiplayer

Un juego de Pac-Man multijugador que permite a varios jugadores controlar el juego desde sus dispositivos en la red local usando una API REST.

## 🎮 Características

- **Multijugador en red local**: Hasta 2 jugadores pueden jugar simultáneamente
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
pip install pygame fastapi uvicorn pydantic requests
```

## 🎯 Cómo Jugar

### 1. Ejecutar el servidor del juego
```bash
python main.py
```

