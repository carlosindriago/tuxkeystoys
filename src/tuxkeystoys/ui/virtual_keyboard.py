import customtkinter as ctk

# Diseño del teclado virtual
VK_LAYOUT = [
    ["Esc", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"],
    ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "Bksp"],
    ["Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\"],
    ["Caps", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "Enter"],
    ["LShift", "< >", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "RShift"],
    ["LCtrl", "Super/Win", "LAlt", "Space", "RAlt", "RCtrl", "Left", "Up", "Down", "Right"]
]

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


FONT_FAMILY = "Roboto"
COLOR_MODIFIER = ("#E5E7EB", "#2B2B2B") # Color para teclas de modificación (Shift, Ctrl, etc.)

class VirtualKeyboardDialog:
    def __init__(self, parent, title: str, callback):
        self.top = ctk.CTkToplevel(parent)
        self.top.title(title)
        self.top.geometry("950x450")
        self.top.minsize(900, 420)
        self.top.transient(parent)
        self.callback = callback
        
        self.is_chord_mode = ctk.BooleanVar(value=False)
        self.current_chord = []
        self.current_chord_display = []
        
        header_frame = ctk.CTkFrame(self.top, fg_color="transparent")
        header_frame.pack(fill="x", pady=(20, 5))
        
        lbl = ctk.CTkLabel(header_frame, text="🖱️ Haz clic en una tecla o ⌨️ Presiónala físicamente", font=ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold"))
        lbl.pack()

        top_bar = ctk.CTkFrame(self.top, fg_color=("#F9FAFB", "#212121"), corner_radius=8)
        top_bar.pack(fill="x", padx=30, pady=(10, 15), ipady=5)
        
        chord_cb = ctk.CTkCheckBox(top_bar, text="Modo Combinación (ej. Ctrl + C)", variable=self.is_chord_mode, 
                                   command=self.on_chord_mode_change, font=ctk.CTkFont(family=FONT_FAMILY, size=13))
        chord_cb.pack(side="left", padx=15)
        
        self.chord_display_lbl = ctk.CTkLabel(top_bar, text="Combinación: (ninguna)", font=ctk.CTkFont(family=FONT_FAMILY, size=14, slant="italic"), text_color=("#2563EB", "#60A5FA"))
        self.chord_display_lbl.pack(side="left", padx=20)
        
        self.btn_save_chord = ctk.CTkButton(top_bar, text="💾 Guardar", fg_color="#059669", hover_color="#047857", 
                                            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
                                            command=self.save_chord, state="disabled")
        self.btn_save_chord.pack(side="right", padx=15)

        # Contenedor del teclado centrado
        kb_container = ctk.CTkFrame(self.top, fg_color="transparent")
        kb_container.pack(expand=True)

        kb_frame = ctk.CTkFrame(kb_container, fg_color=("#E5E7EB", "#1A1A1A"), corner_radius=12, border_width=1, border_color=("#D1D5DB", "#333333"))
        kb_frame.pack(padx=10, pady=10, ipadx=10, ipady=10)

        modifiers = ["Esc", "Bksp", "Tab", "Caps", "Enter", "LShift", "RShift", "LCtrl", "LAlt", "Super/Win", "RAlt", "RCtrl"]

        for row in VK_LAYOUT:
            row_frame = ctk.CTkFrame(kb_frame, fg_color="transparent")
            row_frame.pack(side="top", pady=3)
            for key in row:
                width = 48
                if key == "Space":
                    width = 300
                elif key in ["Enter", "LShift", "RShift", "Caps", "Bksp", "Tab", "Super/Win", "LCtrl", "RCtrl", "LAlt", "RAlt"]:
                    width = 85
                elif key in ["Up", "Down", "Left", "Right"]:
                    width = 50
                
                # Color especial para modificadores vs teclas normales
                btn_color = COLOR_MODIFIER if key in modifiers else ("#FFFFFF", "#3A3A3A")
                text_col = ("black", "white")
                hover_col = ("#D1D5DB", "#4D4D4D")
                
                if key == "Space":
                    btn_color = ("#FFFFFF", "#3A3A3A")
                
                btn = ctk.CTkButton(row_frame, text=key, width=width, height=45, corner_radius=6,
                                    font=ctk.CTkFont(family=FONT_FAMILY, size=13),
                                    fg_color=btn_color, hover_color=hover_col, 
                                    text_color=text_col,
                                    border_width=1, border_color=("#D1D5DB", "#444444"),
                                    command=lambda k=key: self.on_virtual_click(k))
                btn.pack(side="left", padx=3)

        self.top.bind("<KeyPress>", self.on_physical_keypress)
        self.top.focus_set()
        
        self.top.after(100, self.top.grab_set)

    def on_chord_mode_change(self):
        if not self.is_chord_mode.get():
            self.current_chord = []
            self.current_chord_display = []
            self.chord_display_lbl.configure(text="Combinación: (ninguna)")
            self.btn_save_chord.configure(state="disabled")
        self.top.focus_set()

    def add_to_chord(self, display_name: str, keyd_name: str):
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

    def on_virtual_click(self, key_label: str):
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
