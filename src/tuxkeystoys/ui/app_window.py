import customtkinter as ctk
from tkinter import messagebox
import logging
from tuxkeystoys.core.remap_service import RemapService
from tuxkeystoys.ui.virtual_keyboard import VirtualKeyboardDialog, KEYD_TO_DISPLAY

logger = logging.getLogger(__name__)

# Configuración visual
FONT_FAMILY = "Roboto"
COLOR_PRIMARY = "#2563EB"
COLOR_PRIMARY_HOVER = "#1D4ED8"
COLOR_SUCCESS = "#059669"
COLOR_SUCCESS_HOVER = "#047857"
COLOR_DANGER = "#DC2626"
COLOR_DANGER_HOVER = "#B91C1C"

class KeyboardRemapperApp:
    def __init__(self, root: ctk.CTk, remap_service: RemapService, laptop_model: str):
        self.root = root
        self.remap_service = remap_service
        self.laptop_model = laptop_model
        
        self.root.title("TuxKeysToys - Hardware Remapper")
        self.root.geometry("720x650")
        self.root.minsize(700, 600)

        # Encabezado Principal
        header_container = ctk.CTkFrame(root, fg_color="transparent")
        header_container.pack(fill="x", padx=30, pady=(25, 10))

        title_lbl = ctk.CTkLabel(header_container, text="⌨️ TuxKeysToys", font=ctk.CTkFont(family=FONT_FAMILY, size=28, weight="bold"))
        title_lbl.pack(anchor="w")
        
        desc_lbl = ctk.CTkLabel(header_container, text=f"Remapeo exclusivo para el teclado integrado de {self.laptop_model}.", font=ctk.CTkFont(family=FONT_FAMILY, size=13), text_color=("gray50", "gray70"))
        desc_lbl.pack(anchor="w", pady=(2, 0))

        # Contenedor principal
        self.rules_frame = ctk.CTkScrollableFrame(root, corner_radius=12, fg_color=("#F3F4F6", "transparent"))
        self.rules_frame.pack(fill="both", expand=True, padx=30, pady=10)

        # Encabezados de columnas
        self.header_frame = ctk.CTkFrame(self.rules_frame, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(5, 15))
        ctk.CTkLabel(self.header_frame, text="Tecla Dañada", font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"), text_color=("gray40", "gray80")).pack(side="left", padx=60)
        ctk.CTkLabel(self.header_frame, text="Reemplazar con", font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"), text_color=("gray40", "gray80")).pack(side="left", padx=80)

        self.rows = []
        
        self.saved_rules = self.remap_service.get_existing_rules()

        # Cargar reglas guardadas, o un mínimo de 4 filas vacías
        rules_to_create = max(4, len(self.saved_rules))
        for _ in range(rules_to_create):
            saved_physical = ""
            saved_action = ""
            if len(self.saved_rules) > 0:
                saved_physical, saved_action = self.saved_rules.pop(0)
            self.add_rule_row(saved_physical, saved_action)

        # Contenedor para botones inferiores
        self.bottom_frame = ctk.CTkFrame(root, fg_color="transparent")
        self.bottom_frame.pack(fill="x", padx=30, pady=(10, 25))

        # Botón para añadir una nueva fila
        self.add_btn = ctk.CTkButton(self.bottom_frame, text="➕ Añadir Fila", 
                                       font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
                                       height=45, corner_radius=8,
                                       fg_color=COLOR_SUCCESS, hover_color=COLOR_SUCCESS_HOVER,
                                       command=self.add_empty_rule)
        self.add_btn.pack(side="left")

        # Botón de Aplicar
        self.apply_btn = ctk.CTkButton(self.bottom_frame, text="💾 Aplicar Cambios", 
                                       font=ctk.CTkFont(family=FONT_FAMILY, size=15, weight="bold"),
                                       height=45, corner_radius=8,
                                       fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER,
                                       command=self.apply_remap)
        self.apply_btn.pack(side="right")

    def add_empty_rule(self):
        self.add_rule_row("", "")

    def get_display_name(self, keyd_name: str) -> str:
        if not keyd_name:
            return "Haz clic para seleccionar"
        return KEYD_TO_DISPLAY.get(keyd_name, f"{keyd_name}")

    def add_rule_row(self, saved_physical: str = "", saved_action: str = ""):
        broken_display = self.get_display_name(saved_action)
        new_display = self.get_display_name(saved_physical)

        # Card container for each row
        row_card = ctk.CTkFrame(self.rules_frame, fg_color=("#FFFFFF", "#2B2B2B"), corner_radius=8, border_width=1, border_color=("#E5E7EB", "#3A3A3A"))
        row_card.pack(fill="x", pady=6, padx=5)
        
        # Inner layout
        inner_frame = ctk.CTkFrame(row_card, fg_color="transparent")
        inner_frame.pack(fill="x", pady=10, padx=15)

        btn_broken = ctk.CTkButton(inner_frame, text=broken_display, width=220, height=40, corner_radius=6,
                                   font=ctk.CTkFont(family=FONT_FAMILY, size=13),
                                   fg_color=("#F3F4F6", "#3A3A3A"), hover_color=("#E5E7EB", "#4D4D4D"), text_color=("black", "white"),
                                   border_width=1, border_color=("#D1D5DB", "#555555"))
        btn_broken.configure(command=lambda: self.open_vk(btn_broken, "broken"))
        btn_broken.pack(side="left", padx=(5, 15))
        btn_broken.keyd_name = saved_action
        
        # Flecha indicadora
        arrow_lbl = ctk.CTkLabel(inner_frame, text="⬅️", font=ctk.CTkFont(size=18), text_color=("gray60", "gray40"))
        arrow_lbl.pack(side="left", padx=10)

        btn_new = ctk.CTkButton(inner_frame, text=new_display, width=220, height=40, corner_radius=6,
                                font=ctk.CTkFont(family=FONT_FAMILY, size=13),
                                fg_color=("#F3F4F6", "#3A3A3A"), hover_color=("#E5E7EB", "#4D4D4D"), text_color=("black", "white"),
                                border_width=1, border_color=("#D1D5DB", "#555555"))
        btn_new.configure(command=lambda: self.open_vk(btn_new, "new"))
        btn_new.pack(side="left", padx=(15, 10))
        btn_new.keyd_name = saved_physical
        
        row_tuple = (btn_broken, btn_new)
        
        # Botón de eliminar con hover sutil
        btn_clear = ctk.CTkButton(inner_frame, text="🗑️", width=40, height=40, corner_radius=6,
                                  font=ctk.CTkFont(size=16),
                                  fg_color="transparent", hover_color=("#FEE2E2", "#7F1D1D"), text_color=("#EF4444", "#FCA5A5"))
        btn_clear.configure(command=lambda rf=row_card, rt=row_tuple: self.remove_row(rf, rt))
        btn_clear.pack(side="right", padx=(5, 0))

        self.rows.append(row_tuple)

    def remove_row(self, row_frame, row_tuple):
        row_frame.destroy()
        if row_tuple in self.rows:
            self.rows.remove(row_tuple)

    def open_vk(self, button_widget, mode: str):
        title = "Selecciona la Tecla DAÑADA" if mode == "broken" else "Selecciona el REEMPLAZO"
        
        def callback(display_name: str, keyd_name: str):
            button_widget.configure(text=display_name)
            button_widget.keyd_name = keyd_name
            
        VirtualKeyboardDialog(self.root, title, callback)

    def apply_remap(self):
        rules_to_apply = []
        for btn_broken, btn_new in self.rows:
            if btn_broken.keyd_name and btn_new.keyd_name:
                rules_to_apply.append((btn_new.keyd_name, btn_broken.keyd_name))

        try:
            active_rules = self.remap_service.apply_remap(rules_to_apply)
            messagebox.showinfo("✅ Éxito", f"Se aplicaron {active_rules} reglas correctamente.\nLos cambios ya están activos y solo afectan a tu laptop.")
        except Exception as e:
            logger.error(f"Error apply_remap: {e}")
            messagebox.showerror("❌ Error", f"Ocurrió un error al aplicar la configuración:\n\n{e}")
