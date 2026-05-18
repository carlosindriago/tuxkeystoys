import customtkinter as ctk
from tkinter import messagebox
import os
import subprocess

# Configuración de apariencia moderna (estilo macOS)
ctk.set_appearance_mode("System")  # Se adapta al modo claro/oscuro del sistema
ctk.set_default_color_theme("blue") # Tema de acento azul

INTERNAL_KB_IDS = "0001:0001\n17aa:5054\n0000:0000"
CONFIG_FILE = "/etc/keyd/laptop_remap.conf"

# Diseño del teclado virtual
VK_LAYOUT = [
    ["Esc", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"],
    ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "Bksp"],
    ["Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\"],
    ["Caps", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "Enter"],
    ["LShift", "< >", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "RShift"],
    ["LCtrl", "Super/Win", "LAlt", "Space", "RAlt", "RCtrl", "Left", "Up", "Down", "Right"]
]

# Mapa de Teclas Virtuales a nombres de keyd
VK_TO_KEYD = {
    "Esc": "esc", "F1": "f1", "F2": "f2", "F3": "f3", "F4": "f4", "F5": "f5", "F6": "f6", "F7": "f7", "F8": "f8", "F9": "f9", "F10": "f10", "F11": "f11", "F12": "f12",
    "`": "grave", "1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9", "0": "0", "-": "minus", "=": "equal", "Bksp": "backspace",
    "Tab": "tab", "Q": "q", "W": "w", "E": "e", "R": "r", "T": "t", "Y": "y", "U": "u", "I": "i", "O": "o", "P": "p", "[": "leftbrace", "]": "rightbrace", "\\": "backslash",
    "Caps": "capslock", "A": "a", "S": "s", "D": "d", "F": "f", "G": "g", "H": "h", "J": "j", "K": "k", "L": "l", ";": "semicolon", "'": "apostrophe", "Enter": "enter",
    "LShift": "leftshift", "< >": "102nd", "Z": "z", "X": "x", "C": "c", "V": "v", "B": "b", "N": "n", "M": "m", ",": "comma", ".": "dot", "/": "slash", "RShift": "rightshift",
    "LCtrl": "leftcontrol", "Super/Win": "meta", "LAlt": "leftalt", "Space": "space", "RAlt": "rightalt", "RCtrl": "rightcontrol",
    "Up": "up", "Left": "left", "Down": "down", "Right": "right"
}

KEYSYM_TO_KEYD = {
    "Escape": "esc", "F1": "f1", "F2": "f2", "F3": "f3", "F4": "f4", "F5": "f5", "F6": "f6", "F7": "f7", "F8": "f8", "F9": "f9", "F10": "f10", "F11": "f11", "F12": "f12",
    "grave": "grave", "minus": "minus", "equal": "equal", "BackSpace": "backspace",
    "Tab": "tab", "bracketleft": "leftbrace", "bracketright": "rightbrace", "backslash": "backslash",
    "Caps_Lock": "capslock", "semicolon": "semicolon", "apostrophe": "apostrophe", "Return": "enter",
    "Shift_L": "leftshift", "less": "102nd", "greater": "102nd", "comma": "comma", "period": "dot", "slash": "slash", "Shift_R": "rightshift",
    "Control_L": "leftcontrol", "Super_L": "meta", "Alt_L": "leftalt", "space": "space", "Alt_R": "rightalt", "Control_R": "rightcontrol",
    "Up": "up", "Left": "left", "Down": "down", "Right": "right",
    "Prior": "pageup", "Next": "pagedown", "End": "end", "Home": "home", "Insert": "insert", "Delete": "delete",
    "Print": "sysrq", "Menu": "compose", "Pause": "pause", "Scroll_Lock": "scrolllock", "Num_Lock": "numlock"
}

for char in "abcdefghijklmnopqrstuvwxyz1234567890":
    KEYSYM_TO_KEYD[char] = char
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    KEYSYM_TO_KEYD[char] = char.lower()

KEYD_TO_DISPLAY = {v: k for k, v in KEYSYM_TO_KEYD.items()}
for k, v in VK_TO_KEYD.items():
    KEYD_TO_DISPLAY[v] = f"{k}"

class VirtualKeyboardDialog:
    def __init__(self, parent, title, callback):
        self.top = ctk.CTkToplevel(parent)
        self.top.title(title)
        self.top.geometry("900x450")
        self.top.minsize(850, 400)
        self.top.transient(parent)
        self.callback = callback
        
        self.is_chord_mode = ctk.BooleanVar(value=False)
        self.current_chord = []
        self.current_chord_display = []
        
        lbl = ctk.CTkLabel(self.top, text="Haz clic en el TECLADO VIRTUAL  --o--  PRESIONA una TECLA FÍSICA", font=ctk.CTkFont(family="Arial", size=16, weight="bold"))
        lbl.pack(pady=(15, 5))

        top_bar = ctk.CTkFrame(self.top, fg_color="transparent")
        top_bar.pack(fill="x", padx=20, pady=5)
        
        chord_cb = ctk.CTkCheckBox(top_bar, text="Modo Combinación (Múltiples teclas al mismo tiempo)", variable=self.is_chord_mode, command=self.on_chord_mode_change)
        chord_cb.pack(side="left")
        
        self.chord_display_lbl = ctk.CTkLabel(top_bar, text="Combinación actual: (ninguna)", font=ctk.CTkFont(family="Arial", size=14, slant="italic"), text_color="#2196F3")
        self.chord_display_lbl.pack(side="left", padx=20)
        
        self.btn_save_chord = ctk.CTkButton(top_bar, text="Guardar Combinación", fg_color="#4CAF50", hover_color="#388E3C", command=self.save_chord, state="disabled")
        self.btn_save_chord.pack(side="right")

        kb_frame = ctk.CTkFrame(self.top, fg_color="transparent")
        kb_frame.pack(expand=True, fill="both", padx=10, pady=10)

        for row in VK_LAYOUT:
            row_frame = ctk.CTkFrame(kb_frame, fg_color="transparent")
            row_frame.pack(side="top", pady=3)
            for key in row:
                width = 45
                if key == "Space": width = 250
                elif key in ["Enter", "LShift", "RShift", "Caps", "Bksp", "Tab", "Super/Win"]: width = 85
                
                btn = ctk.CTkButton(row_frame, text=key, width=width, height=45, corner_radius=8,
                                    font=ctk.CTkFont(family="Arial", size=13),
                                    fg_color=("#E0E0E0", "#333333"), hover_color=("#BDBDBD", "#555555"), 
                                    text_color=("black", "white"),
                                    command=lambda k=key: self.on_virtual_click(k))
                btn.pack(side="left", padx=3)

        self.top.bind("<KeyPress>", self.on_physical_keypress)
        self.top.focus_set()
        
        # Esperar un poco antes de capturar el foco para evitar error en Linux
        self.top.after(100, self.top.grab_set)

    def on_chord_mode_change(self):
        if not self.is_chord_mode.get():
            self.current_chord = []
            self.current_chord_display = []
            self.chord_display_lbl.configure(text="Combinación actual: (ninguna)")
            self.btn_save_chord.configure(state="disabled")
        self.top.focus_set()

    def add_to_chord(self, display_name, keyd_name):
        if keyd_name not in self.current_chord:
            self.current_chord.append(keyd_name)
            self.current_chord_display.append(display_name)
            self.chord_display_lbl.configure(text=f"Combinación: {' + '.join(self.current_chord_display)}")
            self.btn_save_chord.configure(state="normal")

    def save_chord(self):
        if self.current_chord:
            final_keyd = "+".join(self.current_chord)
            final_display = " + ".join(self.current_chord_display)
            self.callback(final_display, final_keyd)
            self.top.destroy()

    def on_virtual_click(self, key_label):
        keyd_name = VK_TO_KEYD.get(key_label, "")
        if self.is_chord_mode.get():
            self.add_to_chord(key_label, keyd_name)
        else:
            self.callback(f"{key_label}", keyd_name)
            self.top.destroy()

    def on_physical_keypress(self, event):
        keysym = event.keysym
        keyd_name = KEYSYM_TO_KEYD.get(keysym)
        if not keyd_name:
            keyd_name = keysym.lower()
            if keyd_name.startswith("xf86"):
                keyd_name = keyd_name[4:]
            
        display_name = f"{keysym}"
        
        if self.is_chord_mode.get():
            self.add_to_chord(display_name, keyd_name)
        else:
            self.callback(display_name, keyd_name)
            self.top.destroy()

def get_laptop_model():
    try:
        with open("/sys/devices/virtual/dmi/id/product_name", "r") as f:
            model = f.read().strip()
            if model:
                return f"tu portátil {model}"
    except Exception:
        pass
    return "tu laptop"

class KeyboardRemapperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TuxKeysToys - Teclado Virtual (Solo Laptop)")
        self.root.geometry("680x600")

        # Título Principal
        title_lbl = ctk.CTkLabel(root, text="Remapeo de Teclas Dañadas", font=ctk.CTkFont(family="Arial", size=24, weight="bold"))
        title_lbl.pack(pady=(20, 5))
        
        laptop_model = get_laptop_model()
        desc_lbl = ctk.CTkLabel(root, text=f"Estos cambios SOLO afectarán al teclado integrado de {laptop_model}.", font=ctk.CTkFont(family="Arial", size=12), text_color="gray")
        desc_lbl.pack(pady=(0, 20))

        # Contenedor principal con fondo redondeado (ahora con scroll)
        self.rules_frame = ctk.CTkScrollableFrame(root, corner_radius=15, fg_color=("#F5F5F5", "#2B2B2B"))
        self.rules_frame.pack(fill="both", expand=True, padx=30, pady=10)

        # Encabezados (se añaden a un frame superior para que no hagan scroll, o los dejamos dentro)
        self.header_frame = ctk.CTkFrame(self.rules_frame, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(self.header_frame, text="Tecla Dañada", font=ctk.CTkFont(family="Arial", size=14, weight="bold")).pack(side="left", padx=50)
        ctk.CTkLabel(self.header_frame, text="Reemplazar con", font=ctk.CTkFont(family="Arial", size=14, weight="bold")).pack(side="left", padx=65)

        self.rows = []
        
        self.load_existing_config()

        # Cargar reglas guardadas, o un mínimo de 6 filas vacías
        rules_to_create = max(6, len(self.saved_rules))
        for i in range(rules_to_create):
            saved_physical = ""
            saved_action = ""
            if len(self.saved_rules) > 0:
                saved_physical, saved_action = self.saved_rules.pop(0)
            self.add_rule_row(saved_physical, saved_action)

        # Contenedor para botones inferiores
        self.bottom_frame = ctk.CTkFrame(root, fg_color="transparent")
        self.bottom_frame.pack(pady=15)

        # Botón para añadir una nueva fila
        self.add_btn = ctk.CTkButton(self.bottom_frame, text="+ Añadir Regla", 
                                       font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
                                       height=40, corner_radius=10,
                                       fg_color="#4CAF50", hover_color="#388E3C",
                                       command=self.add_empty_rule)
        self.add_btn.pack(side="left", padx=15)

        # Botón de Aplicar estilo destacado
        self.apply_btn = ctk.CTkButton(self.bottom_frame, text="Aplicar y Guardar Cambios", 
                                       font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
                                       height=40, corner_radius=10,
                                       fg_color="#2196F3", hover_color="#1976D2",
                                       command=self.apply_remap)
        self.apply_btn.pack(side="left", padx=15)

    def add_empty_rule(self):
        self.add_rule_row("", "")

    def load_existing_config(self):
        self.saved_rules = []
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r") as f:
                    in_main = False
                    for line in f:
                        line = line.strip()
                        if line == "[main]":
                            in_main = True
                        elif in_main and "=" in line and not line.startswith("#"):
                            parts = line.split("=")
                            physical = parts[0].strip()
                            action = parts[1].strip()
                            self.saved_rules.append((physical, action))
        except Exception as e:
            print(f"Error cargando configuración: {e}")

    def get_display_name(self, keyd_name):
        if not keyd_name: return "Seleccionar..."
        return KEYD_TO_DISPLAY.get(keyd_name, f"{keyd_name}")

    def add_rule_row(self, saved_physical="", saved_action=""):
        broken_display = self.get_display_name(saved_action)
        new_display = self.get_display_name(saved_physical)

        row_frame = ctk.CTkFrame(self.rules_frame, fg_color="transparent")
        row_frame.pack(fill="x", pady=4)

        btn_broken = ctk.CTkButton(row_frame, text=broken_display, width=200, height=35, corner_radius=8,
                                   font=ctk.CTkFont(family="Arial", size=13),
                                   fg_color=("#E0E0E0", "#444444"), hover_color=("#BDBDBD", "#666666"), text_color=("black", "white"))
        btn_broken.configure(command=lambda: self.open_vk(btn_broken, "broken"))
        btn_broken.pack(side="left", padx=(20, 10))
        btn_broken.keyd_name = saved_action
        
        btn_new = ctk.CTkButton(row_frame, text=new_display, width=200, height=35, corner_radius=8,
                                font=ctk.CTkFont(family="Arial", size=13),
                                fg_color=("#E0E0E0", "#444444"), hover_color=("#BDBDBD", "#666666"), text_color=("black", "white"))
        btn_new.configure(command=lambda: self.open_vk(btn_new, "new"))
        btn_new.pack(side="left", padx=(35, 10))
        btn_new.keyd_name = saved_physical
        
        row_tuple = (btn_broken, btn_new)
        
        btn_clear = ctk.CTkButton(row_frame, text="✕", width=35, height=35, corner_radius=8,
                                  font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
                                  fg_color="#EF5350", hover_color="#D32F2F", text_color="white")
        btn_clear.configure(command=lambda rf=row_frame, rt=row_tuple: self.remove_row(rf, rt))
        btn_clear.pack(side="left", padx=(15, 20))

        self.rows.append(row_tuple)

    def remove_row(self, row_frame, row_tuple):
        # Destruir el widget visual y sacarlo de la lista
        row_frame.destroy()
        if row_tuple in self.rows:
            self.rows.remove(row_tuple)

    def open_vk(self, button_widget, mode):
        title = "Selecciona la Tecla DAÑADA" if mode == "broken" else "Selecciona el REEMPLAZO"
        
        def callback(display_name, keyd_name):
            button_widget.configure(text=display_name)
            button_widget.keyd_name = keyd_name
            
        VirtualKeyboardDialog(self.root, title, callback)

    def apply_remap(self):
        config_content = f"# Archivo autogenerado por TuxKeysToys\n[ids]\n{INTERNAL_KB_IDS}\n\n[main]\n"
        reglas_activas = 0
        for btn_broken, btn_new in self.rows:
            if btn_broken.keyd_name and btn_new.keyd_name:
                config_content += f"{btn_new.keyd_name} = {btn_broken.keyd_name}\n"
                reglas_activas += 1

        if reglas_activas == 0:
            config_content += "# No hay reglas activas\n"

        try:
            with open("/tmp/laptop_remap.conf", "w") as f:
                f.write(config_content)
            
            subprocess.run(["sudo", "mv", "/tmp/laptop_remap.conf", "/etc/keyd/laptop_remap.conf"], check=True)
            subprocess.run(["sudo", "keyd", "reload"], check=True)
            
            messagebox.showinfo("Éxito", f"Se aplicaron {reglas_activas} reglas correctamente.\nSolo afectarán a tu laptop.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al aplicar:\n\n{e}")

if __name__ == "__main__":
    # CustomTkinter usa CTk en lugar de Tk()
    root = ctk.CTk()
    app = KeyboardRemapperApp(root)
    root.mainloop()