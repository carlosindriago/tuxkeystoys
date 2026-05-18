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
        self.top.geometry("900x380")
        self.top.minsize(850, 350)
        self.top.transient(parent)
        self.callback = callback
        
        lbl = ctk.CTkLabel(self.top, text="Haz clic en el TECLADO VIRTUAL  --o--  PRESIONA una TECLA FÍSICA ahora", font=ctk.CTkFont(family="Arial", size=16, weight="bold"))
        lbl.pack(pady=15)

        kb_frame = ctk.CTkFrame(self.top, fg_color="transparent")
        kb_frame.pack(expand=True, fill="both", padx=10, pady=10)

        for row in VK_LAYOUT:
            row_frame = ctk.CTkFrame(kb_frame, fg_color="transparent")
            row_frame.pack(side="top", pady=3)
            for key in row:
                width = 45
                if key == "Space": width = 250
                elif key in ["Enter", "LShift", "RShift", "Caps", "Bksp", "Tab", "Super/Win"]: width = 85
                
                # Estilo tipo teclas de Mac (gris oscuro/claro con esquinas redondeadas)
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

    def on_virtual_click(self, key_label):
        keyd_name = VK_TO_KEYD.get(key_label, "")
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
        self.callback(display_name, keyd_name)
        self.top.destroy()

class KeyboardRemapperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TuxKeysToys - Teclado Virtual (Solo Laptop)")
        self.root.geometry("680x600")

        # Título Principal
        title_lbl = ctk.CTkLabel(root, text="Remapeo de Teclas Dañadas", font=ctk.CTkFont(family="Arial", size=24, weight="bold"))
        title_lbl.pack(pady=(20, 5))
        
        desc_lbl = ctk.CTkLabel(root, text="Estos cambios SOLO afectarán al teclado integrado de tu ThinkPad T420s.", font=ctk.CTkFont(family="Arial", size=12), text_color="gray")
        desc_lbl.pack(pady=(0, 20))

        # Contenedor principal con fondo redondeado
        self.rules_frame = ctk.CTkFrame(root, corner_radius=15, fg_color=("#F5F5F5", "#2B2B2B"))
        self.rules_frame.pack(fill="both", expand=True, padx=30, pady=10)

        # Encabezados
        ctk.CTkLabel(self.rules_frame, text="Tecla Dañada", font=ctk.CTkFont(family="Arial", size=14, weight="bold")).grid(row=0, column=0, padx=20, pady=15)
        ctk.CTkLabel(self.rules_frame, text="Reemplazar con", font=ctk.CTkFont(family="Arial", size=14, weight="bold")).grid(row=0, column=1, padx=20, pady=15)

        self.rows = []
        
        self.load_existing_config()

        for i in range(1, 7):
            saved_physical = ""
            saved_action = ""
            if len(self.saved_rules) > 0:
                saved_physical, saved_action = self.saved_rules.pop(0)
            self.add_rule_row(i, saved_physical, saved_action)

        # Botón de Aplicar estilo destacado
        self.apply_btn = ctk.CTkButton(root, text="Aplicar y Guardar Cambios", 
                                       font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
                                       height=50, corner_radius=10,
                                       fg_color="#2196F3", hover_color="#1976D2",
                                       command=self.apply_remap)
        self.apply_btn.pack(pady=25)

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

    def add_rule_row(self, row_index, saved_physical="", saved_action=""):
        broken_display = self.get_display_name(saved_action)
        new_display = self.get_display_name(saved_physical)

        btn_broken = ctk.CTkButton(self.rules_frame, text=broken_display, width=200, height=35, corner_radius=8,
                                   font=ctk.CTkFont(family="Arial", size=13),
                                   fg_color=("#E0E0E0", "#444444"), hover_color=("#BDBDBD", "#666666"), text_color=("black", "white"),
                                   command=lambda: self.open_vk(btn_broken, "broken"))
        btn_broken.grid(row=row_index, column=0, pady=8, padx=20)
        btn_broken.keyd_name = saved_action
        
        btn_new = ctk.CTkButton(self.rules_frame, text=new_display, width=200, height=35, corner_radius=8,
                                font=ctk.CTkFont(family="Arial", size=13),
                                fg_color=("#E0E0E0", "#444444"), hover_color=("#BDBDBD", "#666666"), text_color=("black", "white"),
                                command=lambda: self.open_vk(btn_new, "new"))
        btn_new.grid(row=row_index, column=1, pady=8, padx=20)
        btn_new.keyd_name = saved_physical
        
        btn_clear = ctk.CTkButton(self.rules_frame, text="✕", width=35, height=35, corner_radius=8,
                                  font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
                                  fg_color="#EF5350", hover_color="#D32F2F", text_color="white",
                                  command=lambda: self.clear_row(btn_broken, btn_new))
        btn_clear.grid(row=row_index, column=2, pady=8, padx=(0, 20))

        self.rows.append((btn_broken, btn_new))

    def clear_row(self, btn_broken, btn_new):
        btn_broken.configure(text="Seleccionar...")
        btn_broken.keyd_name = ""
        btn_new.configure(text="Seleccionar...")
        btn_new.keyd_name = ""

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