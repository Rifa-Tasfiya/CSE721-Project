from tkinter import *
from ui.encdec_window import open_encdec_window
from ui.cracker_window import open_cracker_window

# Dark theme
BG_MAIN = "#0F172A"
BG_PANEL = "#1E293B"
FG_TEXT = "#E5E7EB"
FG_LABEL = "#CBD5E1"

BTN_PRIMARY = "#2563EB"   # blue
BTN_SECONDARY = "#4F46E5" # indigo
BTN_EXIT = "#475569"      # slate


def run_home():
    root = Tk()
    root.title("CSE721 Crypto Tool")
    root.geometry("520x360")
    root.config(bg=BG_MAIN)

    Label(
        root,
        text="CSE721 Encryption/Decryption Project",
        font=("Arial", 15, "bold"),
        bg=BG_MAIN,
        fg=FG_TEXT
    ).pack(pady=20)

    Label(
        root,
        text="Choose an option to continue:",
        font=("Arial", 11),
        bg=BG_MAIN,
        fg=FG_LABEL
    ).pack(pady=5)

    panel = Frame(root, bg=BG_PANEL)
    panel.pack(padx=20, pady=20, fill="both", expand=True)

    def go_encdec():
        open_encdec_window(root)

    def go_cracker():
        open_cracker_window(root)

    Button(
        panel,
        text="Encryption / Decryption Tool",
        font=("Arial", 12, "bold"),
        bg=BTN_PRIMARY,
        fg="white",
        activebackground="#1E40AF",
        width=28,
        height=2,
        command=go_encdec
    ).pack(pady=18)

    Button(
        panel,
        text="Cracker Tool (Hill Cipher)",
        font=("Arial", 12, "bold"),
        bg=BTN_SECONDARY,
        fg="white",
        activebackground="#312E81",
        width=28,
        height=2,
        command=go_cracker
    ).pack(pady=10)

    Button(
        root,
        text="Exit",
        font=("Arial", 11, "bold"),
        bg=BTN_EXIT,
        fg="white",
        activebackground="#334155",
        width=10,
        command=root.destroy
    ).pack(pady=12)

    root.mainloop()
