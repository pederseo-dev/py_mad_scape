# py_mad_scape# Pac-Man Game - Instrucciones de Instalación

## Requisitos
- Python 3.7 o superior instalado en Windows

## Pasos de Instalación

### 1. Crear entorno virtual
```bash
python -m venv venv
```

### 2. Activar el entorno virtual
```bash
venv\Scripts\activate
```

### 3. Instalar las dependencias
```bash
pip install pygame fastapi uvicorn pydantic
```

## Ejecución del Proyecto

### Ejecutar el juego
```bash
python main.py
uvicorn main:app --reload
```

## Desactivar el entorno virtual
Cuando termines de trabajar, puedes desactivar el entorno con:
```bash
deactivate
```

---

## Notas
- Asegúrate de activar el entorno virtual cada vez que trabajes en el proyecto
- El archivo `main.py` debe estar en la raíz del proyecto