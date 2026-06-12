# Guía de Contribución para TuxKeysToys

¡Gracias por tu interés en contribuir a TuxKeysToys! Todas las contribuciones son bienvenidas, desde reportes de bugs hasta mejoras de código y documentación.

## Cómo empezar

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/tuxkeystoys.git
cd tuxkeystoys
```

### 2. Configurar el entorno de desarrollo
Es altamente recomendable usar un entorno virtual que tenga acceso a los paquetes del sistema (necesario para Tkinter).

```bash
python3 -m venv venv --system-site-packages
```

### 3. Instalar dependencias de desarrollo
Este proyecto usa `setuptools` y permite instalar las dependencias necesarias para desarrollo (incluyendo `pytest` y `ruff`).

```bash
./venv/bin/pip install -e .[dev]
```

## Flujo de Trabajo (Workflow)

1. **Crea una rama (branch):** Crea una rama con un nombre descriptivo para tu feature o fix (ej. `feature/nuevos-ids-hardware` o `fix/error-ui`).
   ```bash
   git checkout -b tu-rama
   ```
2. **Haz tus cambios:** Escribe código limpio y usa Type Hints.
3. **Pasa el Linter (ruff):** Asegúrate de que tu código cumpla con las normas de estilo.
   ```bash
   ./venv/bin/ruff check .
   ```
4. **Ejecuta las pruebas (pytest):** Todo el código nuevo debe pasar las pruebas existentes. Si estás agregando una funcionalidad nueva, por favor añade pruebas unitarias para ella en la carpeta `tests/`.
   ```bash
   ./venv/bin/pytest
   ```
5. **Haz Commit:** Usa mensajes de commit descriptivos.
6. **Abre un Pull Request (PR):** Describe detalladamente qué cambios hiciste y por qué.

## Añadiendo compatibilidad a más laptops
Si estás agregando IDs de hardware de teclados para otras marcas de laptops en `src/tuxkeystoys/core/remap_service.py`, por favor asegúrate de especificar en tu PR de qué modelo de laptop provienen.

¡Gracias por contribuir a la comunidad Open Source!
