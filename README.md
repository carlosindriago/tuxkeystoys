# TuxKeysToys 🐧⌨️

TuxKeysToys es una utilidad gráfica para MX Linux (y distribuciones basadas en Debian/Ubuntu) diseñada para facilitar el remapeo de teclas a nivel de hardware. Su principal ventaja es que **afecta exclusivamente al teclado integrado de la laptop**, respetando el comportamiento original de cualquier teclado externo (USB, Bluetooth, etc.).

Esta herramienta es ideal para laptops con teclas físicas dañadas, actuando como una alternativa a utilidades como PowerToys de Windows, pero enfocada en las necesidades y la arquitectura de Linux.

## Características ✨

- **Remapeo Exclusivo:** Por defecto, los cambios se aplican usando el ID de hardware estándar de los teclados integrados (`0001:0001` y otros), garantizando que los teclados externos no se vean afectados.
- **Teclado Virtual:** Interfaz amigable para seleccionar teclas que no puedes presionar físicamente (las dañadas).
- **Detección Física:** Permite presionar la tecla física que deseas usar como reemplazo para asegurar que el sistema la detecta correctamente.
- **Persistente:** La configuración sobrevive a reinicios y funciona desde la pantalla de inicio de sesión.
- **Backend Robusto:** Utiliza `keyd`, un demonio de remapeo de teclas a nivel de kernel muy ligero y poderoso.

## Compatibilidad 💻

La aplicación fue desarrollada y probada en una **ThinkPad T420s**, interceptando automáticamente los circuitos internos (Teclado principal, botones extra y ACPI). 
Sin embargo, **debería funcionar en el 99% de las laptops del mercado** (Asus, Dell, HP, Acer, etc.), ya que la inmensa mayoría utiliza el identificador estándar `0001:0001` (AT Translated Set 2 keyboard) para el teclado integrado.

*Si tienes una laptop de otra marca y alguna tecla multimedia no se remapea, puedes contribuir añadiendo el ID de hardware de tu laptop al código.*

## Requisitos Previos 🛠️

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

## Instalación del Proyecto 🚀

```bash
# 1. Clonar el repositorio
git clone https://github.com/carlosindriago/tuxkeystoys.git
cd tuxkeystoys

# 2. Crear entorno virtual (con acceso a los paquetes del sistema para Tkinter)
python3 -m venv venv --system-site-packages

# 3. Lanzar la aplicación
sudo -E ./venv/bin/python tuxkeystoys.py
```

## Uso 🎮

1. Lanza la aplicación ejecutando `sudo -E ./venv/bin/python tuxkeystoys.py`.
2. Haz clic en "Seleccionar..." debajo de **Tecla Dañada**.
3. Si la tecla está físicamente rota, búscala y haz clic en ella en el **Teclado Virtual** mostrado en pantalla.
4. Haz clic en "Seleccionar..." debajo de **Reemplazar con**.
5. Presiona la tecla física que deseas usar para reemplazarla.
6. Haz clic en **Aplicar y Guardar Cambios**.
7. ¡Disfruta de tu teclado funcionando nuevamente!

## Contribuciones 🤝

¡Las contribuciones son bienvenidas! Especialmente si:
- Quieres añadir soporte (nuevos IDs de hardware) para teclas multimedia exclusivas de otras marcas de laptops.
- Quieres mejorar la interfaz gráfica o empaquetarla como `.deb` o AppImage/Flatpak.
- Tienes ideas para nuevas funcionalidades.

Siéntete libre de abrir un *Issue* o enviar un *Pull Request*.

## Licencia 📄

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---
*Desarrollado con ❤️ en MX Linux por Carlos Indriago y la ayuda de IA.*
