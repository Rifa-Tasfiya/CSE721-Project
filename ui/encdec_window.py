from tkinter import *
from tkinter import messagebox
from ciphers.caeser import encryption_ceaser, decryption_ceaser
from ciphers.affine import affine_encrypt, affine_decrypt
from ciphers.playfair import playfair_encrypt, playfair_decrypt
from ciphers.hill2x2 import hill_encrypt, hill_decrypt




# Dark theme
BG_MAIN     = "#0F172A"
BG_SECTION  = "#1E293B"
FG_TEXT     = "#E5E7EB"
FG_LABEL    = "#CBD5E1"
ENTRY_BG    = "#020617"
ENTRY_FG    = "#E5E7EB"

BTN_ENCRYPT = "#2563EB"
BTN_DECRYPT = "#1D4ED8"
BTN_RESET   = "#475569"
BTN_BACK    = "#334155"


def open_encdec_window(parent):
    # Hide home window
    parent.withdraw()

    win = Toplevel(parent)
    win.title("Encryption / Decryption Tool")
    win.geometry("650x680")
    win.config(bg=BG_MAIN)

    def on_close():
        win.destroy()
        parent.deiconify()

    win.protocol("WM_DELETE_WINDOW", on_close)

    Label(
        win,
        text="Encryption / Decryption Tool",
        font=("Arial", 18, "bold"),
        bg=BG_MAIN,
        fg=FG_TEXT
    ).pack(pady=14)

    # Input
    Label(
        win, text="Input Text (Plaintext or Ciphertext):",
        font=("Arial", 11, "bold"),
        bg=BG_MAIN, fg=FG_LABEL
    ).pack(anchor="w", padx=22)

    input_box = Text(
        win, font=("Arial", 12),
        bg=BG_SECTION, fg=FG_TEXT,
        insertbackground=FG_TEXT
    )
    input_box.pack(padx=22, pady=6, fill="x")
    input_box.config(height=5)

    # Options frame
    frame_opts = Frame(win, bg=BG_MAIN)
    frame_opts.pack(padx=22, pady=14, fill="x")

    Label(
        frame_opts, text="Select Cipher:",
        font=("Arial", 11, "bold"),
        bg=BG_MAIN, fg=FG_LABEL
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
        bg=BG_SECTION, fg=FG_TEXT,
        activebackground="#334155",
        activeforeground=FG_TEXT,
        width=20
    )
    opt["menu"].config(bg=BG_SECTION, fg=FG_TEXT)
    opt.grid(row=0, column=1, sticky="w", padx=12)

    Label(
        frame_opts, text="Key:",
        font=("Arial", 11, "bold"),
        bg=BG_MAIN, fg=FG_LABEL
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

    Label(
        win,
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

    # Output
    Label(
        win, text="Output:",
        font=("Arial", 11, "bold"),
        bg=BG_MAIN, fg=FG_LABEL
    ).pack(anchor="w", padx=22, pady=(14, 0))

    output_box = Text(
        win, font=("Arial", 12),
        bg=BG_SECTION, fg=FG_TEXT,
        insertbackground=FG_TEXT
    )
    output_box.pack(padx=22, pady=6, fill="x")
    output_box.config(height=6)

    # Placeholder handlers
    def on_encrypt():
        text = input_box.get("1.0", END).strip()
        cipher = cipher_var.get()
        key = key_var.get().strip()

        # ---------- Caesar Cipher ----------
        if cipher == "Caesar Cipher":
            try:
                shift = int(key)
                result = encryption_ceaser(text, shift)

                output_box.delete("1.0", END)
                output_box.insert(END, result)

            except ValueError:
                messagebox.showerror(
                    "Error",
                    "For Caesar cipher, key must be an integer (e.g., 3)."
                )

        # ---------- Affine Cipher ----------
        elif cipher == "Affine Cipher":
            try:
                key = key.replace(" ", "")

                if "," not in key:
                    raise ValueError

                parts = key.split(",")

                if len(parts) != 2:
                    raise ValueError

                a = int(parts[0])
                b = int(parts[1])

                result = affine_encrypt(text, a, b)

                if "Invalid key" in result:
                    messagebox.showerror("Error", result)
                    return

                output_box.delete("1.0", END)
                output_box.insert(END, result)

            except ValueError:
                messagebox.showerror(
                    "Error",
                    "For Affine cipher, key must be in format a,b (e.g., 5,8)."
                )

        # ---------- Playfair Cipher ----------
        elif cipher == "Playfair Cipher":
            if key == "":
                messagebox.showerror(
                    "Error",
                    "Playfair cipher requires a keyword."
                )
                return

            try:
                result = playfair_encrypt(text, key)

                output_box.delete("1.0", END)
                output_box.insert(END, result)

            except Exception:
                messagebox.showerror(
                    "Error",
                    "Playfair encryption failed."
                )

        # ---------- Hill Cipher (2x2) ----------
        elif cipher == "Hill Cipher (2x2)":
            try:
                key = key.replace(" ", "")

                if "," not in key:
                    raise ValueError

                parts = key.split(",")

                if len(parts) != 4:
                    raise ValueError

                a = int(parts[0])
                b = int(parts[1])
                c = int(parts[2])
                d = int(parts[3])

                result = hill_encrypt(text, a, b, c, d)

                if "Invalid" in result:
                    messagebox.showerror("Error", result)
                    return

                output_box.delete("1.0", END)
                output_box.insert(END, result)

            except ValueError:
                messagebox.showerror(
                    "Error",
                    "For Hill 2x2, key must be in format a,b,c,d (e.g., 3,3,2,5)."
                )

            except Exception:
                messagebox.showerror(
                    "Error",
                    "Hill encryption failed."
                )

        # ---------- Not Implemented ----------
        else:
            messagebox.showinfo(
                "Info",
                "This cipher is not connected yet."
            )
       

    def on_decrypt():
        text = input_box.get("1.0", END).strip()
        cipher = cipher_var.get()
        key = key_var.get().strip()

        # ---------- Caesar Cipher ----------
        if cipher == "Caesar Cipher":
            try:
                shift = int(key)
                result = decryption_ceaser(text, shift)

                output_box.delete("1.0", END)
                output_box.insert(END, result)

            except ValueError:
                messagebox.showerror(
                    "Error",
                    "For Caesar cipher, key must be an integer (e.g., 3)."
                )

        # ---------- Affine Cipher ----------
        elif cipher == "Affine Cipher":
            try:
                key = key.replace(" ", "")

                if "," not in key:
                    raise ValueError

                parts = key.split(",")

                if len(parts) != 2:
                    raise ValueError

                a = int(parts[0])
                b = int(parts[1])

                result = affine_decrypt(text, a, b)

                if "Invalid key" in result:
                    messagebox.showerror("Error", result)
                    return

                output_box.delete("1.0", END)
                output_box.insert(END, result)

            except ValueError:
                messagebox.showerror(
                    "Error",
                    "For Affine cipher, key must be in format a,b (e.g., 5,8)."
                )

        # ---------- Playfair Cipher ----------
        elif cipher == "Playfair Cipher":
            if key == "":
                messagebox.showerror(
                    "Error",
                    "Playfair cipher requires a keyword."
                )
                return

            try:
                result = playfair_decrypt(text, key)

                output_box.delete("1.0", END)
                output_box.insert(END, result)

            except Exception:
                messagebox.showerror(
                    "Error",
                    "Playfair decryption failed."
                )

        # ---------- Hill Cipher (2x2) ----------
        elif cipher == "Hill Cipher (2x2)":
            try:
                key = key.replace(" ", "")

                if "," not in key:
                    raise ValueError

                parts = key.split(",")

                if len(parts) != 4:
                    raise ValueError

                a = int(parts[0])
                b = int(parts[1])
                c = int(parts[2])
                d = int(parts[3])

                result = hill_decrypt(text, a, b, c, d)

                if "Invalid" in result:
                    messagebox.showerror("Error", result)
                    return

                output_box.delete("1.0", END)
                output_box.insert(END, result)

            except ValueError:
                messagebox.showerror(
                    "Error",
                    "For Hill 2x2, key must be in format a,b,c,d (e.g., 3,3,2,5)."
                )

            except Exception:
                messagebox.showerror(
                    "Error",
                    "Hill decryption failed."
                )

        # ---------- Not Implemented ----------
        else:
            messagebox.showinfo(
                "Info",
                "This cipher is not connected yet."
            )



    def on_reset():
        input_box.delete("1.0", END)
        output_box.delete("1.0", END)
        key_var.set("")
        cipher_var.set("Caesar Cipher")

    # Buttons
    frame_btn = Frame(win, bg=BG_MAIN)
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
        frame_btn, text="BACK",
        font=("Arial", 12, "bold"),
        bg=BTN_BACK, fg="white",
        activebackground="#1F2937",
        width=18, command=on_close
    ).grid(row=1, column=1, padx=12, pady=6)
