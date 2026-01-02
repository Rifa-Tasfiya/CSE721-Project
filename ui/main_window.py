from tkinter import *
from tkinter import messagebox

# ---------- Dark Bluish Theme ----------
BG_MAIN     = "#0F172A"   # dark navy
BG_SECTION  = "#1E293B"   # section background
FG_TEXT     = "#E5E7EB"   # light text
FG_LABEL    = "#CBD5E1"
ENTRY_BG    = "#020617"
ENTRY_FG    = "#E5E7EB"

BTN_ENCRYPT = "#2563EB"
BTN_DECRYPT = "#1D4ED8"
BTN_RESET   = "#475569"
BTN_CRACKER = "#4F46E5"


def run_app():
    root = Tk()
    root.title("CSE721 Encryption / Decryption Tool")
    root.geometry("650x680")
    root.config(bg=BG_MAIN)

    # ---------- Title ----------
    Label(
        root,
        text="Encryption / Decryption Tool",
        font=("Arial", 18, "bold"),
        bg=BG_MAIN,
        fg=FG_TEXT
    ).pack(pady=14)

    # ---------- Input ----------
    Label(
        root,
        text="Input Text (Plaintext or Ciphertext):",
        font=("Arial", 11, "bold"),
        bg=BG_MAIN,
        fg=FG_LABEL
    ).pack(anchor="w", padx=22)

    input_box = Text(
        root, font=("Arial", 12),
        bg=BG_SECTION, fg=FG_TEXT,
        insertbackground=FG_TEXT
    )
    input_box.pack(padx=22, pady=6, fill="x")
    input_box.config(height=6)

    # ---------- Options ----------
    frame_opts = Frame(root, bg=BG_MAIN)
    frame_opts.pack(padx=22, pady=14, fill="x")

    Label(
        frame_opts,
        text="Select Cipher:",
        font=("Arial", 11, "bold"),
        bg=BG_MAIN,
        fg=FG_LABEL
    ).grid(row=0, column=0, sticky="w")

    cipher_var = StringVar(value="Caesar Cipher")
    opt = OptionMenu(
        frame_opts,
        cipher_var,
        "Caesar Cipher",
        "Affine Cipher",
        "Playfair Cipher",
        "Hill Cipher (2x2)"
    )
    opt.config(
        bg=BG_SECTION,
        fg=FG_TEXT,
        activebackground="#334155",
        activeforeground=FG_TEXT,
        width=20
    )
    opt["menu"].config(bg=BG_SECTION, fg=FG_TEXT)
    opt.grid(row=0, column=1, sticky="w", padx=12)

    Label(
        frame_opts,
        text="Key:",
        font=("Arial", 11, "bold"),
        bg=BG_MAIN,
        fg=FG_LABEL
    ).grid(row=1, column=0, sticky="w", pady=12)

    key_var = StringVar()
    key_entry = Entry(
        frame_opts,
        textvariable=key_var,
        font=("Arial", 12),
        bg=ENTRY_BG,
        fg=ENTRY_FG,
        insertbackground=ENTRY_FG,
        bd=2
    )
    key_entry.grid(row=1, column=1, sticky="we", padx=12)

    frame_opts.grid_columnconfigure(1, weight=1)

    # ---------- Key Help ----------
    Label(
        root,
        text=(
            "Key format:\n"
            "• Caesar: shift (e.g., 3)\n"
            "• Affine: a,b (e.g., 5,8)\n"
            "• Playfair: keyword (e.g., MONARCHY)\n"
            "• Hill 2x2: a,b,c,d (e.g., 3,3,2,5)"
        ),
        font=("Arial", 10),
        bg=BG_MAIN,
        fg=FG_LABEL,
        justify="left"
    ).pack(anchor="w", padx=22)

    # ---------- Output ----------
    Label(
        root,
        text="Output:",
        font=("Arial", 11, "bold"),
        bg=BG_MAIN,
        fg=FG_LABEL
    ).pack(anchor="w", padx=22, pady=(14, 0))

    output_box = Text(
        root, font=("Arial", 12),
        bg=BG_SECTION, fg=FG_TEXT,
        insertbackground=FG_TEXT
    )
    output_box.pack(padx=22, pady=6, fill="x")
    output_box.config(height=6)

    # ---------- Button Functions (UI placeholders) ----------
    def on_encrypt():
        messagebox.showinfo("Encrypt", f"Encrypt clicked\nCipher: {cipher_var.get()}")

    def on_decrypt():
        messagebox.showinfo("Decrypt", f"Decrypt clicked\nCipher: {cipher_var.get()}")

    def on_reset():
        input_box.delete("1.0", END)
        output_box.delete("1.0", END)
        key_var.set("")
        cipher_var.set("Caesar Cipher")

    def open_hill_cracker_window():
        win = Toplevel(root)
        win.title("Hill Cracker – Known Plaintext Attack")
        win.geometry("520x300")
        win.config(bg=BG_SECTION)

        Label(
            win,
            text="Hill Cipher Cracker (Part 2)",
            font=("Arial", 15, "bold"),
            bg=BG_SECTION,
            fg=FG_TEXT
        ).pack(pady=14)

        Label(
            win,
            text="Known Plaintext Attack UI will be implemented here.",
            font=("Arial", 11),
            bg=BG_SECTION,
            fg=FG_LABEL
        ).pack(pady=10)

        Button(
            win,
            text="Close",
            font=("Arial", 11, "bold"),
            bg=BTN_RESET,
            fg="white",
            width=14,
            command=win.destroy
        ).pack(pady=12)

    # ---------- Buttons ----------
    frame_btn = Frame(root, bg=BG_MAIN)
    frame_btn.pack(pady=22)

    Button(
        frame_btn, text="ENCRYPT",
        font=("Arial", 12, "bold"),
        bg=BTN_ENCRYPT, fg="white",
        activebackground="#1E40AF",
        width=18, command=on_encrypt
    ).grid(row=0, column=0, padx=12, pady=6)

    Button(
        frame_btn, text="DECRYPT",
        font=("Arial", 12, "bold"),
        bg=BTN_DECRYPT, fg="white",
        activebackground="#1E3A8A",
        width=18, command=on_decrypt
    ).grid(row=0, column=1, padx=12, pady=6)

    Button(
        frame_btn, text="RESET",
        font=("Arial", 12, "bold"),
        bg=BTN_RESET, fg="white",
        activebackground="#334155",
        width=18, command=on_reset
    ).grid(row=1, column=0, padx=12, pady=6)

    Button(
        frame_btn, text="HILL CRACKER",
        font=("Arial", 12, "bold"),
        bg=BTN_CRACKER, fg="white",
        activebackground="#312E81",
        width=18, command=open_hill_cracker_window
    ).grid(row=1, column=1, padx=12, pady=6)

    root.mainloop()
