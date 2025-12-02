"""View: GUI components for Channel tab"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from app_theme.dark_theme import ModernDarkTheme
from tabs.common.shared_ui import SharedUI

class ChannelView(SharedUI):
    """Manages all GUI components for Channel calculations"""

    def __init__(self, parent_notebook):
        self.parent_notebook = parent_notebook

        # Create main frame for this tab
        self.frame = tk.Frame(parent_notebook, bg=ModernDarkTheme.BG_FRAME)
        parent_notebook.add(self.frame, text="Κανάλι")

        # Create sub-notebook for channel subtabs
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(expand=True, fill="both")

        # Create all subtabs
        self._create_bsc_subtab()
        self._create_matrix_subtab()
        self._create_chain_subtab()

        # Store matrix widgets
        self.matrix_entries = []
        self.chain_matrix_widgets = []

    # ──────────────────────────────────────────────────────────────────
    # Subtab 1: BSC (Binary Symmetric Channel)
    # ──────────────────────────────────────────────────────────────────

    def _create_bsc_subtab(self):
        """Create BSC capacity subtab"""
        f = tk.Frame(self.notebook, bg=ModernDarkTheme.BG_FRAME)
        self.notebook.add(f, text="BSC")

        # Input section
        self._label(f, "Πιθανότητα σφάλματος e:", 0, 0)

        # CHANGED: Replaced tk.Entry with self._entry
        self.e_entry = self._entry(f, width=10, default="0.1")
        self.e_entry.grid(row=0, column=1, padx=6, pady=4)

        # CHANGED: Replaced tk.Button with self._button
        self.calc_bsc_btn = self._button(f, "Υπολογισμός BSC",
                                         color=ModernDarkTheme.BG_BLUISH)
        self.calc_bsc_btn.grid(row=0, column=2, padx=6, pady=4)

        # Matplotlib figure for plotting
        self.fig = Figure(figsize=(6, 3), dpi=90, facecolor=ModernDarkTheme.BG_FRAME)
        self.ax = self.fig.add_subplot(111, facecolor=ModernDarkTheme.BG_FRAME)
        self.ax.tick_params(axis='x', colors=ModernDarkTheme.WHITE_TEXT)
        self.ax.tick_params(axis='y', colors=ModernDarkTheme.WHITE_TEXT)
        for spine in self.ax.spines.values():
            spine.set_color(ModernDarkTheme.WHITE_TEXT)

        self.canvas = FigureCanvasTkAgg(self.fig, f)
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=3,
                                        padx=6, pady=6, sticky="nsew")

        # Result text area
        self.bsc_result = self._scrolled(f, 6)
        self.bsc_result.grid(row=2, column=0, columnspan=3, padx=6, pady=6, sticky="ew")

        f.grid_rowconfigure(1, weight=1)
        f.grid_columnconfigure(1, weight=1)

    # ──────────────────────────────────────────────────────────────────
    # Subtab 2: Channel Matrix
    # ──────────────────────────────────────────────────────────────────

    def _create_matrix_subtab(self):
        """Create channel matrix subtab"""
        f = tk.Frame(self.notebook, bg=ModernDarkTheme.BG_FRAME)
        self.notebook.add(f, text="Υπολογισμός Χωρητικότητας Διαύλου")

        # Matrix dimensions input
        self._label(f, "Αριθμός Γραμμών:", 0, 0)

        # CHANGED: Replaced tk.Entry with self._entry
        self.rows_entry = self._entry(f, width=10, default="2")
        self.rows_entry.grid(row=0, column=1, padx=6, pady=4, sticky="w")

        self._label(f, "Αριθμός Στηλών:", 1, 0)

        # CHANGED: Replaced tk.Entry with self._entry
        self.cols_entry = self._entry(f, width=10, default="2")
        self.cols_entry.grid(row=1, column=1, padx=6, pady=4, sticky="w")

        # CHANGED: Replaced tk.Button with self._button
        self.create_matrix_btn = self._button(f, "Δημιουργία Πίνακα",
                                              color=ModernDarkTheme.BG_BLUISH)
        self.create_matrix_btn.grid(row=0, column=2, rowspan=2, padx=6, pady=4)

        # Matrix entry frame (will be populated dynamically)
        self.matrix_frame = tk.Frame(f, bg=ModernDarkTheme.BG_FRAME)
        self.matrix_frame.grid(row=2, column=0, columnspan=3, padx=6, pady=6, sticky="nsew")

        # M value input
        self._label(f, "Τιμή Μ(είναι το πλήθος εισόδων ή συμβόλων):", 3, 0)

        # CHANGED: Replaced tk.Entry with self._entry
        self.m_entry = self._entry(f, width=10, default="2")
        self.m_entry.grid(row=3, column=1, padx=6, pady=4, sticky="w")

        # CHANGED: Replaced tk.Button with self._button
        self.calc_capacity_btn = self._button(f, "Υπολογισμός Χωρητικότητας",
                                              color=ModernDarkTheme.BG_LIGHT_ORANGE)
        self.calc_capacity_btn.grid(row=3, column=2, padx=6, pady=4)

        # Result text area
        self.matrix_result = self._scrolled(f, 14)
        self.matrix_result.grid(row=4, column=0, columnspan=3, padx=6, pady=6, sticky="nsew")

        f.grid_columnconfigure(1, weight=1)
        f.grid_rowconfigure(4, weight=1)

    # ──────────────────────────────────────────────────────────────────
    # Subtab 3: Cascaded Channels
    # ──────────────────────────────────────────────────────────────────

    def _create_chain_subtab(self):
        """Create cascaded channels subtab"""
        f = tk.Frame(self.notebook, bg=ModernDarkTheme.BG_FRAME)
        self.notebook.add(f, text="Αλυσίδα Διαύλων Πληροφορίας")

        # Instructions
        instructions = tk.Label(f,
                               text="Δημιουργία αλυσίδας Διαύλων: Πολλαπλασιασμός πινάκων P₁ × P₂ × P₃...",
                               bg=ModernDarkTheme.BG_FRAME, fg=ModernDarkTheme.BG_BLUISH,
                               font=("Consolas", 11, "bold"))
        instructions.grid(row=0, column=0, columnspan=3, padx=6, pady=10)

        # Number of matrices input
        num_frame = tk.Frame(f, bg=ModernDarkTheme.BG_FRAME)
        num_frame.grid(row=1, column=0, columnspan=3, pady=6)

        tk.Label(num_frame, text="Αριθμός Πινάκων:",
                bg=ModernDarkTheme.BG_FRAME, fg=ModernDarkTheme.WHITE_TEXT,
                font=("Consolas", 11)).grid(row=0, column=0, padx=4)

        # CHANGED: Replaced tk.Entry with self._entry
        self.num_matrices_entry = self._entry(num_frame, width=10, default="2")
        self.num_matrices_entry.grid(row=0, column=1, padx=4)

        # CHANGED: Replaced tk.Button with self._button
        self.create_chain_btn = self._button(num_frame, "Δημιουργία Πινάκων",
                                             color=ModernDarkTheme.BG_BLUISH)
        self.create_chain_btn.grid(row=0, column=2, padx=4)

        # Chain matrices frame (will be populated dynamically)
        self.chain_matrices_frame = tk.Frame(f, bg=ModernDarkTheme.BG_FRAME)
        self.chain_matrices_frame.grid(row=2, column=0, columnspan=3,
                                      padx=6, pady=6, sticky="nsew")

        # Calculate chain capacity
        calc_frame = tk.Frame(f, bg=ModernDarkTheme.BG_FRAME)
        calc_frame.grid(row=3, column=0, columnspan=3, pady=6)

        self._label(calc_frame, "Τιμή Μ:", 0, 0)

        # CHANGED: Replaced tk.Entry with self._entry
        self.m_chain_entry = self._entry(calc_frame, width=8, default="2")
        self.m_chain_entry.grid(row=0, column=1, padx=4)

        # CHANGED: Replaced tk.Button with self._button
        self.calc_chain_btn = self._button(calc_frame, "Υπολογισμός Αλυσίδας",
                                           color=ModernDarkTheme.BG_LIGHT_ORANGE)
        self.calc_chain_btn.grid(row=0, column=2, padx=6, pady=4)

        # Result text area
        self.chain_result = self._scrolled(f, 16)
        self.chain_result.grid(row=4, column=0, columnspan=3,
                            padx=6, pady=6, sticky="nsew")

        f.grid_columnconfigure(0, weight=1)
        f.grid_rowconfigure(4, weight=1)
