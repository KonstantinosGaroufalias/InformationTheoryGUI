import tkinter as tk
from tkinter import ttk, scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from app_theme.dark_theme import ModernDarkTheme
from tabs.common.shared_ui import SharedUI


class ChannelView(SharedUI):
    def __init__(self, parent_notebook):
        self.parent_notebook = parent_notebook
        self.frame = tk.Frame(parent_notebook, bg=ModernDarkTheme.BG_FRAME)
        parent_notebook.add(self.frame, text="Κανάλι")

        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(expand=True, fill="both")

        self._create_bsc_subtab()
        self._create_matrix_subtab()
        self._create_chain_subtab()

        self.matrix_entries = []
        self.chain_matrices = []
        self.chain_frames = []

    def _create_bsc_subtab(self):
        f = tk.Frame(self.notebook, bg=ModernDarkTheme.BG_FRAME)
        self.notebook.add(f, text="BSC")

        self._label(f, "Πιθανότητα σφάλματος e:", 0, 0)
        self.e_entry = self._entry(f, width=10, default="0.1")
        self.e_entry.grid(row=0, column=1, padx=6, pady=4)

        self.calc_bsc_btn = self._button(f, "Υπολογισμός BSC", color=ModernDarkTheme.BG_BLUISH)
        self.calc_bsc_btn.grid(row=0, column=2, padx=6, pady=4)

        self.fig = Figure(figsize=(6, 3), dpi=90, facecolor=ModernDarkTheme.BG_FRAME)
        self.ax = self.fig.add_subplot(111, facecolor=ModernDarkTheme.BG_FRAME)
        self.ax.tick_params(axis='x', colors=ModernDarkTheme.WHITE_TEXT)
        self.ax.tick_params(axis='y', colors=ModernDarkTheme.WHITE_TEXT)
        for spine in self.ax.spines.values():
            spine.set_color(ModernDarkTheme.WHITE_TEXT)

        self.canvas = FigureCanvasTkAgg(self.fig, f)
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=3, padx=6, pady=6, sticky="nsew")

        self.bsc_result = self._scrolled(f, 6)
        self.bsc_result.grid(row=2, column=0, columnspan=3, padx=6, pady=6, sticky="ew")

        f.grid_rowconfigure(1, weight=1)
        f.grid_columnconfigure(1, weight=1)

    def _create_matrix_subtab(self):
        f = tk.Frame(self.notebook, bg=ModernDarkTheme.BG_FRAME)
        self.notebook.add(f, text="Υπολογισμός Χωρητικότητας Διαύλου")

        self._label(f, "Αριθμός Γραμμών:", 0, 0)
        self.rows_entry = self._entry(f, width=10, default="2")
        self.rows_entry.grid(row=0, column=1, padx=6, pady=4, sticky="w")

        self._label(f, "Αριθμός Στηλών:", 1, 0)
        self.cols_entry = self._entry(f, width=10, default="2")
        self.cols_entry.grid(row=1, column=1, padx=6, pady=4, sticky="w")

        self.create_matrix_btn = self._button(f, "Δημιουργία Πίνακα", color=ModernDarkTheme.BG_BLUISH)
        self.create_matrix_btn.grid(row=0, column=2, rowspan=2, padx=6, pady=4)

        self.matrix_frame = tk.Frame(f, bg=ModernDarkTheme.BG_FRAME)
        self.matrix_frame.grid(row=2, column=0, columnspan=3, padx=6, pady=6, sticky="nsew")

        self._label(f, "Τιμή Μ(είναι το πλήθος εισόδων ή συμβόλων):", 3, 0)
        self.m_entry = self._entry(f, width=10, default="2")
        self.m_entry.grid(row=3, column=1, padx=6, pady=4, sticky="w")

        self.calc_capacity_btn = self._button(f, "Υπολογισμός Χωρητικότητας", color=ModernDarkTheme.BG_LIGHT_ORANGE)
        self.calc_capacity_btn.grid(row=3, column=2, padx=6, pady=4)

        self.matrix_result = self._scrolled(f, 14)
        self.matrix_result.grid(row=4, column=0, columnspan=3, padx=6, pady=6, sticky="nsew")

        f.grid_columnconfigure(1, weight=1)
        f.grid_rowconfigure(4, weight=1)

    def _create_chain_subtab(self):
        f = tk.Frame(self.notebook, bg=ModernDarkTheme.BG_FRAME)
        self.notebook.add(f, text="Αλυσίδα Διαύλων Πληροφορίας")

        instructions = tk.Label(f, text="Δημιουργία αλυσίδας Διαύλων: Πολλαπλασιασμός πινάκων P₁ × P₂ × P₃...",
                                bg=ModernDarkTheme.BG_FRAME, fg=ModernDarkTheme.BG_BLUISH,
                                font=("Consolas", 11, "bold"))
        instructions.grid(row=0, column=0, columnspan=3, padx=6, pady=10)

        # Input for number of matrices
        num_frame = tk.Frame(f, bg=ModernDarkTheme.BG_FRAME)
        num_frame.grid(row=1, column=0, columnspan=3, pady=6)

        tk.Label(num_frame, text="Αριθμός Πινάκων:", bg=ModernDarkTheme.BG_FRAME, fg=ModernDarkTheme.WHITE_TEXT,
                 font=("Consolas", 11)).grid(row=0, column=0, padx=4)
        self.num_matrices_entry = self._entry(num_frame, width=10, default="2")
        self.num_matrices_entry.grid(row=0, column=1, padx=4)

        self.create_chain_btn = self._button(num_frame, "Δημιουργία Πινάκων", color=ModernDarkTheme.BG_BLUISH)
        self.create_chain_btn.grid(row=0, column=2, padx=4)

        # Scrollable container for all chain matrices
        self.chain_container = tk.Frame(f, bg=ModernDarkTheme.BG_FRAME)
        self.chain_container.grid(row=2, column=0, columnspan=3, padx=6, pady=6, sticky="nsew")

        # Calculation section
        calc_frame = tk.Frame(f, bg=ModernDarkTheme.BG_FRAME)
        calc_frame.grid(row=3, column=0, columnspan=3, pady=6)

        self._label(calc_frame, "Τιμή Μ:", 0, 0)
        self.m_chain_entry = self._entry(calc_frame, width=8, default="2")
        self.m_chain_entry.grid(row=0, column=1, padx=4)

        self.calc_chain_btn = self._button(calc_frame, "Υπολογισμός Αλυσίδας", color=ModernDarkTheme.BG_LIGHT_ORANGE)
        self.calc_chain_btn.grid(row=0, column=2, padx=6, pady=4)

        self.chain_result = self._scrolled(f, 16)
        self.chain_result.grid(row=4, column=0, columnspan=3, padx=6, pady=6, sticky="nsew")

        f.grid_columnconfigure(0, weight=1)
        f.grid_rowconfigure(4, weight=1)

    def create_matrix_grid(self, rows, cols):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        self.matrix_entries = []

        tk.Label(self.matrix_frame, text="P(Y|X)", bg=ModernDarkTheme.BG_FRAME, fg=ModernDarkTheme.BG_BLUISH,
                 font=("Consolas", 10, "bold")).grid(row=0, column=0, padx=4, pady=4)

        for j in range(cols):
            tk.Label(self.matrix_frame, text=f"Y{j + 1}", bg=ModernDarkTheme.BG_FRAME, fg=ModernDarkTheme.BG_BLUISH,
                     font=("Consolas", 9, "bold")).grid(row=0, column=j + 1, padx=2)

        for i in range(rows):
            tk.Label(self.matrix_frame, text=f"X{i + 1}", bg=ModernDarkTheme.BG_FRAME, fg=ModernDarkTheme.BG_BLUISH,
                     font=("Consolas", 9, "bold")).grid(row=i + 1, column=0, padx=4)

            row_entries = []
            for j in range(cols):
                entry = tk.Entry(self.matrix_frame, width=7, bg=ModernDarkTheme.BG_FRAME, fg=ModernDarkTheme.WHITE_TEXT,
                                 font=("Consolas", 9), justify='center', insertbackground=ModernDarkTheme.WHITE_TEXT)
                entry.insert(0, f"{1.0 / cols:.2f}")
                entry.grid(row=i + 1, column=j + 1, padx=2, pady=2)
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)

    def create_chain_matrices(self, num_matrices):
        for widget in self.chain_container.winfo_children():
            widget.destroy()

        self.chain_matrices = []
        self.chain_frames = []

        for idx in range(num_matrices):
            matrix_frame = tk.LabelFrame(self.chain_container, text=f"Πίνακας {idx + 1}",
                                         bg=ModernDarkTheme.BG_FRAME, fg=ModernDarkTheme.BG_BLUISH,
                                         font=("Consolas", 10, "bold"))
            matrix_frame.grid(row=idx, column=0, padx=10, pady=8, sticky="ew")

            dims_frame = tk.Frame(matrix_frame, bg=ModernDarkTheme.BG_FRAME)
            dims_frame.pack(pady=4)

            tk.Label(dims_frame, text="Γραμμές:", bg=ModernDarkTheme.BG_FRAME, fg=ModernDarkTheme.WHITE_TEXT,
                     font=("Consolas", 9)).grid(row=0, column=0, padx=2)
            rows_entry = self._entry(dims_frame, width=5, default="2")
            rows_entry.grid(row=0, column=1, padx=2)

            tk.Label(dims_frame, text="Στήλες:", bg=ModernDarkTheme.BG_FRAME, fg=ModernDarkTheme.WHITE_TEXT,
                     font=("Consolas", 9)).grid(row=0, column=2, padx=2)
            cols_entry = self._entry(dims_frame, width=5, default="2")
            cols_entry.grid(row=0, column=3, padx=2)

            grid_container = tk.Frame(matrix_frame, bg=ModernDarkTheme.BG_FRAME)
            grid_container.pack(pady=4)

            self.chain_frames.append({
                'rows_entry': rows_entry,
                'cols_entry': cols_entry,
                'grid_container': grid_container,
                'matrix_entries': []
            })

            create_btn = self._button(dims_frame, "Δημιουργία", color=ModernDarkTheme.BG_BLUISH)
            create_btn.grid(row=0, column=4, padx=4)

            create_btn.config(command=lambda i=idx: self.create_single_chain_matrix(i))

    def create_single_chain_matrix(self, matrix_idx):
        frame_data = self.chain_frames[matrix_idx]

        try:
            rows = int(frame_data['rows_entry'].get())
            cols = int(frame_data['cols_entry'].get())

            if rows <= 0 or cols <= 0:
                return False, "Θετικοί αριθμοί μόνο!"

            for widget in frame_data['grid_container'].winfo_children():
                widget.destroy()

            frame_data['matrix_entries'] = []

            for i in range(rows):
                row_entries = []
                for j in range(cols):
                    entry = tk.Entry(frame_data['grid_container'], width=8, bg=ModernDarkTheme.BG_ENTRY,fg=ModernDarkTheme.WHITE_TEXT, font=("Consolas", 9), justify='center',
                                     insertbackground=ModernDarkTheme.WHITE_TEXT)
                    entry.insert(0, f"{1.0 / cols:.2f}")
                    entry.grid(row=i, column=j, padx=2, pady=2)
                    row_entries.append(entry)
                frame_data['matrix_entries'].append(row_entries)

            return True, ""
        except ValueError:
            return False, "Έγκυροι ακέραιοι απαιτούνται!"

    def update_bsc_plot(self, x_vals, y_vals, e, C):
        self.ax.clear()

        self.ax.set_facecolor(ModernDarkTheme.BG_FRAME)
        self.ax.plot(x_vals, y_vals, color=ModernDarkTheme.BG_BLUISH, lw=2, label='C_BSC(e)')
        self.ax.axvline(e, color=ModernDarkTheme.BG_LIGHT_ORANGE, ls="--", lw=1.5, label=f'e={e}')

        self.ax.set_xlabel("Πιθανότητα σφάλματος (e)", color=ModernDarkTheme.WHITE_TEXT, fontsize=10)
        self.ax.set_ylabel("Χωρητικότητα (bits/symbol)", color=ModernDarkTheme.WHITE_TEXT, fontsize=10)

        self.ax.set_title("BSC Graphic", color=ModernDarkTheme.WHITE_TEXT, fontsize=12)

        self.ax.legend(facecolor=ModernDarkTheme.BG_FRAME, edgecolor=ModernDarkTheme.WHITE_TEXT,labelcolor=ModernDarkTheme.WHITE_TEXT)
        self.ax.grid(True, alpha=0.2, color=ModernDarkTheme.WHITE_TEXT)
        self.canvas.draw()

    def display_bsc_result(self, e, C):
        self.bsc_result.delete("1.0", tk.END)
        self.bsc_result.insert(tk.END, "Δυαδικό συμμετρικό κανάλι (BSC)\n")
        self.bsc_result.insert(tk.END, f"e = {e}\n")
        self.bsc_result.insert(tk.END, f"Χωρητικότητα του BSC: C_BSC(e) = {C:.4f} bits/symbol\n")

    def display_matrix_creation_success(self, rows, cols):
        self.matrix_result.delete("1.0", tk.END)
        self.matrix_result.insert(tk.END, f"Ο Πίνακας {rows}×{cols} δημιουργήθηκε με επιτυχία!\n\n")
        self.matrix_result.insert(tk.END, "Σημείωση: Κάθε γραμμή πρέπει να αθροίζει σε 1\n")
        self.matrix_result.insert(tk.END, "Πίνακας P(Y|X)\n")

    def display_capacity_result(self, P_YX, m, capacity):
        self.matrix_result.delete("1.0", tk.END)
        self.matrix_result.insert(tk.END, "--- Αποτελέσματα ---\n")
        self.matrix_result.insert(tk.END, "\nΧωρητικότητα Διαύλου\n")
        self.matrix_result.insert(tk.END, "Πίνακας Καναλιού P(Y|X):\n")
        self.matrix_result.insert(tk.END, f"{P_YX}\n\n")
        self.matrix_result.insert(tk.END, f"M = {m}\n\n")
        self.matrix_result.insert(tk.END, f"Χωρητικότητα: C = {capacity:.4f} bits/symbol\n\n")

    def display_chain_frames_created(self, num_matrices):
        self.chain_result.delete("1.0", tk.END)
        self.chain_result.insert(tk.END, f"Δημιουργήθηκαν {num_matrices} πλαίσια πινάκων!\n\n")
        self.chain_result.insert(tk.END, "Ορίστε διαστάσεις και πατήστε 'Δημιουργία'\nγια κάθε πίνακα.\n")

    def display_chain_result(self, matrices, P_combined, m, capacity):
        self.chain_result.delete("1.0", tk.END)
        self.chain_result.insert(tk.END, "--- Αποτελέσματα ---\n")
        self.chain_result.insert(tk.END, "\nΑΛΥΣΙΔΑ ΚΑΝΑΛΙΩΝ\n")

        for idx, matrix in enumerate(matrices):
            self.chain_result.insert(tk.END, f"Πίνακας P{idx + 1}:\n")
            self.chain_result.insert(tk.END, f"{matrix}\n\n")

        self.chain_result.insert(tk.END, "Τελικός Πίνακας (P₁ × P₂ × ..... × Pₙ):\n")
        self.chain_result.insert(tk.END, f"{P_combined}\n\n")
        self.chain_result.insert(tk.END, f"M = {m}\n\n")
        self.chain_result.insert(tk.END, f"Χωρητικότητα Αλυσίδας: C = {capacity:.4f} bits/symbol\n\n")
