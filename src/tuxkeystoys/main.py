import sys
import logging
import customtkinter as ctk
from tuxkeystoys.infrastructure.system_handler import SystemHandler
from tuxkeystoys.core.remap_service import RemapService
from tuxkeystoys.ui.app_window import KeyboardRemapperApp

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stdout
    )

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting TuxKeysToys...")

    # Configuración de apariencia moderna (estilo macOS)
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    # Inicializar dependencias
    system_handler = SystemHandler()
    remap_service = RemapService(system_handler)
    laptop_model = system_handler.get_laptop_model()

    root = ctk.CTk()
    _app = KeyboardRemapperApp(root, remap_service, laptop_model)
    root.mainloop()

if __name__ == "__main__":
    main()
