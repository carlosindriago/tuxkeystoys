# TuxKeysToys

TuxKeysToys es una utilidad gráfica para MX Linux (y distribuciones basadas en Debian) diseñada para facilitar el remapeo de teclas a nivel de hardware, afectando **exclusivamente al teclado integrado de la laptop** y respetando el comportamiento original de cualquier teclado externo (USB, Bluetooth, etc.).

Esta herramienta es ideal para laptops con teclas físicas dañadas, actuando como una alternativa a utilidades como PowerToys de Windows, pero enfocada en las necesidades de Linux.

## Características

- **Remapeo Exclusivo:** Los cambios se aplican usando el ID de hardware (`0001:0001`), garantizando que solo el teclado de la laptop (ej. ThinkPad T420s) sea afectado.
- **Teclado Virtual:** Interfaz amigable para seleccionar teclas que no puedes presionar físicamente (las dañadas).
- **Detección Física:** Permite presionar la tecla física que deseas usar como reemplazo para asegurar que el sistema la detecta correctamente.
- **Persistente:** La configuración sobrevive a reinicios y funciona desde la pantalla de inicio de sesión.
- **Backend Robusto:** Utiliza `keyd`, un demonio de remapeo de teclas a nivel de kernel muy ligero y poderoso.

## Requisitos Previos

- Python 3
- Entorno Virtual de Python (`python3-venv`)
- Soporte para Tkinter (`python3-tk`)
- `keyd` instalado y corriendo como servicio.

### Instalación de dependencias

```bash
# 1. Instalar herramientas del sistema
sudo apt update && sudo apt install -y build-essential git python3-tk python3-venv

# 2. Instalar keyd
git clone https://github.com/rvaiya/keyd /tmp/keyd
cd /tmp/keyd
make && sudo make install
sudo systemctl enable keyd
sudo systemctl start keyd
```

## Instalación y Configuración del Proyecto

```bash
# 1. Clonar o crear el directorio
mkdir -p ~/tuxkeystoys
cd ~/tuxkeystoys

# 2. Crear entorno virtual (con acceso a los paquetes del sistema para Tkinter)
python3 -m venv venv --system-site-packages

# 3. Lanzar la aplicación
sudo -E ./venv/bin/python tuxkeystoys.py
```

## Uso

1. Lanza la aplicación ejecutando `sudo -E ./venv/bin/python tuxkeystoys.py` dentro del directorio del proyecto.
2. Haz clic en "Seleccionar..." debajo de **Tecla Dañada**. Se abrirá una ventana.
3. Si la tecla está físicamente dañada, bscala y haz clic en ella en el **Teclado Virtual** mostrado en pantalla.
4. Haz clic en "Seleccionar..." debajo de **Reemplazar con**.
5. Presiona la tecla física que deseas usar para reemplazarla.
6. Haz clic en **Aplicar y Guardar Cambios**.
7. ¡Disfruta de tu teclado funcionando nuevamente!

## Historial de Desarrollo

- Se creó el concepto basado en la necesidad de reemplazar teclas dañadas (como `< >`, `Super`, etc.) sin afectar un teclado externo en MX Linux.
- Se seleccionó `keyd` como motor por su capacidad para filtrar reglas por ID de dispositivo.
- Se implementó una interfaz gráfica con Tkinter (`tuxkeystoys.py`).
- Se resolvieron problemas de compatibilidad de entornos virtuales con `tkinter` al forzar el uso de `python3-venv --system-site-packages`.
- Se introdujo un teclado virtual interactivo para solucionar el problema de no poder escribir o presionar las teclas dañadas para configurarlas.
- Se descubrió que las laptops ThinkPad exponen múltiples interfaces de teclado (`0001:0001` para el principal, `17aa:5054` para botones extra, y `0000:0000` para ACPI). El programa ahora intercepta todos estos circuitos internos para asegurar que teclas como `Menu` o `RePag` sean remapeadas correctamente.
- Se mapearon correctamente teclas con nombres atípicos en el subsistema evdev/keyd:
  - La tecla **Super/Windows** debe ser asignada a `meta` (no a `leftmeta`).
  - La tecla física **Menu** es detectada a nivel de hardware como `compose`.
  - Las teclas multimedia (ej. `xf86forward`) deben tener el prefijo `xf86` removido (ej. `forward`) para que `keyd` las acepte.

---
*Desarrollado en MX Linux.*
