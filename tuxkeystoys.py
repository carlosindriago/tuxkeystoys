import tkinter as tk
from tkinter import messagebox
import os
import subprocess

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

# Mapa de Teclas Físicas de Tkinter a nombres de keyd (Mejorado para evitar crashes)
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

# Rellenar alfabeto y números para teclado físico
for char in "abcdefghijklmnopqrstuvwxyz1234567890":
    KEYSYM_TO_KEYD[char] = char
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    KEYSYM_TO_KEYD[char] = char.lower()

# Mapeo inverso para mostrar nombres amigables en la UI al cargar
KEYD_TO_DISPLAY = {v: k for k, v in KEYSYM_TO_KEYD.items()}
for k, v in VK_TO_KEYD.items():
    KEYD_TO_DISPLAY[v] = f"Virtual: {k}"

class VirtualKeyboardDialog:
    def __init__(self, parent, title, callback):
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.top.geometry("950x350")
        self.top.minsize(900, 300)
        self.top.transient(parent)
        self.top.grab_set()
        self.callback = callback
        
        lbl = tk.Label(self.top, text="Haz clic en el TECLADO VIRTUAL  --o--  PRESIONA una TECLA FÍSICA ahora", font=("Arial", 12, "bold"))
        lbl.pack(pady=10)

        kb_frame = tk.Frame(self.top, padx=10, pady=10)
        kb_frame.pack(expand=True, fill="both")

        for row in VK_LAYOUT:
            row_frame = tk.Frame(kb_frame)
            row_frame.pack(side="top", pady=2)
            for key in row:
                width = 4
                if key == "Space": width = 25
                elif key in ["Enter", "LShift", "RShift", "Caps", "Bksp", "Tab", "Super/Win"]: width = 9
                
                btn = tk.Button(row_frame, text=key, width=width, height=2, 
                                padx=2, command=lambda k=key: self.on_virtual_click(k))
                btn.pack(side="left", padx=2)

        # Escuchar teclado físico
        self.top.bind("<KeyPress>", self.on_physical_keypress)
        self.top.focus_set()

    def on_virtual_click(self, key_label):
        keyd_name = VK_TO_KEYD.get(key_label, "")
        self.callback(f"Virtual: {key_label}", keyd_name)
        self.top.destroy()

    def on_physical_keypress(self, event):
        keysym = event.keysym
        keyd_name = KEYSYM_TO_KEYD.get(keysym)
        if not keyd_name:
            # Fallback simple
            keyd_name = keysym.lower()
            if keyd_name.startswith("xf86"):
                keyd_name = keyd_name[4:]
            
        display_name = f"Física: {keysym}"
        self.callback(display_name, keyd_name)
        self.top.destroy()

class KeyboardRemapperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TuxKeysToys - Teclado Virtual (Solo Laptop)")
        self.root.geometry("650x550")
        self.root.configure(padx=20, pady=20)

        tk.Label(root, text="Remapeo de Teclas Dañadas", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(root, text="Estos cambios SOLO afectarán al teclado integrado de tu ThinkPad T420s.", fg="gray").pack(pady=5)

        self.rules_frame = tk.Frame(root)
        self.rules_frame.pack(fill="both", expand=True, pady=10)

        tk.Label(self.rules_frame, text="Tecla Dañada", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10)
        tk.Label(self.rules_frame, text="Reemplazar con", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=10)

        self.rows = []
        
        # Cargar configuración existente
        self.load_existing_config()

        # Crear 6 filas para reglas, rellenando con las guardadas si existen
        for i in range(1, 7):
            saved_physical = ""
            saved_action = ""
            if len(self.saved_rules) > 0:
                saved_physical, saved_action = self.saved_rules.pop(0)
            self.add_rule_row(i, saved_physical, saved_action)

        tk.Button(root, text="Aplicar y Guardar Cambios", bg="#4CAF50", fg="white", font=("Arial", 12), command=self.apply_remap).pack(pady=20)

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
        return KEYD_TO_DISPLAY.get(keyd_name, f"Tecla: {keyd_name}")

    def add_rule_row(self, row_index, saved_physical="", saved_action=""):
        # El formato en config es: fisico_presionado = accion_ejecutada
        # UI: Tecla Dañada (accion_ejecutada) | Reemplazar con (fisico_presionado)
        
        broken_display = self.get_display_name(saved_action)
        new_display = self.get_display_name(saved_physical)

        # Botón para tecla rota (la acción)
        btn_broken = tk.Button(self.rules_frame, text=broken_display, width=20, 
                               command=lambda: self.open_vk(btn_broken, "broken"))
        btn_broken.grid(row=row_index, column=0, pady=5, padx=10)
        btn_broken.keyd_name = saved_action
        
        # Botón para tecla de reemplazo (la tecla física a presionar)
        btn_new = tk.Button(self.rules_frame, text=new_display, width=20, 
                            command=lambda: self.open_vk(btn_new, "new"))
        btn_new.grid(row=row_index, column=1, pady=5, padx=10)
        btn_new.keyd_name = saved_physical
        
        # Botón limpiar
        btn_clear = tk.Button(self.rules_frame, text="X", fg="red", 
                              command=lambda: self.clear_row(btn_broken, btn_new))
        btn_clear.grid(row=row_index, column=2, pady=5)

        self.rows.append((btn_broken, btn_new))

    def clear_row(self, btn_broken, btn_new):
        btn_broken.config(text="Seleccionar...")
        btn_broken.keyd_name = ""
        btn_new.config(text="Seleccionar...")
        btn_new.keyd_name = ""

    def open_vk(self, button_widget, mode):
        title = "Selecciona la Tecla DAÑADA" if mode == "broken" else "Selecciona el REEMPLAZO"
        
        def callback(display_name, keyd_name):
            button_widget.config(text=display_name)
            button_widget.keyd_name = keyd_name
            
        VirtualKeyboardDialog(self.root, title, callback)

    def apply_remap(self):
        config_content = f"# Archivo autogenerado por TuxKeysToys\n[ids]\n{INTERNAL_KB_IDS}\n\n[main]\n"
        reglas_activas = 0
        for btn_broken, btn_new in self.rows:
            if btn_broken.keyd_name and btn_new.keyd_name:
                # El formato de keyd es: fisico_presionado = accion_ejecutada
                config_content += f"{btn_new.keyd_name} = {btn_broken.keyd_name}\n"
                reglas_activas += 1

        if reglas_activas == 0:
            config_content += "# No hay reglas activas\n"

        try:
            with open("/tmp/laptop_remap.conf", "w") as f:
                f.write(config_content)
            
            subprocess.run(["sudo", "mv", "/tmp/laptop_remap.conf", "/etc/keyd/laptop_remap.conf"], check=True)
            subprocess.run(["sudo", "keyd", "reload"], check=True)
            
            messagebox.showinfo("Éxito", f"Se aplicaron {reglas_activas} reglas correctamente y se guardaron.\nSolo afectarán a tu laptop.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al aplicar:\n\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyboardRemapperApp(root)
    root.mainloop()