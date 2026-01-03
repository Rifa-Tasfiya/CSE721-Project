from tkinter import *
from tkinter import messagebox


from attacks.hill_known_plaintext import recover_hill2x2_key_from_strings


# Dark theme
BG_MAIN     = "#0F172A"
BG_SECTION  = "#1E293B"
FG_TEXT     = "#E5E7EB"
FG_LABEL    = "#CBD5E1"
ENTRY_BG    = "#020617"
ENTRY_FG    = "#E5E7EB"

BTN_RUN     = "#4F46E5"
BTN_RESET   = "#475569"
BTN_BACK    = "#334155"


def open_cracker_window(parent):
    parent.withdraw()

    win = Toplevel(parent)
    win.title("Hill Cipher Cracker (Known Plaintext Attack)")
    win.geometry("650x560")
    win.config(bg=BG_MAIN)

    def on_close():
        win.destroy()
        parent.deiconify()

    win.protocol("WM_DELETE_WINDOW", on_close)

    Label(
        win,
        text="Cracker Tool: Hill Cipher (Known Plaintext Attack)",
        font=("Arial", 15, "bold"),
        bg=BG_MAIN,
        fg=FG_TEXT
    ).pack(pady=14)

    Label(
        win,
        text="Enter multiple plaintexts and ciphertexts separated by commas.\n(Example: meetme, attacknow)",
        font=("Arial", 10),
        bg=BG_MAIN,
        fg=FG_LABEL
    ).pack(pady=6)

    frame = Frame(win, bg=BG_MAIN)
    frame.pack(padx=22, pady=14, fill="x")

    def labeled_entry(r, label):
        Label(
            frame,
            text=label,
            font=("Arial", 11, "bold"),
            bg=BG_MAIN,
            fg=FG_LABEL
        ).grid(row=r, column=0, sticky="w", pady=8)

        v = StringVar()
        e = Entry(
            frame,
            textvariable=v,
            font=("Arial", 12),
            bg=ENTRY_BG,
            fg=ENTRY_FG,
            insertbackground=ENTRY_FG,
            bd=2
        )
        e.grid(row=r, column=1, sticky="we", padx=12, pady=8)
        return v

    frame.grid_columnconfigure(1, weight=1)

    
    plain_csv = labeled_entry(0, "Known Plaintexts (comma-separated):")
    cipher_csv = labeled_entry(1, "Known Ciphertexts (comma-separated):")

    Label(
        win,
        text="Output (Recovered Key Matrix):",
        font=("Arial", 11, "bold"),
        bg=BG_MAIN,
        fg=FG_LABEL
    ).pack(anchor="w", padx=22, pady=(10, 0))

    output_box = Text(
        win,
        font=("Arial", 12),
        bg=BG_SECTION,
        fg=FG_TEXT,
        insertbackground=FG_TEXT
    )
    output_box.pack(padx=22, pady=8, fill="x")
    output_box.config(height=8)

    def on_run():
        pt_csv = plain_csv.get().strip()
        ct_csv = cipher_csv.get().strip()

        output_box.delete("1.0", END)

        key_matrix, msg = recover_hill2x2_key_from_strings(pt_csv, ct_csv)

        if key_matrix is None:
            messagebox.showerror("Error", msg)
            output_box.insert(END, msg)
            return

        output_box.insert(END, msg + "\n\n")
        output_box.insert(END, "Recovered Key Matrix (mod 26):\n")
        output_box.insert(END, f"[{int(key_matrix[0,0])}  {int(key_matrix[0,1])}]\n")
        output_box.insert(END, f"[{int(key_matrix[1,0])}  {int(key_matrix[1,1])}]\n")

    def on_reset():
        plain_csv.set("")
        cipher_csv.set("")
        output_box.delete("1.0", END)

    frame_btn = Frame(win, bg=BG_MAIN)
    frame_btn.pack(pady=16)

    Button(
        frame_btn,
        text="RUN",
        font=("Arial", 12, "bold"),
        bg=BTN_RUN,
        fg="white",
        activebackground="#312E81",
        width=18,
        command=on_run
    ).grid(row=0, column=0, padx=12, pady=6)

    Button(
        frame_btn,
        text="RESET",
        font=("Arial", 12, "bold"),
        bg=BTN_RESET,
        fg="white",
        activebackground="#334155",
        width=18,
        command=on_reset
    ).grid(row=0, column=1, padx=12, pady=6)

    Button(
        frame_btn,
        text="BACK",
        font=("Arial", 12, "bold"),
        bg=BTN_BACK,
        fg="white",
        activebackground="#1F2937",
        width=18,
        command=on_close
    ).grid(row=1, column=0, columnspan=2, padx=12, pady=6)
