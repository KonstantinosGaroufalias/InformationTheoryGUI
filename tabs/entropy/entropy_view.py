"""View: GUI components for Entropy tab"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from app_theme.dark_theme import ModernDarkTheme
from tabs.common.shared_ui import SharedUI

class EntropyView(SharedUI):
    """Manages all GUI components for Entropy calculations"""

    def __init__(self, parent_notebook):
        self.parent_notebook = parent_notebook

        # Create main frame for this tab
        self.frame = tk.Frame(parent_notebook, bg=ModernDarkTheme.BG_FRAME)
        parent_notebook.add(self.frame, text="Εντροπία")

        # Create sub-notebook for entropy subtabs
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(expand=True, fill="both")

        # Create all subtabs
        self._create_entropy_subtab()
        self._create_kl_subtab()
        self._create_joint_subtab()
        self._create_mutual_info_subtab()
        self._create_conditional_subtab()
    # ──────────────────────────────────────────────────────────────────
    # Subtab 1: Basic Entropy H(X)
    # ──────────────────────────────────────────────────────────────────

    def _create_entropy_subtab(self):
        """Create basic entropy H(X) subtab"""
        f = tk.Frame(self.notebook, bg=ModernDarkTheme.BG_FRAME)
        self.notebook.add(f, text="Εντροπία H(X)")

        self._label(f, "Πιθανότητες (με κενό):", 0, 0)

        # CHANGED: Replaced tk.Entry with self._entry
        self.prob_entry = self._entry(f, width=40, default="0.5 0.3 0.2")
        self.prob_entry.grid(row=0, column=1, padx=6, pady=4, sticky="ew")

        # CHANGED: Replaced tk.Button with self._button
        self.calc_entropy_btn = self._button(f, "Υπολογισμός Εντροπίας" ,color=ModernDarkTheme.BG_BLUISH)
        self.calc_entropy_btn.grid(row=0, column=2, padx=6, pady=4)

        self.result_text = self._scrolled(f, 18)
        self.result_text.grid(row=1, column=0, columnspan=3, padx=6, pady=6, sticky="nsew")

        f.grid_columnconfigure(1, weight=1)
        f.grid_rowconfigure(1, weight=1)

    # ──────────────────────────────────────────────────────────────────
    # Subtab 2: KL Divergence
    # ──────────────────────────────────────────────────────────────────

    def _create_kl_subtab(self):
        """Create KL Divergence subtab"""
        f = tk.Frame(self.notebook, bg=ModernDarkTheme.BG_FRAME)
        self.notebook.add(f, text="KL Απόκλιση D_KL(Q||P)")

        self._label(f, "Κατανομή P:", 0, 0)
        self._label(f, "Κατανομή Q:", 1, 0)

        # CHANGED: Replaced tk.Entry with self._entry
        self.P_entry = self._entry(f, width=30, default="0.48 0.52")
        self.P_entry.grid(row=0, column=1, padx=6, pady=4, sticky="ew")

        # CHANGED: Replaced tk.Entry with self._entry
        self.Q_entry = self._entry(f, width=30, default="0.5 0.5")
        self.Q_entry.grid(row=1, column=1, padx=6, pady=4, sticky="ew")

        # CHANGED: Replaced tk.Button with self._button
        self.calc_kl_btn = self._button(f, "Υπολογισμός KL (P||Q)" , color=ModernDarkTheme.BG_BLUISH)
        self.calc_kl_btn.grid(row=0, column=2, rowspan=2, padx=6, pady=4)

        self.kl_result_text = self._scrolled(f, 14)
        self.kl_result_text.grid(row=2, column=0, columnspan=3, padx=6, pady=6, sticky="nsew")

        f.grid_columnconfigure(1, weight=1)
        f.grid_rowconfigure(2, weight=1)

    # ──────────────────────────────────────────────────────────────────
    # Subtab 3: Joint Entropy
    # ──────────────────────────────────────────────────────────────────

    def _create_joint_subtab(self):
        """Create Joint Entropy subtab"""
        f = tk.Frame(self.notebook, bg=ModernDarkTheme.BG_FRAME)
        self.notebook.add(f, text="Συνδετική Εντροπία H(XY)")

        self._label(f, "Πιθανότητες Px (με κενό):", 0, 0)

        # CHANGED: Replaced tk.Entry with self._entry
        self.px_entry = self._entry(f, width=30, default="0.5 0.3 0.2")
        self.px_entry.grid(row=0, column=1, padx=6, pady=4, sticky="ew")

        self._label(f, "Πιθανότητες Py (με κενό):", 1, 0)

        # CHANGED: Replaced tk.Entry with self._entry
        self.py_entry = self._entry(f, width=30, default="0.6 0.25 0.15")
        self.py_entry.grid(row=1, column=1, padx=6, pady=4, sticky="ew")

        # CHANGED: Replaced tk.Button with self._button
        self.calc_joint_btn = self._button(f, "Υπολογισμός Συνδετικής Εντροπίας" ,color=ModernDarkTheme.BG_LIGHT_ORANGE)
        self.calc_joint_btn.grid(row=0, column=2, rowspan=2, padx=6, pady=4)

        self.joint_result_text = self._scrolled(f, 14)
        self.joint_result_text.grid(row=2, column=0, columnspan=3, padx=6, pady=6, sticky="nsew")

        f.grid_columnconfigure(1, weight=1)
        f.grid_rowconfigure(2, weight=1)


    # NEW SUBTAB: Mutual Information I(X;Y)
    def _create_mutual_info_subtab(self):
        """Create Διαπληροφορία I(X;Y) subtab"""
        f = tk.Frame(self.notebook, bg=ModernDarkTheme.BG_FRAME)
        self.notebook.add(f, text="Διαπληροφορία I(X;Y)")  # <── NEW TAB TITLE

        self._label(f, "Πιθανότητες Px (με κενό):", 0, 0)
        self.mi_px_entry = self._entry(f, width=30, default="0.2 0.8")  # <── NEW ENTRY
        self.mi_px_entry.grid(row=0, column=1, padx=6, pady=4, sticky="ew")

        self._label(f, "Πιθανότητες Py (με κενό):", 1, 0)
        self.mi_py_entry = self._entry(f, width=30, default="0.3 0.7")  # <── NEW ENTRY
        self.mi_py_entry.grid(row=1, column=1, padx=6, pady=4, sticky="ew")

        # Button to trigger mutual information calculation
        self.calc_mi_btn = self._button(f,"Υπολογισμός Διαπληροφορίας",color=ModernDarkTheme.BG_LIGHT_ORANGE)  # <── NEW BUTTON
        self.calc_mi_btn.grid(row=0, column=2, rowspan=2, padx=6, pady=4)

        # Output box
        self.mi_result_text = self._scrolled(f, 14)  # <── NEW TEXT
        self.mi_result_text.grid(row=2, column=0, columnspan=3, padx=6, pady=6, sticky="nsew")

        f.grid_columnconfigure(1, weight=1)
        f.grid_rowconfigure(2, weight=1)

    # NEW SUBTAB: Conditional Entropy H(Y|X), H(X|Y)
    def _create_conditional_subtab(self):
        """Create Υπό Συνθήκη Εντροπία subtab"""
        f = tk.Frame(self.notebook, bg=ModernDarkTheme.BG_FRAME)
        self.notebook.add(f, text="Υπο-Συνθήκη Εντροπία")  # <── NEW TAB TITLE

        self._label(f, "Πιθανότητες Px (με κενό):", 0, 0)
        self.cond_px_entry = self._entry(f, width=30, default="0.5 0.3 0.2")
        self.cond_px_entry.grid(row=0, column=1, padx=6, pady=4, sticky="ew")

        self._label(f, "Πιθανότητες Py (με κενό):", 1, 0)
        self.cond_py_entry = self._entry(f, width=30, default="0.6 0.25 0.15")
        self.cond_py_entry.grid(row=1, column=1, padx=6, pady=4, sticky="ew")

        # Button to trigger conditional entropy calculation
        self.calc_cond_btn = self._button(f,"Υπολογισμός H(Y|X), H(X|Y)",color=ModernDarkTheme.BG_LIGHT_ORANGE)
        self.calc_cond_btn.grid(row=0, column=2, rowspan=2, padx=6, pady=4)

        # Output box
        self.cond_result_text = self._scrolled(f, 14)
        self.cond_result_text.grid(row=2, column=0, columnspan=3, padx=6, pady=6, sticky="nsew")

        f.grid_columnconfigure(1, weight=1)
        f.grid_rowconfigure(2, weight=1)
